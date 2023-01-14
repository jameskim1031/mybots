import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load("./data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("./data/frontLegSensorValues.npy")
matplotlib.pyplot.plot(backLegSensorValues, linewidth=3)
matplotlib.pyplot.plot(frontLegSensorValues)
matplotlib.pyplot.legend(["back leg", "front leg"])
matplotlib.pyplot.show()