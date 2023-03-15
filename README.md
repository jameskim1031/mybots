# James's Ludobot Playground

Welcome to James's Ludobot Playground! Here, I will provide you step by step explanations on how my ludobots randomly form and evolve over generations to move faster in a straight line. I will also provide explanation on how you can generate your own random robots/ creatures and witness how they evolve! Hope you have a ludof fun!

## Things you can do:

1. Create your own robots (TRY IT OUT!):

    * In **constants.py**, set numberOfGeneration, populationSize, and numOfSeeds as you want
      
      * For testing purposes, I set numberOfGeneration = 5, populationSize = 3, numOfSeeds = 1
    
    * Run **search.py**

2. Observe our robot's evolution over generations:
    
    * In **load.py**, choose creature_number (between 0 and 9) and generation_number (0 or 250 or 499)
    
      * Recommended: Select a creature_number and run **load.py** at generation_number 0, 250, and 499 in this order
    
    * Running **load.py** shows how a same robot looks like at different generations
    
    * The robots you will see are from running 500,000 simulations
    
3. Observe our best robots:
    
    * FINISH THIS PART
    
    
    
## Documentation

In this documentation, I will show how the robot's body and brain is first generated. Then I will explain how the creature chooses to mutate at each generation and perform selection to improve itself through parallel hillclimber. Finally, I will share some plots I collected to provide evidence that the robots really did improve over mulitple generations.

### Generating body & brain

#### High level overview of body generation

The robots contain 3 building blocks: the spine, the arm, and the leg. The spine is the central building block that runs through the middle of the robots. The arm extends from the spine to the left and the right. The leg extends from the arm to the sky or to the ground. 

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225151951-114dc941-09fa-4765-99aa-b3b7be097c05.jpg" width="500">
</div>
As seen above in the diagram, spines are added along the x axis, arms along the y axis, and legs along the z axis. The order of generation always follows spine -> arms -> legs. Therefore, a leg cannot be generated without an arm, which cannot be created without a spine.

#### Joints and cubes

All building blocks of ludobots are generated in simulation using pyrosim's Send_Cube() and Send_Joint() functions. The Send_Cube() function is responsible for creating the actual blocks, while the Send_Joint() function creates the joints between the blocks. For example, to attach an arm to a spine, we would first use the Send_Cube() function to create a spine block, use the Send_Joint() function to create a joint between the spine and the arm, and finally use the Send_Cube function again to create a arm block. 

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225155646-500b526b-123a-4190-b864-c8c6fff0d1e8.jpg" width="500">
</div>

Notice how I had to create the joint for the spine and the arm before I created the arm block. This is particularly important because, in pyrosim, the block's positions are relative to the relevant joint's position. I'll explain how this works in the diagram below. 

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225159725-2b4ee58c-1083-4958-80ec-065ce7a04c90.jpg" width="800">
</div>

#### Generate_Body() and Generate_BRAIN() functions

Another thing to note is that, in my code, I do not immediately use Send_Cube() and Send_Joint() when I initializing the robot. Instead, in my __init__() function of my SOLUTION class, I store all the parameter informations I need to use the two functions into a global variable called **self.everything**. Then to actually generate the robot, in my function Generate_Body(), I loop through self.everything, determine if the part is a joint or a block and apply Send_Cube() and Send_Joint() accordingly. I will explain why I do this later is my mutation documentation. Below is the code for Generate_Body().

```
def Generate_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.nndf")
        for part in self.everything:
            if part[-1] == 'joint':
                pyrosim.Send_Joint( name = part[0] , parent= part[1] , child = part[2], type = "revolute", position = part[3].tolist(), jointAxis = "0 1 0")
            else:
                pyrosim.Send_Cube(name= part[0], pos= part[1] , size= part[2], color_string= part[4], color_name=part[5])
        pyrosim.End()
```

