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
            self.robot.Act(i)
            
    
    def __del__(self):
        p.disconnect()