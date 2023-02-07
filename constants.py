import numpy

BLAmp = numpy.pi /4
BLFreq = 1
BLPhaseOffset = 0

FLAmp = 4
FLFreq = 20
FLPhaseOffset = 0

length = 500
start, end = 0, numpy.pi * 2

sleepTimer = 1/60

force = 50

numberOfGenerations = 10

populationSize = 10

numSensorNeurons = 3

numMotorNeurons = 2

motorJointRange = 0.8