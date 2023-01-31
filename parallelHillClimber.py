from solution import SOLUTION
import copy
import constants as c

class PARALLEL_HILL_CLIMBER:
    # We'll start by assigning a unique ID to each solution. Create a variable called self.nextAvailableID in PARALLEL_HILL_CLIMBER's constructor and set it to zero.
    def __init__(self):
        self.nextAvailableID = 0
        self.parent = {}
        for i in range(c.populationSize):
            self.parent[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        

    # Modify PHC's Evolve() function to evaluate each of the parents, one after the other, using a for loop. Leave the for loop that iterates over generations commented out for now.
    def Evolve(self):
        for solution in self.parent.values():
            solution.Evaluate("GUI")
        # self.parent.Evaluate("GUI")
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.child.Evaluate("DIRECT")

        self.Print()

        self.Select()
    
    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID()
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()
    

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Print(self):
        print([self.parent.fitness, self.child.fitness])

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass