import numpy as np
import random


BLAmp = np.pi /4
BLFreq = 1
BLPhaseOffset = 0

FLAmp = 4
FLFreq = 20
FLPhaseOffset = 0

length = 2000
start, end = 0, np.pi * 2

sleepTimer = 1/90

force = 30

numberOfGenerations = 1

populationSize = 1

motorJointRange = 0.5

bodyNum = np.random.randint(low=2, high=4, size = 1)[0]

numSensorNeurons = bodyNum + 1

numMotorNeurons = bodyNum

maxHeight = 3

maxWidth = 3

maxLength = 2