Along with storing all relevant parameter in **self.everything**, I also keep track of just the blocks in a global variable called **self.sensors** and just the joints in a global varibale called **self.motors**. The variable that stores the blocks are called **self.sensors** because it is the parts/ blocks that senses the surroundings just like your body parts senses your surroundings. The variable that stores the joinst are called **self.motors** because it is the joints that moves the robot parts just like your elbow moves your upper arm and lower arm. Just like your sensors and joints comumunicate with each other in your body (e.g. when you grab a hot pot, your hand sensors tell your body to move your hand), our robot's sensors and motors communicate with each other. Just like our human bodies, the communication between the motor neurons and sensor neurons in our robot happens through synapses. There is a single synapse between all of our sensor neurons and all of our motor neurons. The matrix self.weights represents how strong a sensor neuron is connected to a motor neuron. The function **Send_Synapse()** connects neurons together with the relevant weights from self.weights. The diagram below shows how synapse connects all the neurons to each other.

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225163584-019e03d0-bfc5-492c-8f62-bad2382ae32a.jpg" width="600">
</div>

This is done in the **Generate_Brain** function. 

```
def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")        
        name = 0
        for sensor in self.sensors:
            pyrosim.Send_Sensor_Neuron(name = name , linkName = sensor)
            name += 1
        for motor in self.motors:
            pyrosim.Send_Motor_Neuron( name = name , jointName = motor)
            name += 1
        for currentRow in range(len(self.sensors)):
            for currentColumn in range(len(self.motors)):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + len(self.sensors), weight = self.weights[currentRow, currentColumn]) 
        pyrosim.End()
```

Below is a diagram of how the synapses (black line) connect sensor neurons and motor neurons:



#### Randomizing the robot's generation

So now that we understand how robots are generated in pyrosim, let's dive into how they are randomized in generation. Remember that that the parts are generated in the order of spine -> arm -> leg, and that the legs are attached to the arms, and that the arms are attach to the spine. Having this knowledge in mind, here is a tree representation of how the blocks are randomized:

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225166658-c0e854d8-f22c-4878-a423-38def7cc36c9.jpg" width="600">
</div>

In the figure above, I wasn't able to finish the tree for the far right "Two Arms" because of space, however, the same logic follows for the left and right arm. This tree repeats each time a new spine is added. Throughout the generation, a global variable **self.currentPartCount** keeps track of how many parts are created. Generation stops as soon as **self.currentPartCount** reaches **self.totalPartNum**.

### Mutation

Now that we know how the robot is initially generated, we will look into how the robot mutates throughout generations. At each generation, the robot randomly chooses one of these 3 methods to mutate:

1. Change a sensor/ motor synapse in self.weights
2. Add a body part
3. Remove a body part

If a robot chooses method 1, it randomly selects a sensor and motor pairing represented by self.weights[sensor, motor]. Then it updates this value with another random value. This changes the weight of the synapse between the selected sensor and motor. 
```
randomRow = random.randint(0, len(self.sensors) - 1)
randomColumn = random.randint(0, len(self.motors) - 1)
self.weights[randomRow,randomColumn] = (random.random() * 2) - 1
```

If a robot chooses method 2, it will randomly select a body part to add to the robot. How does the robot know which body part to add to which body part? Dictionary! A global dictionary called **self.partsToAdd** keeps track of all body parts that can be added at each mutation. Here is a representation of how parts are added to **self.partsToAdd**:

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225173027-3adb4454-259d-4f34-b10e-0f3d22b2b81e.jpg" width="600">
</div>

The left side of the diagram represents the current robot with its parts labelled. The right side of the diagram shows the same robot but with orange parts that shows which parts can be added and still maintain the spine -> arm -> leg structure that we established. Thus, all the orange parts are added to **self.partsToAdd**. Then in the Mutate() function, the robot will randomly select one of the key, value pairings of this **self.partsToAdd** dictionary and append it to **self.everything** so that the new part is included in the next generation. If a part is added, the robot also makes sure to update the **self.partsToAdd** dictionary so that it includes new parts that can be added. An example is shown below
