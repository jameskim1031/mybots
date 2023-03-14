import numpy as np
import random


BLAmp = np.pi /4
BLFreq = 1
BLPhaseOffset = 0

FLAmp = 4
FLFreq = 20
FLPhaseOffset = 0

length = 1000
start, end = 0, np.pi * 2

sleepTimer = 1/1000

force = 75

numberOfGenerations = 100

populationSize = 1

motorJointRange = 0.6

bodyNum = np.random.randint(low=3, high=6, size = 1)[0]

numSensorNeurons = bodyNum + 1

numMotorNeurons = bodyNum

maxHeight = 1

maxWidth = 1

maxLength = 1

numOfSeeds = 5