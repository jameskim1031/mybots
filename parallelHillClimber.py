from solution import SOLUTION
import copy
import constants as c
import os

class PARALLEL_HILL_CLIMBER:
    # We'll start by assigning a unique ID to each solution. Create a variable called self.nextAvailableID in PARALLEL_HILL_CLIMBER's constructor and set it to zero.
    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        

    # Back in PHC's Evolve() function, comment out the reference to the second for loop, but leave the self....Wait_For... uncommented. This should deactivate our parallelism in Evolve() now: it now starts the simulation of the first parent, then waits for that simulation to end. Then, it starts the simulation of the second simulation, and so on.
    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    
    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.Evaluate(self.children)

        self.Print()

        self.Select()

    # At the end of Spawn(), print each entry in self.children and then exit() immediately. Run search.py; you should see two SOLUTION's printed.
    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
        
    def Mutate(self):
        for i in self.children.keys():
            self.children[i].Mutate()
    
    # Uncomment and modify PHC's self.Select() to compete each child against its parent. If it wins, it should replace its parent in self.parents.
    def Select(self):
        for i in self.parents:
            if self.parents[i].fitness > self.children[i].fitness:
                self.parents[i] = self.children[i]

    # Modify Print() to iterate through the keys in self.parents, and print the fitness of self.parents[key] and then the fitness of self.children[key] on the same line.
    def Print(self):
        print("")
        for i in self.parents.keys():
            print(["parent fitness:", self.parents[i].fitness, "child fitness:", self.children[i].fitness])
        print("")
    # Include an exit() right after this call to Evaluate(), and print fitness in SOLUTION's Get_Fitness... again.
    def Evaluate(self, solutions):
        for solution in solutions.values():
            solution.Start_Simulation("DIRECT")

        for solution in solutions.values():
            solution.Wait_For_Simulation_To_End()

    # Finally, modify PHC's Show_Best() method to find the parent with the lowest fitness, and re-simulate that one with the graphics turned on. Note that we only need to use SOLUTION's Start_Simulation("GUI"); we do not to use Wait_For_... because we already have the fitness of this solution.
    def Show_Best(self):
        all_solution = self.parents.items()
        lowest_fitness = min(all_solution, key=lambda x: x[1].fitness)
        lowest_parent = lowest_fitness[1]
        lowest_parent.Start_Simulation("GUI")
        # largest_fitness = max(all_solution, key=lambda x: x[1].fitness)
        # largest_parent = largest_fitness[1]
        # largest_parent.Start_Simulation("GUI")