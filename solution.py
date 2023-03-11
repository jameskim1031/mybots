import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.chooseSensors = np.random.randint(low=0, high=c.bodyNum, size = 1)[0]
        self.chosenSensors = np.random.choice(c.bodyNum + 1, self.chooseSensors, replace=False)
        self.totalPartNum = 3
        self.currentPartCount = 0
        self.spineID = 0
        self.armID = 0
        self.legID = 0
        self.everything = []
        self.sensors = []
        self.motors = []
        
    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Body()
        self.Generate_Brain()
        os.system("start /B python simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("del fitness" + str(self.myID) +".txt")        

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[0,3,1] , size=[1,1,1])
        pyrosim.End()
    
    def Generate_Body(self):
        self.currentPartCount = 0
        self.spineID = 0
        self.armID = 0
        self.legID = 0
        self.everything = []
        self.sensors = []
        self.motors = []
        pyrosim.Start_URDF(f"body{self.myID}.nndf")

        while self.currentPartCount < self.totalPartNum:
            # create spine
            if self.currentPartCount == 0:
                spine_size = np.array([np.maximum(0.3,np.random.random_sample()) * c.maxWidth, np.maximum(0.3,np.random.random_sample()) * c.maxLength, np.maximum(0.3,np.random.random_sample()) * c.maxHeight])
                spine_pos = np.array([2, 0, c.maxHeight / 2])
                spine_name = "spine" + str(self.spineID)
                pyrosim.Send_Cube(name= "spine" + str(self.spineID), pos= spine_pos , size= spine_size)
                self.everything.append([spine_name, spine_pos, spine_size])
                self.sensors.append(spine_name)
                self.currentPartCount += 1
                if self.currentPartCount == self.totalPartNum:
                    break
                # create arm
                if self.currentPartCount == 1:
                    joint_pos = np.array([2, -(spine_size[1] / 2), spine_pos[2]])
                    joint_name = spine_name + "_arm" + str(self.armID)
                pyrosim.Send_Joint( name = joint_name , parent= spine_name , child = "arm" + str(self.armID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                self.everything.append([joint_name, joint_pos])
                self.motors.append(joint_name)
                arm_size = np.array([np.maximum(0.3,np.random.random_sample()) * c.maxWidth, np.maximum(0.3,np.random.random_sample()) * c.maxLength, np.maximum(0.3,np.random.random_sample()) * c.maxHeight])
                arm_pos = np.array([0, -arm_size[1] / 2, 0])
                arm_name = "arm" + str(self.armID)
                pyrosim.Send_Cube(name= arm_name, pos= arm_pos , size= arm_size)
                self.everything.append([arm_name, arm_pos, arm_size])
                self.sensors.append(arm_name)
                self.currentPartCount += 1
                self.spineID += 1
                if self.currentPartCount == self.totalPartNum:
                    break
            else:
                joint_name = "spine" + str(self.spineID - 1) + "_spine" + str(self.spineID)
                joint_pos = np.array([spine_pos[0] - (spine_size[0] / 2), 0, spine_pos[2]])
                pyrosim.Send_Joint( name = joint_name , parent= "spine" + str(self.spineID - 1) , child = "spine" + str(self.spineID), type = "revolute", position = joint_pos.tolist(), jointAxis = "0 1 0")
                self.everything.append([joint_name, joint_pos])
                self.motors.append(joint_name)

                spine_size = np.array([np.maximum(0.3,np.random.random_sample()) * c.maxWidth, np.maximum(0.3,np.random.random_sample()) * c.maxLength, np.maximum(0.3,np.random.random_sample()) * c.maxHeight])
                spine_pos = np.array([-(spine_size[0] / 2), 0, 0])
                spine_name = "spine" + str(self.spineID)
                pyrosim.Send_Cube(name= "spine" + str(self.spineID), pos= spine_pos , size= spine_size)
                self.everything.append([spine_name, spine_pos, spine_size])
                self.sensors.append(spine_name)
                self.currentPartCount += 1
                if self.currentPartCount == self.totalPartNum:
                    break
            
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        name = 0
        for sensor in self.sensors:
            pyrosim.Send_Sensor_Neuron(name = name , linkName = sensor)
            name += 1

        for motor in self.motors:
            pyrosim.Send_Motor_Neuron( name = name , jointName = motor)
            name += 1
        
        for currentRow in range(len(self.sensors)):
            for currentColumn in range(len(self.motors)):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + len(self.sensors), weight = (np.random.rand(1)[0] * 2) - 1)
        print("brainny")
        print(self.sensors)
        print(self.motors)
        
        pyrosim.End()

    def Mutate(self):
        print("mutate")
        randomRow = random.randint(0, len(self.sensors) - 1)
        randomColumn = random.randint(0, len(self.motors) - 1)
        #self.weights[randomRow,randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID