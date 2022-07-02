from .Neighborhood import SwapNeighborhood, InsertionNeighborhood, BlockNeighborhoodK3, TwoEdgeExchangeNeighborhood
from .InputData import InputData
from .Solution import Solution
from .EvaluationLogic import EvaluationLogic
from .SolutionPool import SolutionPool
from copy import deepcopy
from datetime import datetime, timedelta

""" Base class for several types of improvement algorithms. """ 
class ImprovementAlgorithm:
    def __init__(self, inputData: InputData, neighborhoodEvaluationStrategy = 'BestImprovement', neighborhoodTypes = ['Swap']):
        self.InputData = inputData

        self.EvaluationLogic = {}
        self.SolutionPool = {}
        self.RNG = {}

        self.NeighborhoodEvaluationStrategy = neighborhoodEvaluationStrategy
        self.NeighborhoodTypes = neighborhoodTypes
        self.Neighborhoods = {}

    def Initialize(self, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool, rng = None) -> None:
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool
        self.RNG = rng

    """ Similar to the so-called factory concept in software design. """
    def CreateNeighborhood(self, neighborhoodType: str, bestCurrentSolution: Solution) -> None:
        if neighborhoodType == 'Swap':
            return SwapNeighborhood(self.InputData, bestCurrentSolution.allocation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'Insertion':
            return InsertionNeighborhood(self.InputData, bestCurrentSolution.allocation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'BlockK3':
            return BlockNeighborhoodK3(self.InputData, bestCurrentSolution.allocation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'TwoEdgeExchange':
            return TwoEdgeExchangeNeighborhood(self.InputData, bestCurrentSolution.allocation, self.EvaluationLogic, self.SolutionPool)
        else:
            raise Exception(f"Neighborhood type {neighborhoodType} not defined.")

    def InitializeNeighborhoods(self, solution: Solution) -> None:
        for neighborhoodType in self.NeighborhoodTypes:
            neighborhood = self.CreateNeighborhood(neighborhoodType, solution)
            self.Neighborhoods[neighborhoodType] = neighborhood

""" Iterative improvement algorithm through sequential variable neighborhood descent. """
class IterativeImprovement(ImprovementAlgorithm):
    def __init__(self, inputData: InputData, neighborhoodEvaluationStrategy = 'BestImprovement', neighborhoodTypes = ['Swap']):
        super().__init__(inputData, neighborhoodEvaluationStrategy, neighborhoodTypes)

    def Run(self, solution: Solution) -> Solution:
        self.InitializeNeighborhoods(solution)    

        # According to "Hansen et al. (2017): Variable neighorhood search", this is equivalent to the 
        # sequential variable neighborhood descent with a pipe neighborhood change step.
        for neighborhoodType in self.NeighborhoodTypes:
            neighborhood = self.Neighborhoods[neighborhoodType]
            neighborhood.LocalSearch(self.NeighborhoodEvaluationStrategy, solution)
        
        return solution

class TabuSearch(ImprovementAlgorithm):
    def __init__(self, inputData: InputData, maxSeconds: int, neighborhoodEvaluationStrategy = 'BestImprovement', neighborhoodTypes = ['Swap']):
        super().__init__(inputData, neighborhoodEvaluationStrategy, neighborhoodTypes)
        self.TabuList = []
        self.MaxSeconds = maxSeconds

    def aspirationskriterium(self, solution: Solution, bestSolution: Solution) -> bool:
        return solution.profit > bestSolution.profit

    def Run(self, initialSolution: Solution) -> Solution:
        start = datetime.now()
        currentSolution = initialSolution
        bestSolution = self.SolutionPool.GetHighestProfitSolution()
        while datetime.now() <= start + timedelta(seconds = self.MaxSeconds):
            iterative = IterativeImprovement(self.InputData, self.NeighborhoodEvaluationStrategy, self.NeighborhoodTypes)
            iterative.Initialize(self.EvaluationLogic, self.SolutionPool)
            currentSolution = iterative.Run(bestSolution)
            if currentSolution not in self.TabuList:
                self.TabuList.append(deepcopy(currentSolution))
                if currentSolution.profit > bestSolution.profit or self.aspirationskriterium(currentSolution, bestSolution):
                    bestSolution = currentSolution

        return bestSolution