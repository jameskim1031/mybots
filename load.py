import pickle
import parallelHillClimber

# Select creature_number number:
    # 0 to 9
creature_number = 0

# Select generation number:
    # either 0, 250, or 499
generation_number = 0


## change this path to "testing/" if you want to see your own robot!
with open(f"pickles/parent{creature_number}generation{generation_number}.pickle", "rb") as file:
    # Use the pickle.load() method to load the object from file
    parent = pickle.load(file)
parent.Start_Simulation("GUI")