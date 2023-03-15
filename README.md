# James's Ludobot Playground

Welcome to James's Ludobot Playground! Here, I will provide you step by step explanations on how my ludobots randomly form and evolve over generations to move faster in a straight line. I will also provide explanation on how you can generate your own random robots/ creatures and witness how they evolve! Hope you have a ludof fun!

## Deliverables:
* 10 second preview:      

   * ![Ludobot_Final_Project__1__AdobeExpress](https://user-images.githubusercontent.com/95663596/225208127-133ff949-c022-4133-810f-68e09ead882b.gif)

* 2 minute video: https://youtu.be/fqxOYwTM7jE

* Grading: Engineering

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

#### Method 1: Change Synapse
If a robot chooses method 1, it randomly selects a sensor and motor pairing represented by self.weights[sensor, motor]. Then it updates this value with another random value. This changes the weight of the synapse between the selected sensor and motor. 
```
randomRow = random.randint(0, len(self.sensors) - 1)
randomColumn = random.randint(0, len(self.motors) - 1)
self.weights[randomRow,randomColumn] = (random.random() * 2) - 1
```

#### Method 2: Add Part
If a robot chooses method 2, it will randomly select a body part to add to the robot. How does the robot know which body part to add to which body part? Dictionary! A global dictionary called **self.partsToAdd** keeps track of all body parts that can be added at each mutation. Here is a representation of how parts are added to **self.partsToAdd**:

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225173027-3adb4454-259d-4f34-b10e-0f3d22b2b81e.jpg" width="600">
</div>

The left side of the diagram represents the current robot with its parts labelled. The right side of the diagram shows the same robot but with orange parts that shows which parts can be added and still maintain the spine -> arm -> leg structure that we established. Thus, all the orange parts are added to **self.partsToAdd**. Then in the Mutate() function, the robot will randomly select one of the key, value pairings of this **self.partsToAdd** dictionary and append it to **self.everything** so that the new part is included in the next generation. If a part is added, the robot also makes sure to update the **self.partsToAdd** dictionary so that it includes new parts that can be added. An example is shown below: 

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225174322-e89d6256-b4d2-4a6f-9e32-1646e6a3c08f.jpg" width="700">
</div>

As you can see, an new arm has been formed and two new parts to add have been created in the purple circle.

#### Method 3: Remove Part
If a robot chooses method 3, it will randomly select a body part to remove from the robot. Similarly to the method 2, the robot uses a dictionary called **self.partsToRemove** to keep track of existing parts to remove. For this, the robot identify the leaf node body parts during the initial generation and adds it to the dictionary. Then the Mutate() function randomly chooses a part to remove from the dictionary, identifies which elements of the self.everything list matches with the randomly selected part, and removes the element from self.everything. Thus, the robot will no longer have those existing parts in the next generation. Below is an example:

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225175064-0dfcedbc-cd95-4a9e-8293-12f9f7a02a16.jpg" width="700">
</div>

The left side represents current robot and the right side shows potential parts to remove as circled in orange. Similar to method 2, the Mutate() function makes sure to add new potential parts to remove if removing a part creates another leaf node body part. An example is shown below:

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225175482-13a3f121-80c3-49c6-b8be-46e5a6a9f9e5.jpg" width="700">
</div>

As you can see, one of the legs has been removed and the attached arm has been now identified as a potential part to remove.

### Selection: Hill climber

Now that the robot is able to mutate its body, how does it decide which version of the body to keep? This question is key to our topic of "evolving" robot. For a robot to evolve means is to mutate itself to get better at something. This what **hill climbing** is. Every time our robot mutates, our program will select which version of the robot performed better. 

In our program, the goal of the robot is to travel the furthest in the positive x direction. Thus, the **fitness** value of our robots are how far each robot traveled in the positive x direciotn.

The robot's Get_Fitness() function in robot.py collects the fitness values:
```
def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]

        f = open("tmp" + self.solutionID + ".txt", "w")
        f.write(str(xPosition))
        f.close()
        
        os.system("rename tmp" + self.solutionID + ".txt fitness" + self.solutionID + ".txt")
        exit()
```

At each mutation, the hill climbing algorithm will compare the fitness of the parent (previous) generation and the child (new) generation then keep the the generation that traveled the furthest in the positive x direction. 

The Select() function in parallelHillClimber.py performs this selection process:
```
def Select(self):
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]
```

We perform the "selection" by ensuring that the parent always has the best fitness. Thus, at the end of the hillclimbing, the parent will be the "best" robot. 

### Parellel Hill Climber

<img src="https://user-images.githubusercontent.com/95663596/225183856-3af89b68-7f06-4882-b9f6-ecd4db59fa5f.jpg" width="700">

<img src="https://user-images.githubusercontent.com/95663596/225184009-bb41b0da-326b-4a7d-91ba-fef6596cbc25.jpg" width="700">

What is interesting about our program is that we are able run multiple of these hill climbing selection in parallel. If this is confusing, think about it like this:

A single hill climber is like giving a child random cookie ingredients to make a yummy cookie. Every 10 minutes, you magically duplicate the cookie into 2 cookies. You then give the child more ingredients and ask him to add those new ingredients to only one of the cookies. Once the child works on the cookie, you taste the two and only keep the cookie you like better. After many hours, you will have with you the best version of the cookie.

In parallel hillclimbing, you have not 1 but 10 children to make you cookies in the same process. After many hours, you will have the amazing cookies from 10 children. Now for the final contest, you will try the top cookies from each of the children and choose the very best cookie.

Applying this to our program, at the end of parallel hillclimbing, we will have with us the best robots of each population. Each child in the cookie contest represent each population of parallel hillclimbing. 

``` 
def Show_Best(self):
        all_solution = self.parents.items()
        highest_fitness = max(all_solution, key=lambda x: x[1].fitness)
        highest_parent = highest_fitness[1]
        highest_parent.Start_Simulation("GUI")
```

The **Show_Best()** function in **parallelHillClimber.py** does the "final contest" of the robots. The variable **self.parents** contains the best robot of each population represented by **self.parent**. The function compares the fitness values of all of the parents and find the robot that travels the furthest in the positive x-direction. Thus, parallel hill climbing allows us to select the best robot from a larger pool of robots by running multiple populations together.

### Results

For the final project, I was able to run 10 seeds of 500 generations and 10 population (a total of 500,000 simulation). To show that the robot actually improves (increases fitness value) over many generations, I created a plot that compares the number of generation and the fitness value of the best robot of each seed: 

<div align="center">
  <img src="https://user-images.githubusercontent.com/95663596/225186181-cdb10721-1a83-4e0f-b7c3-2755fe84b61a.png" width="700">
</div>

As you can see, there is a clear trend of the fitness value going up as the generation number increases. The flat parts of the lines represent when there are no new generation that are better than the current robot. Everytime there is a increase in the graph, it is showing that the parallel hill climb has found a better robot with better fitness value.

As shown in the first section of this README, you are able to see the lineage of mutation for couple of the robots that I have generate using **load.py**. Here are couple examples that shows exactly how the robot has mutated. 

Robot at generation 0:

<img src="https://user-images.githubusercontent.com/95663596/225189442-1e3d5de6-a54c-4704-929f-bfaf4c0f51a6.png" width="200">


Robot at generation 250:

<img src="https://user-images.githubusercontent.com/95663596/225190170-e17c4c6e-0f2e-4343-9f84-83cb14c79dc7.png" width="200">


Robot at generation 499:

<img src="https://user-images.githubusercontent.com/95663596/225190236-6daade85-9744-4369-bc2c-c64bcebe6693.png" width="200">

We can see from the 3 images above that between generation 0 and generation 250, the robot added arms and legs. There is no change of the robot physical body between 250 and 499. However, knowing that the fitness still improved, the robot probablychanged its synpase weights. This is an expected behavior of the robots as the graph indicates that the fitness value doesn't go up signifcantly after 250 generations. 

### Conclusion

I hope that this playground helped explain how we created a robot that evolved over many generations. The plot of 500,000 simulation showed that the robots did infact evolve to have greater fitness values over time. We also learned that the evolution has a logarithmic growth as shown in the plot and also the minimal physical changes it goes through after 250 generation. Again, I encourage you to play around with **load.py** to see the lineage of the robot's evolution over many generation and to also create your own robot using **search.py**


## Citation
* https://www.reddit.com/r/ludobots/
* https://xenobots.github.io/
