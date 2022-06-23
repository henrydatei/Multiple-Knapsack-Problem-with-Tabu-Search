from Neighborhood import *
import math
from copy import deepcopy
import numpy

""" Base class for several types of improvement algorithms. """ 
class ImprovementAlgorithm:
    def __init__(self, inputData, neighborhoodEvaluationStrategy = 'BestImprovement', neighborhoodTypes = ['Swap']):
        self.InputData = inputData

        self.EvaluationLogic = {}
        self.SolutionPool = {}
        self.RNG = {}

        self.NeighborhoodEvaluationStrategy = neighborhoodEvaluationStrategy
        self.NeighborhoodTypes = neighborhoodTypes
        self.Neighborhoods = {}

    def Initialize(self, evaluationLogic, solutionPool, rng = None):
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool
        self.RNG = rng

    """ Similar to the so-called factory concept in software design. """
    def CreateNeighborhood(self, neighborhoodType, bestCurrentSolution):
        if neighborhoodType == 'Swap':
            return SwapNeighborhood(self.InputData, bestCurrentSolution.Permutation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'Insertion':
            return InsertionNeighborhood(self.InputData, bestCurrentSolution.Permutation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'BlockK3':
            return BlockNeighborhoodK3(self.InputData, bestCurrentSolution.Permutation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'TaillardInsertion':
            return TaillardInsertionNeighborhood(self.InputData, bestCurrentSolution.Permutation, self.EvaluationLogic, self.SolutionPool)
        elif neighborhoodType == 'TwoEdgeExchange':
            return TwoEdgeExchangeNeighborhood(self.InputData, bestCurrentSolution.Permutation, self.EvaluationLogic, self.SolutionPool)
        else:
            raise Exception(f"Neighborhood type {neighborhoodType} not defined.")

    def InitializeNeighborhoods(self, solution):
        for neighborhoodType in self.NeighborhoodTypes:
            neighborhood = self.CreateNeighborhood(neighborhoodType, solution)
            self.Neighborhoods[neighborhoodType] = neighborhood

""" Iterative improvement algorithm through sequential variable neighborhood descent. """
class IterativeImprovement(ImprovementAlgorithm):
    def __init__(self, inputData, neighborhoodEvaluationStrategy = 'BestImprovement', neighborhoodTypes = ['Swap']):
        super().__init__(inputData, neighborhoodEvaluationStrategy, neighborhoodTypes)

    def Run(self, solution):
        self.InitializeNeighborhoods(solution)    

        # According to "Hansen et al. (2017): Variable neighorhood search", this is equivalent to the 
        # sequential variable neighborhood descent with a pipe neighborhood change step.
        for neighborhoodType in self.NeighborhoodTypes:
            neighborhood = self.Neighborhoods[neighborhoodType]

            neighborhood.LocalSearch(self.NeighborhoodEvaluationStrategy, solution)
        
        return solution

""" Iterated greedy algorithm with destruction and construction. """
class IteratedGreedy(ImprovementAlgorithm):
    def __init__(self, inputData, numberJobsToRemove, baseTemperature, maxIterations, localSearchAlgorithm = None):
        super().__init__(inputData)

        self.NumberJobsToRemove = numberJobsToRemove
        self.BaseTemperature = baseTemperature
        self.MaxIterations = maxIterations

        if localSearchAlgorithm is not None:
            self.LocalSearchAlgorithm = localSearchAlgorithm
        else:
            self.LocalSearchAlgorithm = IterativeImprovement(self.InputData, neighborhoodTypes=[]) # IterativeImprovement without a neighborhood does not modify the solution
    
    def Initialize(self, evaluationLogic, solutionPool, rng):
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool
        self.RNG = rng

        self.LocalSearchAlgorithm.Initialize(self.EvaluationLogic, self.SolutionPool)
    
    def Destruction(self, currentSolution):
        removedJobs = self.RNG.choice(self.InputData.n, size=self.NumberJobsToRemove, replace = False).tolist()

        partialPermutation = [i for i in currentSolution.Permutation if i not in removedJobs]

        return removedJobs, partialPermutation

    def Construction(self, removedJobs, permutation):
        completeSolution = Solution(self.InputData.InputJobs, permutation)
        for i in removedJobs:
            self.EvaluationLogic.DetermineBestInsertionAccelerated(completeSolution, i)

        return completeSolution

    def AcceptWorseSolution(self, currentObjectiveValue, newObjectiveValue):
        randomNumber = self.RNG.random()

        totalProcessingTime = sum(x.ProcessingTime(i) for x in self.InputData.InputJobs for i in range(len(x.Operations)))
        Temperature = self.BaseTemperature * totalProcessingTime / (self.InputData.n * self.InputData.m * 10)
        probability = math.exp(-(newObjectiveValue - currentObjectiveValue) / Temperature)
        
        return randomNumber <= probability

    def Run(self, currentSolution):
        currentSolution = self.LocalSearchAlgorithm.Run(currentSolution)

        currentBest = self.SolutionPool.GetLowestMakespanSolution().Makespan
        iteration = 0
        while(iteration < self.MaxIterations):
            removedJobs, partialPermutation = self.Destruction(currentSolution)
            newSolution = self.Construction(removedJobs, partialPermutation)

            newSolution = self.LocalSearchAlgorithm.Run(newSolution)
            
            if newSolution.Makespan < currentSolution.Makespan:
                currentSolution = newSolution

                if newSolution.Makespan < currentBest:
                    print(f'New best solution in iteration {iteration}: {currentSolution}')
                    self.SolutionPool.AddSolution(currentSolution)
                    currentBest = newSolution.Makespan

            elif self.AcceptWorseSolution(currentSolution.Makespan, newSolution.Makespan):
                currentSolution = newSolution

            iteration += 1

        return self.SolutionPool.GetLowestMakespanSolution()


