import pickle
import parallelHillClimber

# SELECT THE SEED NUMBER
parent_number = 2
generation_number = 499

with open(f"pickles/parent{parent_number}generation{generation_number}.pickle", "rb") as file:
    # Use the pickle.load() method to load the object from file
    parent = pickle.load(file)
parent.Start_Simulation("GUI")