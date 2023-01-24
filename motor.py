import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        # self.Prepare_To_Act()

    # def Prepare_To_Act(self):
    #     self.amplitude = c.BLAmp
    #     self.frequency = c.BLFreq
    #     self.offset = c.BLPhaseOffset
    #     if self.jointName == b'Torso_BackLeg':
    #         self.frequency /= 2
    #     self.motorValues = self.amplitude * numpy.sin(self.frequency * numpy.linspace(c.start, c.end, c.length) + self.offset)
        

    def Set_Value(self, robotId, desiredAngle):
        # if t == c.length - 1:
        #     numpy.save("./data/motor" + str(self.jointName) + ".npy",self.motorValues)
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.force)
        




        



    