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

force = 30

numberOfGenerations = 15

populationSize = 15

numSensorNeurons = 9

numMotorNeurons = 8

motorJointRange = 0.4