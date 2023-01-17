import numpy
import matplotlib.pyplot

# backLegSensorValues = numpy.load("./data/backLegSensorValues.npy")
# frontLegSensorValues = numpy.load("./data/frontLegSensorValues.npy")
BackLeg = numpy.load("./data/BackLeg.npy")
FrontLeg = numpy.load("./data/FrontLeg.npy")
Torso = numpy.load("./data/Torso.npy")

BackLegMotor = numpy.load("./data/motorb'Torso_BackLeg'.npy")
FrontLegMotor = numpy.load("./data/motorb'Torso_FrontLeg'.npy")
# matplotlib.pyplot.plot(backLegSensorValues, linewidth=3)
# matplotlib.pyplot.plot(frontLegSensorValues)
# matplotlib.pyplot.legend(["back leg", "front leg"])
# matplotlib.pyplot.plot(BackLeg)
matplotlib.pyplot.plot(BackLegMotor)
matplotlib.pyplot.plot(FrontLegMotor)
matplotlib.pyplot.show()