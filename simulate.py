import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random
import constants as c
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()

# numpy.save("./data/backLegSensorValues.npy",backLegSensorValues)
# numpy.save("./data/frontLegSensorValues.npy",frontLegSensorValues)
# numpy.save("./data/BackLegTargetAngles.npy",BackLegTargetAngles)
# numpy.save("./data/FrontLegTargetAngles.npy",FrontLegTargetAngles)






# targetAngles = numpy.sin(numpy.linspace(0, numpy.pi * 2, 1000)) * (numpy.pi / 4)