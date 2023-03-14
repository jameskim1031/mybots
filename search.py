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

    # if not os.path.exists("pickles"):
    #     os.mkdir("pickles")
    # with open(f"pickles/my_file{i}.pickle", "wb") as f:
    #     pickle.dump(phc, f)

# Plotting Fitness
for i in range(c.numOfSeeds):
    plt.plot(fitness_curves[i], label='Random Seed ' + str(i))
plt.title('Highest fitness vs Generations for 10 Random Seeds')
plt.xlabel("Number of Generations")
plt.ylabel("Highest fitness of robot in Population")
plt.legend(loc = "upper left")
plt.show()