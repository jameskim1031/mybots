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




# BackLegAmplitude, BackLegFrequency, BackLegPhaseOffset = c.BLAmp, c.BLFreq, c.BLPhaseOffset
# BackLegTargetAngles = numpy.zeros(c.length)
# BackLegTargetAngles = BackLegAmplitude * numpy.sin(BackLegFrequency * numpy.linspace(c.start, c.end, c.length) + BackLegPhaseOffset)

# FrontLegAmplitude, FrontLegFrequency, FrontLegPhaseOffset = c.FLAmp, c.FLFreq, c.FLPhaseOffset
# FrontLegTargetAngles = numpy.zeros(c.length)
# FrontLegTargetAngles = FrontLegAmplitude * numpy.sin(FrontLegFrequency * numpy.linspace(c.start, c.end, c.length) + FrontLegPhaseOffset)

# numpy.save("./data/backLegSensorValues.npy",backLegSensorValues)
# numpy.save("./data/frontLegSensorValues.npy",frontLegSensorValues)
# numpy.save("./data/BackLegTargetAngles.npy",BackLegTargetAngles)
# numpy.save("./data/FrontLegTargetAngles.npy",FrontLegTargetAngles)






# targetAngles = numpy.sin(numpy.linspace(0, numpy.pi * 2, 1000)) * (numpy.pi / 4)