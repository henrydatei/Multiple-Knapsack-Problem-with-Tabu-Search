import numpy
from .Solution import Solution
from .EvaluationLogic import EvaluationLogic
from .SolutionPool import SolutionPool
from .InputData import InputData

from typing import Tuple

class ConstructiveHeuristics:
    def __init__(self, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool):
        self.RandomSeed = 2021
        self.RandomRetries = 10
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool

    def greedyAllocation(self, inputData: InputData) -> Tuple[bool, Solution]:
        allocation = [-1] * inputData.NumItems
        sortedItems = sorted(inputData.InputItems, key = lambda item: item.Profit/item.Weight, reverse = True)
        sortedKnapsacks = sorted(inputData.InputKnapsacks, key = lambda knap: knap.Penalty, reverse = True)
        for item in sortedItems:
            for knapsack in sortedKnapsacks:
                itemIDs = [i for i, x in enumerate(allocation) if x == knapsack.Id]
                items = [inputData.findItemByID(itemID) for itemID in itemIDs]
                currentWeight = sum([item.Weight for item in items])
                #print(item, knapsack, items, currentWeight)
                if currentWeight + item.Weight <= knapsack.Capacity:
                    allocation[item.Id] = knapsack.Id
                    break
        sol = Solution(allocation)
        valid = self.EvaluationLogic.calcProfit(sol)
        return valid, sol

    def Run(self, inputData: InputData, solutionMethod: str) -> None:
        print('Generating an initial solution according to ' + solutionMethod + '.')

        solution = None 
        
        if solutionMethod == 'greedy':
            valid, solution = self.greedyAllocation(inputData)
        else:
            print('Unkown constructive solution method: ' + solutionMethod + '.')

        if valid:
            self.SolutionPool.AddSolution(solution)
