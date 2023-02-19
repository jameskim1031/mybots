import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.bodyLength = 4
        # np.random.randint(low=c.minBodyLength, high=c.maxBodyLength, size = 1)[0]
        self.legStart = 0.5
        self.legIncrement = 1
        if self.bodyLength % 2 == 1:
            self.legStart = self.legIncrement = (self.bodyLength / 2) / ((self.bodyLength + 1) / 2)
        
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
        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Body0", pos=[-2,0,0.45], size=[self.bodyLength,1,0.5], color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        #left side
        left_leg_pos = self.legStart - 4
        body_count = 1
        for i in range(self.bodyLength):
            # thigh
            pyrosim.Send_Joint( name = "Body0_Body" + str(body_count) , parent= "Body0", child = "Body" + str(body_count), type = "revolute", position = [left_leg_pos,-0.5,0.45], jointAxis = "0 0 1")
            pyrosim.Send_Cube(name="Body" + str(body_count), pos=[0,-0.25,0], size=[0.2,0.5,0.2], color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')

            # # leg
            pyrosim.Send_Joint( name = "Body" + str(body_count) + "_Body" + str(body_count + 1) , parent= "Body" + str(body_count), child = "Body" + str(body_count + 1), type = "revolute", position = [0,-0.5,0], jointAxis = "0 0 1")
            pyrosim.Send_Cube(name="Body" + str(body_count + 1), pos=[0,0,-0.2], size=[0.2,0.2,0.4], color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')

            left_leg_pos += self.legIncrement
            body_count += 2
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Body0")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Body1")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Body2")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Body3")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "Body4")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "Body5")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "Body6")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "Body7")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "Body8")
        

        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Body0_Body1")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Body0_Body3")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Body0_Body5")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Body0_Body7")
        
        
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