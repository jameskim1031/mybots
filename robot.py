import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import os
import constants as c

class ROBOT:
    def __init__(self, solutionID):
        self.motors = {}
        self.robotId = p.loadURDF("body" + str(solutionID) + ".nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.solutionID = solutionID
        self.nn = NEURAL_NETWORK("brain" + self.solutionID +".nndf")
        os.system("del brain" + str(self.solutionID) + ".nndf")
        os.system("del body" + str(self.solutionID) + ".nndf")
        

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
    
    def Sense(self, currIndex):
        for sensor in self.sensors.values():
            sensor.Get_Value(currIndex)
    
    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, currIndex):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[bytes(jointName, encoding='utf-8')].Set_Value(self.robotId, desiredAngle)
           
    def Think(self):
        self.nn.Update()
        self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        zPosition = basePosition[2]

        f = open("tmp" + self.solutionID + ".txt", "w")
        f.write(str(xPosition))
        f.close()
        
        os.system("rename tmp" + self.solutionID + ".txt fitness" + self.solutionID + ".txt")
        exit()

# Find where in the SIMULATION class hierarchy you have to modify the writing of fitness into fitnesssolutionID.txt instead of fitness.txt, and do so.