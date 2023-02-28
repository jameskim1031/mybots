import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import constants as c
import math

class BODY:
    def __init__(self, body_id, start_pos, jointList):
        self.jointList = jointList
        self.body_id = body_id
        self.joint_pos = start_pos

        self.length = max(1,np.random.rand() * 2)
        self.width = max(1,np.random.rand() * 2)
        self.height = np.random.rand() * 1

        self.numMotors = 0
        self.numSensors = 0
    
    def createBody(self):
        # create one snake body
        body_size = [self.length, self.width, self.height]
        body_pos = [-(body_size[0] / 2), 0, 0]
        pyrosim.Send_Cube(name="Body" + str(self.body_id), pos=body_pos , size=body_size, color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        self.numSensors += 1
        self.numArms = np.random.randint(low=1, high=4, size = 1)[0]
        if self.numArms == 0:
            self.joint_pos = [-(body_size[0]), 0, 0]
        elif self.numArms == 1:
            # get joint + block position for left arm
            arm_joint = [-(body_size[0] / 2), -(body_size[1] / 2), 0]
            arm_size = [(np.random.rand() * body_size[0]), (np.random.rand() * body_size[1]), (body_size[2] / 2)]
            arm_position = [0, -(arm_size[1] / 2), 0]
            # send it to create arm
            self.createArm(arm_joint, arm_size, arm_position, self.body_id + self.numSensors)
            self.joint_pos = [-(body_size[0]),0, 0]
        elif self.numArms == 2:
            # get joint + block position for right arm
            arm_joint = [-(body_size[0] / 2), (body_size[1] / 2), 0]
            arm_size = [(np.random.rand() * body_size[0]), (np.random.rand() * body_size[1]), (body_size[2] / 2)]
            arm_position = [0, (arm_size[1] / 2), 0]
            self.createArm(arm_joint, arm_size, arm_position, self.body_id + self.numSensors)
            self.joint_pos = [-(body_size[0]),0, 0]
        else:
            # get joint + block position for left arm
            # send it to create arm
            left_arm_joint = [-(body_size[0] / 2), -(body_size[1] / 2), 0]
            left_arm_size = [(np.random.rand() * body_size[0]), (np.random.rand() * body_size[1]), (body_size[2] / 2)]
            left_arm_position = [0, -(left_arm_size[1] / 2), 0]
            # send it to create arm
            self.createArm(left_arm_joint, left_arm_size, left_arm_position, self.body_id + self.numSensors)
            # get join + block position for right arm
            right_arm_joint = [-(body_size[0] / 2), body_size[1] / 2, 0]
            right_arm_size = [(np.random.rand() * body_size[0]), (np.random.rand() * body_size[1]), (body_size[2] / 2)]
            right_arm_position = [0, (right_arm_size[1] / 2), 0]
            # send it to create arm
            self.createArm(right_arm_joint, right_arm_size, right_arm_position, self.body_id + self.numSensors)
            self.joint_pos = [-(body_size[0]),0, 0]

    def createArm(self, joint, size, position, armID):
        pyrosim.Send_Joint( name = "Body" + str(self.body_id) + "_Body" + str(armID), parent= "Body" + str(self.body_id) , child = "Body" + str(armID), type = "revolute", position = joint, jointAxis = "0 1 0")
        self.jointList.append([self.body_id, armID])
        self.numMotors += 1
        pyrosim.Send_Cube(name="Body" + str(armID), pos=position , size=size, color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        self.numSensors += 1
        self.numLegs = np.random.randint(low=0, high=3, size = 1)[0]
        self.numLegs = 1
        if self.numLegs == 0:
            pass
        elif self.numLegs == 1:
            leg_joint = [0, position[1]*2, 0]
            pyrosim.Send_Joint( name = "Body" + str(armID) + "_Body" + str(armID + 1), parent= "Body" + str(armID) , child = "Body" + str(armID + 1), type = "revolute", position = leg_joint, jointAxis = "0 0 1")
            self.jointList.append([armID, armID + 1])
            #print(self.jointList)
            self.numMotors += 1
            leg_size = [size[0], size[1] / 2,c.maxHeight / 4]
            leg_position = [0,0,-(leg_size[2] / 2)]
            pyrosim.Send_Cube(name="Body" + str(armID + 1), pos=leg_position , size=leg_size, color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            self.numSensors += 1
        else:
            leg_joint = [0, position[1]*2, 0]
            pyrosim.Send_Joint( name = "Body" + str(armID) + "_Body" + str(armID + 1), parent= "Body" + str(armID) , child = "Body" + str(armID + 1), type = "revolute", position = leg_joint, jointAxis = "0 0 1")
            self.jointList.append([armID, armID + 1])
            self.numMotors += 1
            leg_size = [size[0], size[1] / 2,c.maxHeight / 4]
            leg_position = [0,0,(leg_size[2] / 2)]
            pyrosim.Send_Cube(name="Body" + str(armID + 1), pos=leg_position , size=leg_size, color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            self.numSensors += 1