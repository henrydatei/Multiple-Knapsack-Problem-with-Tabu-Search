from .Solution import Solution
from .InputData import InputData
from .EvaluationLogic import EvalutationLogic
import random

class Solver:
    seed: int
    path: str
    inputdata: InputData
    solutionPool: list

    def __init__(self, path, seed = 42) -> None:
        self.seed = seed
        self.path = path
        self.inputdata = InputData(path)
        self.solutionPool = []
        random.seed(seed)

    def __repr__(self) -> str:
        return f"Solver({self.seed = }, {self.path = }, {self.inputdata = }, {self.solutionPool = })"

    def greedyAllocation(self) -> None:
        solution = [[] for i in range(self.inputdata.numKnapsacks)]
        sortedItems = sorted(self.inputdata.items, key = lambda item: item.profit/item.weight, reverse = True)
        for item in sortedItems:
            for knapsack in self.inputdata.knapsacks:
                currentWeight = sum([self.inputdata.items[itemID].weight for itemID in solution[knapsack.id]])
                if currentWeight + item.weight <= knapsack.capacity:
                    solution[knapsack.id].append(item.id)
                    break
        
        return solution

    def generateNeighboorhood(self, initialSolution, type = "swap", maxIterations = 100):
        if type == "swap":
            iteration = 0
            while iteration < maxIterations:
                liste = random.sample(self.inputdata.knapsacks, 2)
                knapsackA = liste[0]
                knapsackB = liste[1]
                contentA = initialSolution.allocation[knapsackA.id]
                contentB = initialSolution.allocation[knapsackB.id]
                if len(contentA) == 0 or len(contentB) == 0:
                    continue
                itemA = random.sample(contentA, 1)[0]
                itemB = random.sample(contentB, 1)[0]
                try:
                    newAllocation = initialSolution.allocation
                    newAllocation[knapsackA.id].remove(itemA)
                    newAllocation[knapsackB.id].remove(itemB)
                    newAllocation[knapsackA.id].append(itemB)
                    newAllocation[knapsackB.id].append(itemA)
                    sol = Solution(newAllocation)
                    EvalutationLogic(self.inputdata).calcProfit(sol)
                    self.solutionPool.append(sol)
                except:
                    pass
                iteration = iteration + 1
        elif type == "insert":
            iteration = 0
            while iteration < maxIterations:
                liste = random.sample(self.inputdata.knapsacks, 2)
                knapsackA = liste[0]
                knapsackB = liste[1]
                print(knapsackA, knapsackB)
                contentA = initialSolution.allocation[knapsackA.id]
                print(contentA)
                if len(contentA) == 0:
                    continue
                itemA = random.sample(contentA, 1)[0]
                try:
                    newAllocation = initialSolution.allocation
                    newAllocation[knapsackA.id].remove(itemA)
                    newAllocation[knapsackB.id].append(itemA)
                    print(newAllocation)
                    sol = Solution(newAllocation)
                    EvalutationLogic(self.inputdata).calcProfit(sol)
                    self.solutionPool.append(sol)
                except:
                    pass
                iteration = iteration + 1