import numpy
import matplotlib.pyplot

# backLegSensorValues = numpy.load("./data/backLegSensorValues.npy")
# frontLegSensorValues = numpy.load("./data/frontLegSensorValues.npy")
BackLegTargetAngles = numpy.load("./data/BackLegTargetAngles.npy")
FrontLegTargetAngles = numpy.load("./data/FrontLegTargetAngles.npy")
# matplotlib.pyplot.plot(backLegSensorValues, linewidth=3)
# matplotlib.pyplot.plot(frontLegSensorValues)
# matplotlib.pyplot.legend(["back leg", "front leg"])
matplotlib.pyplot.plot(BackLegTargetAngles)
matplotlib.pyplot.plot(FrontLegTargetAngles)
matplotlib.pyplot.show()