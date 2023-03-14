from solution import SOLUTION
import copy
import constants as c
import os
import numpy as np
import pickle


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.fitnessCurves = np.zeros(c.numberOfGenerations)
        self.mutationProcess = []

    def getBest(self, currentGeneration):
        highest_fitness = float('-inf')
        print("self.parents.items")
        print(self.parents.items())
        for i, parent in self.parents.items():
            if currentGeneration in [0, c.numberOfGenerations / 2, c.numberOfGenerations - 1]:
                if not os.path.exists("pickles"):
                    os.mkdir("pickles")
                with open(f"pickles/parent{i}generation{currentGeneration}.pickle", "wb") as f:
                    pickle.dump(parent, f)

            if parent.fitness > highest_fitness:
                highest_fitness = parent.fitness
                best_parent = parent
        self.fitnessCurves[currentGeneration] = highest_fitness
        self.mutationProcess.append(best_parent.thingsWeMutated)

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()
            self.getBest(currentGeneration)

    
    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)

        self.Print()

        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
        
    def Mutate(self):
        for i in self.children.keys():
            self.children[i].Mutate()
    
    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]

    
    def Print(self):
        print("")
        for i in self.parents.keys():
            print(["parent fitness:", self.parents[i].fitness, "child fitness:", self.children[i].fitness])
        print("")
    
    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation("DIRECT")

        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

    
    def Show_Best(self):
        all_solution = self.parents.items()
        highest_fitness = max(all_solution, key=lambda x: x[1].fitness)
        lowest_parent = highest_fitness[1]
        lowest_parent.Start_Simulation("GUI")
        