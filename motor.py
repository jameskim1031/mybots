import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.Prepare_To_Act()
        self.jointName = jointName

    def Prepare_To_Act(self):
        self.amplitude = c.BLAmp
        self.frequency = c.BLFreq
        self.offset = c.BLPhaseOffset
        self.motorValues = self.amplitude * numpy.sin(self.frequency * numpy.linspace(c.start, c.end, c.length) + self.offset)
        # FrontLegAmplitude, FrontLegFrequency, FrontLegPhaseOffset = c.FLAmp, c.FLFreq, c.FLPhaseOffset
        # FrontLegTargetAngles = numpy.zeros(c.length)
        # FrontLegTargetAngles = FrontLegAmplitude * numpy.sin(FrontLegFrequency * numpy.linspace(c.start, c.end, c.length) + FrontLegPhaseOffset)

    def Set_Value(self, robotId, t):
        print("yoo")
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[t],
            maxForce = c.force)

        # pyrosim.Set_Motor_For_Joint(
        #     bodyIndex = self.robotId,
        #     jointName = b'Torso_FrontLeg',
        #     controlMode = p.POSITION_CONTROL,
        #     targetPosition = FrontLegTargetAngles[i],
        #     maxForce = c.force)




        



    