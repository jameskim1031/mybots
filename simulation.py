import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random
import constants as c

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        
        self.world = WORLD()
        self.robot = ROBOT()


    def Run(self):
        for i in range(c.length):
            time.sleep(c.sleepTimer)
            p.stepSimulation()
            self.robot.Sense(i)
            # backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            # frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = self.robotId,
            #     jointName = b'Torso_BackLeg',
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = BackLegTargetAngles[i],
            #     maxForce = c.force)
            # pyrosim.Set_Motor_For_Joint(
            #     bodyIndex = self.robotId,
            #     jointName = b'Torso_FrontLeg',
            #     controlMode = p.POSITION_CONTROL,
            #     targetPosition = FrontLegTargetAngles[i],
            #     maxForce = c.force)
    
    def __del__(self):
        p.disconnect()