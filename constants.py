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

sleepTimer = 1/60

force = 100

numberOfGenerations = 3

populationSize = 1

motorJointRange = 0.6

bodyNum = np.random.randint(low=3, high=6, size = 1)[0]

numSensorNeurons = bodyNum + 1

numMotorNeurons = bodyNum

maxHeight = 2

maxWidth = 2

maxLength = 2