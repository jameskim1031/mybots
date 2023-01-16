import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim

from sensor import SENSOR
from motor import MOTOR

class ROBOT:
    def __init__(self):
        self.motor = {}
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        
    
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            print(linkName)
            self.sensors[linkName] = SENSOR(linkName)
            
    def Sense(self, currIndex):
        for sensor in self.sensors.values():
            sensor.Get_Value(currIndex)

        # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

# In ith pass through the for loop, call the ith SENSOR instance's Get_Value() method. When called, this method should store the current value of the touch sensor in self.values. But, we do not know which element it should be stored in. It should be stored in the tth element, where t is the current time step.