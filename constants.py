import numpy

BLAmp = numpy.pi /4
BLFreq = 1
BLPhaseOffset = 0

FLAmp = 4
FLFreq = 20
FLPhaseOffset = 0

length = 250
start, end = 0, numpy.pi * 2

sleepTimer = 1/60

force = 30

numberOfGenerations = 1

populationSize = 1

numSensorNeurons = 9

numMotorNeurons = 4

motorJointRange = 0.8

maxBodyLength = 7

minBodyLength = 2