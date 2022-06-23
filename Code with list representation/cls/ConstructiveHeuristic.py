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
        emptyAllocation = [-1] * inputData.NumItems
        sortedItems = sorted(inputData.InputItems, key = lambda item: item.Profit/item.Weight, reverse = True)
        sortedKnapsacks = sorted(inputData.InputKnapsacks, key = lambda knap: knap.Penalty, reverse = True)
        for item in sortedItems:
            for knapsack in sortedKnapsacks:
                currentWeight = sum() # TODO

    def Run(self, inputData: InputData, solutionMethod: str) -> None:
        print('Generating an initial solution according to ' + solutionMethod + '.')

        solution = None 
        
        if solutionMethod == 'greedy':
            valid, solution = self.greedyAllocation(inputData.NumItems)
        else:
            print('Unkown constructive solution method: ' + solutionMethod + '.')

        if valid:
            self.SolutionPool.AddSolution(solution)
