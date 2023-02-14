import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(6,5)
        self.weights = self.weights * 2 - 1
        self.numSensors = np.random.randint(low=1, high=c.bodyNum, size = 1)[0]
        self.sensors = np.random.choice(c.bodyNum + 1, self.numSensors, replace=False)
        
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("del fitness" + str(self.myID) +".txt")        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[0,3,1] , size=[1,1,1])
        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        initial_pos = np.array([2,0, c.maxHeight / 2])
        initial_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
        temp_joint = np.array([2 - (initial_size[0] / 2), 0, initial_pos[2]])
        
        if 0 in self.sensors:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist(), size=initial_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        else:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist() , size=initial_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
        for i in range(c.bodyNum):
            temp_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
            temp_pos = np.array([-(temp_size[0] / 2), 0, 0])
            pyrosim.Send_Joint( name = "Body" + str(i) + "_Body" + str(i + 1) , parent= "Body" + str(i) , child = "Body" + str(i + 1), type = "revolute", position = temp_joint.tolist(), jointAxis = "0 1 0")
            if i in self.sensors:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            else:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
            temp_joint = np.array([-(temp_size[0]), 0, 0])
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        for i in range(c.bodyNum + 1):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = "Body" + str(i))
        # sensors are [0,2,3]
        # pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Body0")
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Body1")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Body2")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Body3")

        for i in range(c.bodyNum):
            pyrosim.Send_Motor_Neuron( name = i + c.bodyNum , jointName = "Body" + str(i) + "_Body" + str(i + 1))

        # pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Body0_Body1")
        # pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Body1_Body2")
        # pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Body2_Body3")
        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID