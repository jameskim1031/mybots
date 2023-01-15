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

amplitude, frequency, phaseOffset = numpy.pi/4, 1, 0
targetAngles = numpy.zeros(1000)

for i in range(1000):
    targetAngles[i] = amplitude * numpy.sin(frequency * (i/1000 * (2 * numpy.pi)) + phaseOffset)
    time.sleep(1/60)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = numpy.sin(i/1000 * (2 * numpy.pi)) * numpy.pi/4,
        maxForce = 30)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = numpy.sin(i/1000 * (2 * numpy.pi)) * numpy.pi/4,
        maxForce = 30)
numpy.save("./data/backLegSensorValues.npy",backLegSensorValues)
numpy.save("./data/frontLegSensorValues.npy",frontLegSensorValues)
numpy.save("./data/targetAngles.npy",targetAngles)
p.disconnect()
