import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c
from body import BODY
from LinkedList import LinkedList

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        # self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        # self.weights = self.weights * 2 - 1
        self.weights = []
        self.numMotors = 0
        self.numSensors = 0
        self.chooseSensors = np.random.randint(low=0, high=c.bodyNum, size = 1)[0]
        self.chosenSensors = np.random.choice(c.bodyNum + 1, self.chooseSensors, replace=False)
        self.jointList = []
        self.LinkedList = LinkedList()
        
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
        pyrosim.Start_URDF(f"body{self.myID}.nndf")
        initial_pos = [2,0, c.maxHeight / 2]
        initial_size = [0.75, 0.3, 0.5]
        body_joint_pos = [2 - (initial_size[0] / 2), 0, initial_pos[2]]
        motor_count = 0
        sensor_count = 0
        
        pyrosim.Send_Cube(name="Body0", pos=initial_pos, size=initial_size, color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
        sensor_count += 1
        self.LinkedList.add(initial_pos, initial_size, body_joint_pos)
        

        parent = 0
        self.jointList = []
        for i in range(c.bodyNum - 1):
            pyrosim.Send_Joint( name = "Body" + str(parent) + "_Body" + str(sensor_count) , parent= "Body" + str(parent) , child = "Body" + str(sensor_count), type = "revolute", position = body_joint_pos, jointAxis = "0 1 0")
            motor_count += 1
            self.jointList.append([parent, sensor_count])
            body = BODY(sensor_count, body_joint_pos, self.jointList)
            body.createBody()
            sensor_count += body.numSensors
            motor_count += body.numMotors
            body_joint_pos = body.joint_pos
            parent = body.body_id

        self.numMotors = motor_count
        self.numSensors = sensor_count

        if self.weights == []:
            self.weights = np.random.rand(self.numSensors,len(self.jointList))
            self.weights = self.weights * 2 - 1

        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        for i in range(self.numSensors):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = "Body" + str(i))

        nameCount = self.numSensors
        for parent, child in self.jointList:
            pyrosim.Send_Motor_Neuron( name = nameCount , jointName = "Body" + str(parent) +"_Body" + str(child))
            nameCount += 1

        for currentRow in range(self.numSensors):
            for currentColumn in range(len(self.jointList)):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensors, weight = (np.random.rand(1)[0] * 2) - 1)
        pyrosim.End()

    def Mutate(self):
        self.LinkedList.Generate_Body_Using_LinkedList()
        self.numSensors += 1
        self.numMotors += 1
        randomRow = random.randint(0, self.numSensors - 2)
        randomColumn = random.randint(0, self.numMotors - 2)
        self.weights[randomRow][randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID