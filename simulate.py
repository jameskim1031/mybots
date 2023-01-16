import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

BackLegAmplitude, BackLegFrequency, BackLegPhaseOffset = numpy.pi / 20, 10, numpy.pi/4
BackLegTargetAngles = numpy.zeros(1000)
BackLegTargetAngles = BackLegAmplitude * numpy.sin(BackLegFrequency * numpy.linspace(0, numpy.pi * 2, 1000) + BackLegPhaseOffset)

FrontLegAmplitude, FrontLegFrequency, FrontLegPhaseOffset = 4, 20, 0
FrontLegTargetAngles = numpy.zeros(1000)
FrontLegTargetAngles = FrontLegAmplitude * numpy.sin(FrontLegFrequency * numpy.linspace(0, numpy.pi * 2, 1000) + FrontLegPhaseOffset)

for i in range(1000):
    time.sleep(1/60)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = BackLegTargetAngles[i],
        maxForce = 30)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = FrontLegTargetAngles[i],
        maxForce = 30)
numpy.save("./data/backLegSensorValues.npy",backLegSensorValues)
numpy.save("./data/frontLegSensorValues.npy",frontLegSensorValues)
numpy.save("./data/BackLegTargetAngles.npy",BackLegTargetAngles)
numpy.save("./data/FrontLegTargetAngles.npy",FrontLegTargetAngles)

p.disconnect()


# targetAngles = numpy.sin(numpy.linspace(0, numpy.pi * 2, 1000)) * (numpy.pi / 4)