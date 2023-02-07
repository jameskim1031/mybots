import pyrosim.pyrosim as pyrosim
import numpy as np
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(13,12)
        self.weights = self.weights * 2 - 1

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
        pyrosim.Send_Cube(name="Box", pos=[-2,0,1] , size=[8,1.1,2])
        pyrosim.End()
    
    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,2.6] , size=[1,1,0.5])

        pyrosim.Send_Joint( name = "Torso_LeftLeg1" , parent= "Torso" , child = "LeftLeg1" , type = "revolute", position = [0.5,0.25,2.6], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg1", pos=[0.25,0,0] , size=[0.5,0.2,0.2])

        pyrosim.Send_Joint( name = "LeftLeg1_LeftLowerLeg1" , parent= "LeftLeg1" , child = "LeftLowerLeg1" , type = "revolute", position = [0.5,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg1", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])

        pyrosim.Send_Joint( name = "Torso_LeftLeg2" , parent= "Torso" , child = "LeftLeg2" , type = "revolute", position = [0.5,-0.25,2.6], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg2", pos=[0.25,0,0] , size=[0.5,0.2,0.2])

        pyrosim.Send_Joint( name = "LeftLeg2_LeftLowerLeg2" , parent= "LeftLeg2" , child = "LeftLowerLeg2" , type = "revolute", position = [0.5,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg2", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])

        pyrosim.Send_Joint( name = "Torso_RightLeg1" , parent= "Torso" , child = "RightLeg1" , type = "revolute", position = [-0.5,0.25,2.6], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg1", pos=[-0.25,0,0] , size=[0.5,0.2,0.2])

        pyrosim.Send_Joint( name = "RightLeg1_RightLowerLeg1" , parent= "RightLeg1" , child = "RightLowerLeg1" , type = "revolute", position = [-0.5,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg1", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])

        pyrosim.Send_Joint( name = "Torso_RightLeg2" , parent= "Torso" , child = "RightLeg2" , type = "revolute", position = [-0.5,-0.25,2.6], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg2", pos=[-0.25,0,0] , size=[0.5,0.2,0.2])

        pyrosim.Send_Joint( name = "RightLeg2_RightLowerLeg2" , parent= "RightLeg2" , child = "RightLowerLeg2" , type = "revolute", position = [-0.5,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg2", pos=[0,0,-0.25] , size=[0.2,0.2,0.5])

        pyrosim.Send_Joint( name = "Torso_SideArm1" , parent= "Torso" , child = "SideArm1" , type = "revolute", position = [0,-0.5,2.6], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="SideArm1", pos=[0,-0.1,0] , size=[0.2,0.2,0.2])

        pyrosim.Send_Joint( name = "SideArm1_SideLowerArm1" , parent= "SideArm1" , child = "SideLowerArm1" , type = "revolute", position = [0,-0.2,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="SideLowerArm1", pos=[0,0,-0.4] , size=[0.2,0.2,0.8])

        pyrosim.Send_Joint( name = "Torso_SideArm2" , parent= "Torso" , child = "SideArm2" , type = "revolute", position = [0,0.5,2.6], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="SideArm2", pos=[0,0.1,0] , size=[0.2,0.2,0.2])

        pyrosim.Send_Joint( name = "SideArm2_SideLowerArm2" , parent= "SideArm2" , child = "SideLowerArm2" , type = "revolute", position = [0,0.2,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="SideLowerArm2", pos=[0,0,-0.4] , size=[0.2,0.2,0.8])

        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "LeftLeg1")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "LeftLowerLeg1")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg2")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "LeftLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "RightLeg1")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "RightLowerLeg1")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "RightLeg2")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 9 , linkName = "SideArm1")
        pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "SideLowerArm1")
        pyrosim.Send_Sensor_Neuron(name = 11 , linkName = "SideArm2")
        pyrosim.Send_Sensor_Neuron(name = 12 , linkName = "SideLowerArm2")

        
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "Torso_LeftLeg1")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "LeftLeg1_LeftLowerLeg1")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "Torso_LeftLeg2")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "LeftLeg2_LeftLowerLeg2")
        pyrosim.Send_Motor_Neuron( name = 17 , jointName = "Torso_RightLeg1")
        pyrosim.Send_Motor_Neuron( name = 18 , jointName = "RightLeg1_RightLowerLeg1")
        pyrosim.Send_Motor_Neuron( name = 19 , jointName = "Torso_RightLeg2")
        pyrosim.Send_Motor_Neuron( name = 20 , jointName = "RightLeg2_RightLowerLeg2")
        pyrosim.Send_Motor_Neuron( name = 21 , jointName = "Torso_SideArm1")
        pyrosim.Send_Motor_Neuron( name = 22 , jointName = "SideArm1_SideLowerArm1")
        pyrosim.Send_Motor_Neuron( name = 23 , jointName = "SideArm2_SideLowerArm2")
        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow,randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID