import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain.nndf")
        
    
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

# Now we are ready to pass this desired angle to the appropriate motor. Copy the statement in ROBOT's Act() that sets the value of the motor attached to the joint called jointName and paste a copy of it just before the print statement in Act().

    def Act(self, currIndex):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[bytes(jointName, encoding='utf-8')].Set_Value(self.robotId, desiredAngle)
           
    def Think(self):
        self.nn.Update()
        self.nn.Print()
