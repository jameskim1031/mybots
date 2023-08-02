# algorithm for negative x direction
def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        initial_pos = np.array([2,0, c.maxHeight / 2])
        initial_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
        temp_joint = np.array([2 - (initial_size[0] / 2), 0, initial_pos[2]])
        
        pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist(), size=initial_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')            
        for i in range(c.bodyNum):
            temp_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
            temp_pos = np.array([-(temp_size[0] / 2), 0, 0])
            pyrosim.Send_Joint( name = "Body" + str(i) + "_Body" + str(i + 1) , parent= "Body" + str(i) , child = "Body" + str(i + 1), type = "revolute", position = temp_joint.tolist(), jointAxis = "0 1 0")
            if i in self.sensors:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            else:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
            temp_joint = np.array([-(temp_size[0]), 0, 0])
        pyrosim.End()


# algorithm for positive x direction
def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        initial_pos = np.array([0,0, c.maxHeight / 2])
        initial_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
        temp_joint = np.array([(initial_size[0] / 2), 0, initial_pos[2]])
        
        if 0 in self.sensors:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist(), size=initial_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        else:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist() , size=initial_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
        for i in range(c.bodyNum):
            temp_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
            temp_pos = np.array([(temp_size[0] / 2), 0, 0])
            pyrosim.Send_Joint( name = "Body" + str(i) + "_Body" + str(i + 1) , parent= "Body" + str(i) , child = "Body" + str(i + 1), type = "revolute", position = temp_joint.tolist(), jointAxis = "0 1 0")
            if i in self.sensors:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            else:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
            temp_joint = np.array([(temp_size[0]), 0, 0])
        pyrosim.End()

# algorithm for positive y direction
def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        initial_pos = np.array([0,0, c.maxHeight / 2])
        initial_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
        temp_joint = np.array([0, (initial_size[1] / 2), initial_pos[2]])
        
        if 0 in self.sensors:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist(), size=initial_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        else:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist() , size=initial_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
        for i in range(c.bodyNum):
            temp_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
            temp_pos = np.array([0, (temp_size[1] / 2), 0])
            pyrosim.Send_Joint( name = "Body" + str(i) + "_Body" + str(i + 1) , parent= "Body" + str(i) , child = "Body" + str(i + 1), type = "revolute", position = temp_joint.tolist(), jointAxis = "0 1 0")
            if i in self.sensors:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            else:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
            temp_joint = np.array([0, (temp_size[1]), 0])
        pyrosim.End()

# algorithm for positive z direction
def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        initial_pos = np.array([0,0, c.maxHeight / 2])
        initial_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
        temp_joint = np.array([0, 0, c.maxHeight / 2 + (initial_size[2] / 2)])
        
        if 0 in self.sensors:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist(), size=initial_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
        else:
            pyrosim.Send_Cube(name="Body0", pos=initial_pos.tolist() , size=initial_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
        for i in range(c.bodyNum):
            temp_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
            temp_pos = np.array([0, 0, (temp_size[2] / 2)])
            pyrosim.Send_Joint( name = "Body" + str(i) + "_Body" + str(i + 1) , parent= "Body" + str(i) , child = "Body" + str(i + 1), type = "revolute", position = temp_joint.tolist(), jointAxis = "0 1 0")
            if i in self.sensors:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
            else:
                pyrosim.Send_Cube(name="Body" + str(i + 1), pos=temp_pos.tolist() , size=temp_size.tolist(), color_string= '    <color rgba="0 0.0 1.0 1.0"/>', color_name='Blue')
            temp_joint = np.array([0, 0, (temp_size[2])])
        pyrosim.End()


# # choose whether we want 0, 1 or 2 arms
# randomization = np.random.randint(low=0, high=3, size = 1)[0]
# #TESTING
# randomization = 1
# if randomization == 1:
#     # choose left arm or right arm
#     left = np.random.randint(low=0, high=2, size = 1)[0]
#     if left:
#         # calculate joint position
#         left_arm_joint = np.array([-(temp_size[0] / 2), -(temp_size[1] / 2), 0])
#         # create random block
#         arm_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
#         # find position of arm
#         arm_pos = np.array([0, -(arm_size[1] / 2), 0])
#         # append to the joint
#         pyrosim.Send_Cube(name="Body" + str(i + 1), pos=arm_pos.tolist() , size=arm_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
#     else: # right arm
#         # calculate joint position
#         right_arm_joint = np.array([-(temp_size[0] / 2), (temp_size[1] / 2), 0])
#         # create random block
#         arm_size = np.array([np.random.random_sample() * c.maxWidth, np.random.random_sample() * c.maxLength, np.random.random_sample() * c.maxHeight])
#         # find position of arm
#         arm_pos = np.array([0, -(arm_size[1] / 2), 0])
#         # append to the joint
#         pyrosim.Send_Cube(name="Body" + str(i + 1), pos=arm_pos.tolist() , size=arm_size.tolist(), color_string= '    <color rgba="0 1.0 0.0 1.0"/>', color_name='Green')
# elif randomization == 2:
#     make_left_arm()
#     make_right_arm()