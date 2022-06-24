from .InputData import InputData
from .ConstructiveHeuristic import ConstructiveHeuristics
from .ImprovementAlgorithm import ImprovementAlgorithm
from .EvaluationLogic import EvaluationLogic
from .SolutionPool import SolutionPool
from .Solution import Solution

import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

class Solver:
    def __init__(self, inputData: InputData, seed: int):
        self.InputData = inputData
        self.Seed = seed
        self.RNG = numpy.random.default_rng(self.Seed)
        self.EvaluationLogic = EvaluationLogic(inputData)
        self.SolutionPool = SolutionPool()
        
        self.ConstructiveHeuristic = ConstructiveHeuristics(self.EvaluationLogic, self.SolutionPool)      

    def Initialize(self) -> None:
        self.OptimizationAlgorithm.Initialize(self.EvaluationLogic, self.SolutionPool, self.RNG)
    
    def ConstructionPhase(self, constructiveSolutionMethod: str) -> Solution:
        self.ConstructiveHeuristic.Run(self.InputData, constructiveSolutionMethod)

        bestInitalSolution = self.SolutionPool.GetLowestProfitSolution()

        print("Constructive solution found.")
        print(bestInitalSolution)

        return bestInitalSolution

    def ImprovementPhase(self, startSolution: Solution, algorithm: ImprovementAlgorithm) -> None:
        algorithm.Initialize(self.EvaluationLogic, self.SolutionPool, self.RNG)
        bestSolution = algorithm.Run(startSolution)

        print("Best found Solution.")
        print(bestSolution)

    def RunLocalSearch(self, constructiveSolutionMethod: str, algorithm: ImprovementAlgorithm) -> None:
        startSolution = self.ConstructionPhase(constructiveSolutionMethod)

        self.ImprovementPhase(startSolution, algorithm)

    def EvalPFSP(self, individual: list) -> list:
        solution = Solution(individual)
        self.EvaluationLogic.calcProfit(solution)
        return [solution.profit]
