import numpy as np
import random


BLAmp = np.pi /4
BLFreq = 1
BLPhaseOffset = 0

FLAmp = 4
FLFreq = 20
FLPhaseOffset = 0

length = 500
start, end = 0, np.pi * 2

sleepTimer = 1/90

force = 30

numberOfGenerations = 1

populationSize = 1

motorJointRange = 0.6

bodyNum = 3
# np.random.randint(low=3, high=5, size = 1)[0]

numSensorNeurons = bodyNum + 1

numMotorNeurons = bodyNum

maxHeight = 1

maxWidth = 3

maxLength = 2