import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.totalPartNum = 8
        self.currentPartCount = 0
        self.spineID = 0
        self.armID = 0
        self.legID = 0
        self.sensors = []
        self.motors = []
        self.everything = []
        self.partsToAdd = {}
        self.partsToRemove = {}
        self.totalPartsToAdd = 0
        self.getEverything()
        self.weights = np.random.rand(len(self.sensors),len(self.motors))
        self.weights = self.weights * 2 - 1
        
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        while True:
            try:
                fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
                break
            except:
                pass
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("del fitness" + str(self.myID) +".txt")        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[0,3,1] , size=[1,1,1])
        pyrosim.End()
    
    def getEverything(self):
        while self.currentPartCount < self.totalPartNum:
            ###### First Block ######
            if self.currentPartCount == 0:
                spine_size = np.array([np.maximum(0.3,np.random.random_sample()) * c.maxWidth, np.maximum(0.3,np.random.random_sample()) * c.maxLength, np.maximum(0.3,np.random.random_sample()) * c.maxHeight])
                spine_pos = np.array([0, 0, 1])
                spine_name = "spine" + str(self.spineID)
                # pyrosim.Send_Cube(name= spine_name, pos= spine_pos , size= spine_size)
                self.everything.append([spine_name, spine_pos, spine_size, "cube"])
                self.sensors.append(spine_name)
                self.currentPartCount += 1
                # if self.currentPartCount == self.totalPartNum:
                #     break

                ##### ARMS #####
                if self.currentPartCount == self.totalPartNum:
                    left_arm_joint = np.array([0, -(spine_size[1] / 2), spine_pos[2]])
                    right_arm_joint = np.array([0, (spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_leftArm"] = ["arm", "left", self.spineID, spine_size, left_arm_joint]
                    self.totalPartsToAdd += 1
                    self.partsToAdd[spine_name + "_rightArm"] = ["arm", "right", self.spineID, spine_size, right_arm_joint]
                    self.totalPartsToAdd += 1
                    break

                armChoice = np.random.randint(low=0, high=4, size = 1)[0]
                ## NO ARMS ##
                if armChoice == 0:
                    left_arm_joint = np.array([0, -(spine_size[1] / 2), spine_pos[2]])
                    right_arm_joint = np.array([0, (spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_leftArm"] = ["arm", "left", self.spineID, spine_size, left_arm_joint]
                    self.totalPartsToAdd += 1
                    self.partsToAdd[spine_name + "_rightArm"] = ["arm", "right", self.spineID, spine_size, right_arm_joint]
                    self.totalPartsToAdd += 1
                    self.spineID += 1
                # ONLY LEFT ARM ##
                elif armChoice == 1:
                    # if we are creating a left arm, then we must add right arm to partsToAdd
                    right_arm_joint = np.array([0, (spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_rightArm"] = ["arm", "right", self.spineID, spine_size, right_arm_joint]
                    self.totalPartsToAdd += 1
                    joint_pos = np.array([0, -(spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, -arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break
                    # ADD LEG #
                    if not self.addLegs(arm_size, "left"):
                        break
                    self.armID += 1
                    self.spineID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break
                    
                ## ONLY RIGHT ARM ##
                elif armChoice == 2:
                    left_arm_joint = np.array([0, -(spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_leftArm"] = ["arm", "left", self.spineID, spine_size, left_arm_joint]
                    self.totalPartsToAdd += 1
                    joint_pos = np.array([0, (spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break
                    # ADD LEG #
                    if not self.addLegs(arm_size, "right"):
                        break
                    self.spineID += 1
                    self.armID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break
                ## LEFT AND RIGHT ARM ##
                else:
                    # LEFT ARM #
                    joint_pos = np.array([0, -(spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, -arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break
                    # ADD LEFT LEG #
                    if not self.addLegs(arm_size, "left"):
                        break
                    self.armID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break
                    
                    # RIGHT ARM #
                    joint_pos = np.array([0, (spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    self.spineID += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break 
                    
                   # ADD RIGHT LEG #
                    if not self.addLegs(arm_size, "right"):
                        break
                    self.armID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break

            ######### Second block ##########
            else:
                # check if its first spine joint
                if self.spineID == 1:
                    # if first one, use absolute joint position
                    joint_pos = np.array([- (spine_size[0] / 2), 0, spine_pos[2]])
                else:
                    # if not, use relative joint position
                    joint_pos = np.array([- (spine_size[0]), 0, spine_pos[2]])
                joint_name = "spine" + str(self.spineID - 1) + "_spine" + str(self.spineID)
                parent_name = "spine" + str(self.spineID - 1)
                child_name = "spine" + str(self.spineID)
                # pyrosim.Send_Joint( name = joint_name , parent= parent_name , child = child_name, type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                self.everything.append([joint_name, parent_name, child_name, joint_pos, "joint"])
                self.motors.append(joint_name)

                spine_size = np.array([np.maximum(0.3,np.random.random_sample()) * c.maxWidth, np.maximum(0.3,np.random.random_sample()) * c.maxLength, np.maximum(0.3,np.random.random_sample()) * c.maxHeight])
                spine_pos = np.array([-(spine_size[0] / 2), 0, 0])
                spine_name = "spine" + str(self.spineID)
                # pyrosim.Send_Cube(name= spine_name, pos= spine_pos , size= spine_size)
                self.everything.append([spine_name, spine_pos, spine_size, "cube"])
                self.sensors.append(spine_name)
                self.currentPartCount += 1
                # if self.currentPartCount == self.totalPartNum:
                #     break
                
                ##### ARMS #####
                if self.currentPartCount == self.totalPartNum:
                    left_arm_joint = np.array([-(spine_size[0] / 2), -(spine_size[1] / 2), spine_pos[2]])
                    right_arm_joint = np.array([-(spine_size[0] / 2), (spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_leftArm"] = ["arm", "left", self.spineID, spine_size, left_arm_joint]
                    self.totalPartsToAdd += 1
                    self.partsToAdd[spine_name + "_rightArm"] = ["arm", "right", self.spineID, spine_size, right_arm_joint]
                    self.totalPartsToAdd += 1
                    break
                armChoice = np.random.randint(low=0, high=4, size = 1)[0]
                ## NO ARMS ##
                if armChoice == 0:
                    left_arm_joint = np.array([-(spine_size[0] / 2), -(spine_size[1] / 2), spine_pos[2]])
                    right_arm_joint = np.array([-(spine_size[0] / 2), (spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_leftArm"] = ["arm", "left", self.spineID, spine_size, left_arm_joint]
                    self.totalPartsToAdd += 1
                    self.partsToAdd[spine_name + "_rightArm"] = ["arm", "right", self.spineID, spine_size, right_arm_joint]
                    self.totalPartsToAdd += 1
                    self.spineID += 1
                # ONLY LEFT ARM ##
                elif armChoice == 1:
                    right_arm_joint = np.array([-(spine_size[0] / 2), (spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_rightArm"] = ["arm", "right", self.spineID, spine_size, right_arm_joint]
                    self.totalPartsToAdd += 1
                    joint_pos = np.array([-(spine_size[0] / 2), -(spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, -arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break
                    # ADD LEG #
                    if not self.addLegs(arm_size, "left"):
                        self.armID += 1
                        break
                    self.armID += 1
                    self.spineID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break
                    
                ## ONLY RIGHT ARM ##
                elif armChoice == 2:
                    left_arm_joint = np.array([-(spine_size[0] / 2), -(spine_size[1] / 2), spine_pos[2]])
                    self.partsToAdd[spine_name + "_leftArm"] = ["arm", "left", self.spineID, spine_size, left_arm_joint]
                    self.totalPartsToAdd += 1
                    joint_pos = np.array([-(spine_size[0] / 2), (spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break
                    # ADD LEG #
                    if not self.addLegs(arm_size, "right"):
                        self.armID += 1
                        break
                    self.spineID += 1
                    self.armID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break
                ## LEFT AND RIGHT ARM ##
                else:
                    # LEFT ARM #
                    joint_pos = np.array([-(spine_size[0] / 2), -(spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, -arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break
                    # ADD LEFT LEG #
                    if not self.addLegs(arm_size, "left"):
                        break
                    self.armID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break
                    
                    # RIGHT ARM #
                    joint_pos = np.array([-(spine_size[0] / 2), (spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                    # pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                    self.everything.append([joint_name, spine_name, "arm" + str(self.armID), joint_pos, "joint"])
                    self.motors.append(joint_name)
                    arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * spine_size[0], np.maximum(0.3,np.random.random_sample()) * spine_size[1], np.maximum(0.3,np.random.random_sample()) * spine_size[2]])
                    arm_pos = np.array([0, arm_size[1] / 2, 0])
                    arm_name = "arm" + str(self.armID)
                    # pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                    self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                    self.sensors.append(arm_name)
                    self.currentPartCount += 1
                    self.spineID += 1
                    # if self.currentPartCount == self.totalPartNum:
                    #     break 
                    
                   # ADD RIGHT LEG #
                    if not self.addLegs(arm_size, "right"):
                        self.armID += 1
                        break
                    self.armID += 1
                    if self.currentPartCount == self.totalPartNum:
                        break

    def addLegs(self, arm_size, side):
        if side == "left":
            joint_pos = np.array([0, -(arm_size[1]), 0])
        else:
            joint_pos = np.array([0, (arm_size[1]), 0])

        if self.currentPartCount == self.totalPartNum:
            arm_name = "arm" + str(self.armID)
            self.partsToAdd[arm_name + "_lowerLeg"] = ["leg", "lowerLeg", self.armID, arm_size, joint_pos]
            self.totalPartsToAdd += 1
            self.partsToAdd[arm_name + "_upperLeg"] = ["leg", "upperLeg", self.armID, arm_size, joint_pos]
            self.totalPartsToAdd += 1
            return False

        legChoice = np.random.randint(low=0, high=3, size = 1)[0]

        if legChoice == 0:
            arm_name = "arm" + str(self.armID)
            self.partsToAdd[arm_name + "_lowerLeg"] = ["leg", "lowerLeg", self.armID, arm_size, joint_pos]
            self.totalPartsToAdd += 1
            self.partsToAdd[arm_name + "_upperLeg"] = ["leg", "upperLeg", self.armID, arm_size, joint_pos]
            self.totalPartsToAdd += 1
            return True
        else:
            leg_size = np.array([np.maximum(0.75,np.random.random_sample()) * arm_size[0], np.maximum(0.75,np.random.random_sample()) * arm_size[1], np.maximum(0.1,np.random.random_sample()) * c.maxHeight])
            if legChoice == 1:
                arm_name = "arm" + str(self.armID)
                self.partsToAdd[arm_name + "_upperLeg"] = ["leg", "upper", self.armID, arm_size, joint_pos]
                leg_pos = np.array([0, 0, -(leg_size[2] / 2)])
                self.totalPartsToAdd += 1
            else:
                arm_name = "arm" + str(self.armID)
                self.partsToAdd[arm_name + "_lowerLeg"] = ["leg", "lower", self.armID, arm_size, joint_pos]
                leg_pos = np.array([0, 0, (leg_size[2] / 2)])
                self.totalPartsToAdd += 1
            joint_name = "arm" + str(self.armID) + "_leg" + str(self.legID)
            parent_name = "arm" + str(self.armID)
            child_name = "leg" + str(self.legID)
            # pyrosim.Send_Joint( name = joint_name , parent= parent_name , child = child_name, type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
            self.everything.append([joint_name, parent_name, child_name, joint_pos, "joint"])
            self.motors.append(joint_name)
            
            leg_name = "leg" + str(self.legID)
            # pyrosim.Send_Cube(name= leg_name, pos= leg_pos , size= leg_size)
            self.everything.append([leg_name, leg_pos, leg_size, "cube"])
            self.sensors.append(leg_name)
            self.legID += 1
            self.currentPartCount += 1
            return True
            

    def Generate_Body(self):
        pyrosim.Start_URDF(f"body{self.myID}.nndf")
        for part in self.everything:
            if part[-1] == 'joint':
                pyrosim.Send_Joint( name = part[0] , parent= part[1] , child = part[2], type = "revolute", position = part[3].tolist(), jointAxis = "0 1 0")
            else:
                pyrosim.Send_Cube(name= part[0], pos= part[1] , size= part[2])
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        #### FIX THIS PART ####
        
        name = 0
        for sensor in self.sensors:
            pyrosim.Send_Sensor_Neuron(name = name , linkName = sensor)
            name += 1

        for motor in self.motors:
            pyrosim.Send_Motor_Neuron( name = name , jointName = motor)
            name += 1
        
        for currentRow in range(len(self.sensors)):
            for currentColumn in range(len(self.motors)):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + len(self.sensors), weight = self.weights[currentRow, currentColumn])
        
        pyrosim.End()

    def Mutate(self): 
        mutateChoice = np.random.randint(low=0, high=2, size = 1)[0]
        
        if mutateChoice == 0:
            print("changing synapse")
            # simply change one of the synapse
            randomRow = random.randint(0, len(self.sensors) - 1)
            randomColumn = random.randint(0, len(self.motors) - 1)
            self.weights[randomRow,randomColumn] = (random.random() * 2) - 1
        else:
            # add another part
            new_row = (np.random.rand(1, self.weights.shape[1]) * 2) - 1
            self.weights = np.vstack([self.weights, new_row])
            new_col = (np.random.rand(self.weights.shape[0], 1) * 2) - 1
            self.weights = np.hstack([self.weights, new_col])

            partToAdd, detail = random.choice(list(self.partsToAdd.items()))        
            if detail[0] == 'leg':
                print("adding leg")
                leg_size = np.array([np.maximum(0.75,np.random.random_sample()) * detail[3][0], np.maximum(0.75,np.random.random_sample()) * detail[3][1], np.maximum(0.1,np.random.random_sample()) * c.maxHeight])
                if detail[1] == 'upper':
                    leg_pos = np.array([0, 0, (leg_size[2] / 2)])
                else:
                    leg_pos = np.array([0, 0, -(leg_size[2] / 2)])
                
                joint_name = "arm" + str(detail[2]) + "_leg" + str(self.legID)
                parent_name = "arm" + str(detail[2])
                child_name = "leg" + str(self.legID)
                self.everything.append([joint_name, parent_name, child_name, detail[4], "joint"])
                self.motors.append(joint_name)
                leg_name = "leg" + str(self.legID)
                self.everything.append([leg_name, leg_pos, leg_size, "cube"])
                self.sensors.append(leg_name)
                self.legID += 1
                del self.partsToAdd[partToAdd]
            elif detail[0] == 'arm':
                print("adding arm")
                arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * detail[3][0], np.maximum(0.3,np.random.random_sample()) * detail[3][1], np.maximum(0.3,np.random.random_sample()) *  detail[3][2]])
                if detail[1] == 'left':
                    arm_pos = np.array([0, -arm_size[1] / 2, 0])
                else:
                    arm_pos = np.array([0, arm_size[1] / 2, 0])
                
                joint_name = "spine" + str(detail[2]) + "_arm" + str(self.armID)
                parent_name = "spine" + str(detail[2])
                child_name = "arm" + str(self.armID)

                self.everything.append([joint_name, parent_name, child_name, detail[4], "joint"])
                self.motors.append(joint_name)
                arm_name = "arm" + str(self.armID)
                self.everything.append([arm_name, arm_pos, arm_size, "cube"])
                self.sensors.append(arm_name)
                # add legs to partsToAdd

                # self.partsToAdd[arm_name + "_lowerLeg"] = ["leg", "lowerLeg", self.armID, arm_size, joint_pos]
                # self.totalPartsToAdd += 1
                # self.partsToAdd[arm_name + "_upperLeg"] = ["leg", "upperLeg", self.armID, arm_size, joint_pos]
                # self.totalPartsToAdd += 1

                self.armID += 1
                del self.partsToAdd[partToAdd]
        

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID