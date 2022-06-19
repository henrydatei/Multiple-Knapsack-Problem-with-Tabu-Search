from copy import deepcopy
from .TabuEntry import TabuEntry
from .Solution import Solution
from .InputData import InputData
import random
import math

class Solver:
    seed: int
    path: str
    inputdata: InputData
    solutionPool: list[Solution]
    tabuList: list

    def __init__(self, path, seed = 42) -> None:
        self.seed = seed
        self.path = path
        self.inputdata = InputData(path)
        self.solutionPool = []
        self.tabuList = []
        random.seed(seed)

    def __repr__(self) -> str:
        return f"Solver({self.seed = }, {self.path = }, {self.inputdata = }, {self.solutionPool = })"

    def greedyAllocation(self) -> None:
        solution = [[] for i in range(self.inputdata.numKnapsacks)]
        sortedItems = sorted(self.inputdata.items, key = lambda item: item.profit/item.weight, reverse = True)
        sortedKnapsacks = sorted(self.inputdata.knapsacks, key = lambda knap: knap.penalty, reverse = True)
        for item in sortedItems:
            for knapsack in sortedKnapsacks:
                currentWeight = sum([self.inputdata.items[itemID].weight for itemID in solution[knapsack.id]])
                if currentWeight + item.weight <= knapsack.capacity:
                    solution[knapsack.id].append(item.id)
                    break
        
        return Solution(self.inputdata, solution)

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
                newAllocation = list(initialSolution.allocation)
                newAllocation[knapsackA.id].remove(itemA)
                newAllocation[knapsackB.id].remove(itemB)
                newAllocation[knapsackA.id].append(itemB)
                newAllocation[knapsackB.id].append(itemA)
                sol = Solution(self.inputdata, newAllocation)
                if sol.calcProfit():
                    self.solutionPool.append(deepcopy(sol))
                iteration = iteration + 1
        elif type == "insert":
            iteration = 0
            while iteration < maxIterations:
                liste = random.sample(self.inputdata.knapsacks, 2)
                knapsackA = liste[0]
                knapsackB = liste[1]
                #print(knapsackA, knapsackB)
                contentA = initialSolution.allocation[knapsackA.id]
                #print(contentA)
                if len(contentA) == 0:
                    continue
                itemA = random.sample(contentA, 1)[0]
                newAllocation = list(initialSolution.allocation)
                newAllocation[knapsackA.id].remove(itemA)
                newAllocation[knapsackB.id].append(itemA)
                #print(newAllocation)
                sol = Solution(self.inputdata, newAllocation)
                if sol.calcProfit():
                    #print(sol.profit, sol.allocation)
                    self.solutionPool.append(deepcopy(sol))
                iteration = iteration + 1
    
    def getBestSolutionFromSolutionPool(self):
        return sorted(self.solutionPool, key = lambda sol: sol.profit, reverse = True)[0]

    def updateTabuList(self):
        toRemove = []
        for idx, tabuEntry in enumerate(self.tabuList):
            tabuEntry.update()
            if tabuEntry.time_remaining <= 0:
                toRemove.append(idx)
        for idx in toRemove[::-1]:
            del self.tabuList[idx]

    def aspirationskriterium(self, sol):
        return False

    def tabuSearch(self, initialSolution, maxIterationsTabuSearch = 10, maxIterationsNeighboorhood = 10000, tabuTime = 3):
        bestSol = deepcopy(initialSolution)
        for iteration in range(maxIterationsTabuSearch):
            print(f"Tabu-Search, Iteration {iteration}")
            self.generateNeighboorhood(deepcopy(bestSol), "insert", math.floor(maxIterationsNeighboorhood/2))
            if len(self.solutionPool) == 0:
                self.generateNeighboorhood(deepcopy(bestSol), "swap", math.ceil(maxIterationsNeighboorhood/2))
            else:
                self.generateNeighboorhood(deepcopy(self.getBestSolutionFromSolutionPool()), "swap", math.ceil(maxIterationsNeighboorhood/2))

            if len(self.solutionPool) > 0:
                currentBestSol = deepcopy(self.getBestSolutionFromSolutionPool())
                if currentBestSol not in [tabuentry.solution for tabuentry in self.tabuList] and currentBestSol.profit > bestSol.profit:
                    bestSol = deepcopy(currentBestSol)
                elif self.aspirationskriterium(deepcopy(currentBestSol)) and currentBestSol.profit > bestSol.profit:
                    bestSol = deepcopy(currentBestSol)

                self.updateTabuList()
                self.tabuList.append(deepcopy(TabuEntry(currentBestSol, tabuTime)))
                
                print(f"\t - Lösung {bestSol.allocation} mit Profit {bestSol.profit}")
            else:
                print(f"\t - keine Lösung in diesem Durchgang gefunden")

        return bestSol
