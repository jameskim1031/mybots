class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, joint):
        if not self.head:
            self.head = joint
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = joint
        self.size += 1

    def insert(self, jointID, new_joint):
        if jointID < 0 or jointID > self.size:
            print("Invalid index")
            return
        if jointID == 0:
            new_joint.next = self.head
            self.head = new_joint
        else:
            curr = self.head
            for i in range(jointID-1):
                curr = curr.next
            new_joint.next = curr.next
            curr.next = new_joint
        self.size += 1

    def increment_all_joints(self):
        curr = self.head
        while curr:
            curr.body_position += 1
            curr.joint_position += 1
            curr = curr.next
    
    def Generate_Body_Using_LinkedList(self):
        current_joint = self.head
        while current_joint is not None:
            pyrosim.Send_Joint( name = "Body" + str(current_joint.parentJoint) +  "Body" + str(current_joint.currentJoint), parent= "Body" + str(current_joint.parentJoint) , child = "Body" + str(current_joint.currentJoint), type = "revolute", position = joint_position, jointAxis = "0 1 0")
            self.jointList.append([parent, sensor_count])

            name = "Body" + str(current_joint.currentJoint)
            pos = current_joint.body_position
            size = current_joint.body_size
            color_string = '<color rgba="0 1.0 0.0 1.0"/>'
            color_name = 'Green'
            pyrosim.Send_Cube(name="Body" + str(current_joint.currentJoint), pos=current_joint.body_position, size=current_joint.body_size, color_string='<color rgba="0 1.0 0.0 1.0"/>', color_name='Green')

            current_joint = current_joint.next