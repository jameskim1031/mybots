import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        
    
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
        for motor in self.motors.values():
            motor.Set_Value(self.robotId, currIndex)

# In ith pass through the for loop, call the ith SENSOR instance's Get_Value() method. When called, this method should store the current value of the touch sensor in self.values. But, we do not know which element it should be stored in. It should be stored in the tth element, where t is the current time step.