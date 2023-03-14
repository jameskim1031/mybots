import pickle
import parallelHillClimber

# SELECT THE SEED NUMBER
parent_number = 0
generation_number = 4

with open(f"pickles/parent{parent_number}generation{generation_number}.pickle", "rb") as file:
    # Use the pickle.load() method to load the object from file
    parent = pickle.load(file)
parent.Start_Simulation("GUI")