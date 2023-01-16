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
            print(self.values)

# backLegSensorValues = numpy.zeros(c.length)
# frontLegSensorValues = numpy.zeros(c.length)