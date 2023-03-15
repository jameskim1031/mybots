import os
from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import matplotlib.pyplot as plt
import constants as c
import random


fitness_curves = {}

for i in range(c.numOfSeeds):
    random.seed(i)
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()
    fitness_curves[i] = phc.fitnessCurves
    
# Plotting Fitness
for i in range(c.numOfSeeds):
    plt.plot(fitness_curves[i], label='Random Seed ' + str(i))
plt.title('Highest fitness vs Generations for ' + str(c.numOfSeeds) + ' Random Seeds')
plt.xlabel("Number of Generations")
plt.ylabel("Highest fitness")
plt.legend(loc = "upper left")
plt.show()