import pyrosim.pyrosim as pyrosim
import numpy
import constants as c

class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.length)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if t == c.length - 1:
            numpy.save("./data/" + self.linkName + ".npy",self.values)
            print(self.values)