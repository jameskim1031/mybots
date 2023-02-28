import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        

    def Set_Value(self, robotId, desiredAngle):
        # if t == c.length - 1:
        #     numpy.save("./data/motor" + str(self.jointName) + ".npy",self.motorValues)
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.force)