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
        

    # Back in PHC's Evolve() function, comment out the reference to the second for loop, but leave the self....Wait_For... uncommented. This should deactivate our parallelism in Evolve() now: it now starts the simulation of the first parent, then waits for that simulation to end. Then, it starts the simulation of the second simulation, and so on.
    def Evolve(self):
        for solution in self.parent.values():
            solution.Start_Simulation("GUI")
        for solution in self.parent.values():
            solution.Wait_For_Simulation_To_End()
        #     print(solution.fitness)
        
        # self.parent.Evaluate("GUI")
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()

        self.Mutate()

        self.child.Evaluate("GUI")

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