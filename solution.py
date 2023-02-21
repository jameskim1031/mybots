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
        self.numMotors = 0
        self.numSensors = 0
        self.chooseSensors = np.random.randint(low=0, high=c.bodyNum, size = 1)[0]
        self.chosenSensors = np.random.choice(c.bodyNum + 1, self.chooseSensors, replace=False)
        
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
        pyrosim.Start_URDF("body.urdf")
        initial_pos = np.array([2,0, c.maxHeight / 2])
        initial_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
        temp_joint = np.array([2 - (initial_size[0] / 2), 0, initial_pos[2]])
        motor_count = 0
        sensor_count = 0
        
        if 0 in self.chosenSensors:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist(), size=initial_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        else:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist() , size=initial_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
        sensor_count += 1
        for i in range(c.bodyNum):
            temp_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
            temp_pos = np.array([-(temp_size[0] / 2), 0, 0])
            pyrosim.Send_Joint( name = "Body" + str(motor_count) + "_Body" + str(motor_count + 1) , parent= "Body" + str(motor_count) , child = "Body" + str(motor_count + 1), type = "revolute", position = temp_joint.tolist(), jointAxis = "0 1 0")
            motor_count += 1
            if i in self.chosenSensors:
                pyrosim.Send_Cube(name="Body" + str(sensor_count), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            else:
                pyrosim.Send_Cube(name="Body" + str(sensor_count), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
            sensor_count += 1

            # choose whether we want 0, 1 or 2 arms
            randomization = np.random.randint(low=0, high=3, size = 1)[0]
            if randomization == 0:
                temp_joint = np.array([-(temp_size[0]), 0, 0])
            elif randomization == 1:
                #choose left or right and add arm
                left = np.random.randint(low=0, high=2, size = 1)[0]
                # get a new random block
                arm_size = np.array([np.random.random_sample() * temp_size[0] / 2, np.random.random_sample() * c.maxLength, np.random.random_sample() * temp_size[2]])
                # find new joint position
                # find arm position
                if left:
                    arm_joint = np.array([-(temp_size[0] / 2), -(temp_size[1] / 2), 0])
                    arm_position = np.array([0,-(arm_size[1]) / 2, 0])
                    temp_joint = np.array([-(temp_size[0]) / 2, (temp_size[1]) / 2, 0])
                else:
                    arm_joint = np.array([-(temp_size[0] / 2), (temp_size[1] / 2), 0])
                    arm_position = np.array([0,(arm_size[1]) / 2, 0])
                    temp_joint = np.array([-(temp_size[0]) / 2, -(temp_size[1]) / 2, 0])
                pyrosim.Send_Joint( name = "Body" + str(motor_count) + "_Body" + str(motor_count + 1) , parent= "Body" + str(motor_count) , child = "Body" + str(motor_count + 1), type = "revolute", position = arm_joint.tolist(), jointAxis = "0 1 0")
                motor_count += 1
                blue = np.random.randint(low=0, high=2, size = 1)[0]
                if blue:
                    pyrosim.Send_Cube(name="Body" + str(sensor_count), pos=arm_position.tolist() , size=arm_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
                else:
                    pyrosim.Send_Cube(name="Body" + str(sensor_count), pos=arm_position.tolist() , size=arm_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
                sensor_count += 1
                # # check if up and down
                # leg = np.random.randint(low=0, high=3, size = 1)[0]
                # if leg == 0:
                #     pass
                # elif leg == 1:
                #     # add leg down
                #     leg_joint = np.array([0, (arm_size[1]), 0])
                #     leg_size = np.array([arm_size[0], (arm_size[1]) / 2, 0])
                # else:
                #     pass

            else:
                #left arm
                left_arm_size = np.array([np.random.random_sample() * temp_size[0] / 2, np.random.random_sample() * c.maxLength, np.random.random_sample() * temp_size[2]])
                left_arm_joint = np.array([-(temp_size[0] / 2), -(temp_size[1] / 2), 0])
                left_arm_position = np.array([0,-(left_arm_size[1]) / 2, 0])
                pyrosim.Send_Joint( name = "Body" + str(motor_count) + "_Body" + str(motor_count + 1) , parent= "Body" + str(motor_count) , child = "Body" + str(motor_count + 1), type = "revolute", position = left_arm_joint.tolist(), jointAxis = "0 1 0")
                motor_count += 1
                blue = np.random.randint(low=0, high=2, size = 1)[0]
                if blue:
                    pyrosim.Send_Cube(name="Body" + str(sensor_count), pos= left_arm_position.tolist() , size=left_arm_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
                else:
                    pyrosim.Send_Cube(name="Body" + str(sensor_count), pos= left_arm_position.tolist() , size=left_arm_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
                sensor_count += 1
                #right arm
                right_arm_size = np.array([np.random.random_sample() * temp_size[0] / 2, np.random.random_sample() * c.maxLength, np.random.random_sample() * temp_size[2]])
                right_arm_joint = np.array([0, (temp_size[1]), 0])
                right_arm_position = np.array([0,(right_arm_size[1]) / 2, 0])
                temp_joint = np.array([-(temp_size[0]) / 2, -(temp_size[1]) / 2, 0])
                pyrosim.Send_Joint( name = "Body" + str(motor_count) + "_Body" + str(motor_count + 1) , parent= "Body" + str(motor_count) , child = "Body" + str(motor_count + 1), type = "revolute", position = right_arm_joint.tolist(), jointAxis = "0 1 0")
                motor_count += 1
                blue = np.random.randint(low=0, high=2, size = 1)[0]
                if blue:
                    pyrosim.Send_Cube(name="Body" + str(sensor_count), pos= right_arm_position.tolist() , size=right_arm_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
                else:
                    pyrosim.Send_Cube(name="Body" + str(sensor_count), pos= right_arm_position.tolist() , size=right_arm_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
                sensor_count += 1

        self.numMotors = motor_count
        self.numSensors = sensor_count
        pyrosim.End()


    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        for i in range(self.numSensors):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = "Body" + str(i))
        # pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Body1")
        # pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "Body2")
        # pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "Body3")

        for i in range(self.numMotors):
            pyrosim.Send_Motor_Neuron( name = self.numSensors + i , jointName = "Body" + str(i) +"_Body" + str(i + 1))
        # pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Body0_Body1")
        # pyrosim.Send_Motor_Neuron( name = 5 , jointName = "Body1_Body2")
        # pyrosim.Send_Motor_Neuron( name = 6 , jointName = "Body2_Body3")
        
        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numMotors):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn + self.numSensors, weight = (np.random.rand(1)[0] * 2) - 1)
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, self.numSensors - 1)
        randomColumn = random.randint(0, self.numMotors - 1)
        #self.weights[randomRow,randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID