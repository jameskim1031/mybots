import os
from hillclimber import HILL_CLIMBER
from parallelHillClimber import PARALLEL_HILL_CLIMBER

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()

# for _ in range(5):
#     os.system("python generate.py")
#     os.system("python simulate.py")

# Note that search.py uses parallel hillclimber's constructor, and two of its methods. Find these three functions in parallelHillClimber.py, comment out the code that is in them, and add just a pass statement for now.

# start from 67