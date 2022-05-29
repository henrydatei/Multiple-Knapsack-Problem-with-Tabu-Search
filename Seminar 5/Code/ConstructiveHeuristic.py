from itertools import permutations
import time
import numpy
from OutputData import Solution
import EvaluationLogic

class ConstructiveHeuristics:
    def __init__(self, evaluationLogic, solutionPool):
        self.RandomSeed = 2021
        self.RandomRetries = 10
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool

    def ROS(self, jobList, x, seed):
        numpy.random.seed(seed)
        tmpSolution = Solution(jobList,0)
        bestCmax = numpy.inf

        for i in range(x):
            tmpPermutation = numpy.random.permutation(len(jobList))
            # initialize Solution            
            tmpSolution.Permutation = tmpPermutation

            self.EvaluationLogic.DefineStartEnd(tmpSolution)

            if(tmpSolution.Makespan < bestCmax):
                bestCmax = tmpSolution.Makespan
                bestPermutation = tmpPermutation

        bestRandomSolution = Solution(jobList, bestPermutation)
        self.EvaluationLogic.DefineStartEnd(bestRandomSolution)

        return bestRandomSolution

    def CheckAllPermutations(self, jobList):
        allPerms = set(permutations(range(len(jobList))))
        bestCmax = numpy.inf
        tmpSolution = Solution(jobList,0)

        for tmpPerm in allPerms:
            tmpSolution.SetPermutation(tmpPerm)
            self.EvaluationLogic.DefineStartEnd(tmpSolution)  

            if(tmpSolution.Makespan < bestCmax):
                bestCmax = tmpSolution.Makespan
                bestPerm = tmpPerm

        bestSol = Solution(jobList,bestPerm)
        self.EvaluationLogic.DefineStartEnd(bestSol)

        return bestSol 

    def FirstComeFirstServe(self, jobList):
        tmpPermutation = [*range(len(jobList))]

        tmpSolution = Solution(jobList, tmpPermutation)
        self.EvaluationLogic.DefineStartEnd(tmpSolution)

        return tmpSolution

    def ShortestProcessingTime(self, jobList, allMachines = False):
        jobPool = []

        for i in range(len(jobList)):
            if(allMachines):
                jobPool.append((i,sum(jobList[i].ProcessingTime(x) for x in range(len(jobList[i].Operations)))))
            else: 
                jobPool.append((i,jobList[i].ProcessingTime(0)))

        jobPool.sort(key=lambda x: x[1])

        tmpPermutation = [x[0] for x in jobPool]
        tmpSolution = Solution(jobList, tmpPermutation)

        self.EvaluationLogic.DefineStartEnd(tmpSolution)

        return tmpSolution    

    def LongestProcessingTime(self, jobList, allMachines = False):
        jobPool = []    

        for i in range(len(jobList)):
            if(allMachines):
                jobPool.append((i,sum(jobList[i].ProcessingTime(x) for x in range(len(jobList[i].Operations)))))
            else: 
                jobPool.append((i,jobList[i].ProcessingTime(0)))

        jobPool.sort(key=lambda x: x[1], reverse=True)

        tmpPermutation = [x[0] for x in jobPool]
        tmpSolution = Solution(jobList, tmpPermutation)

        self.EvaluationLogic.DefineStartEnd(tmpSolution)

        return tmpSolution   

    def NEH(self, jobList):
        jobPool = []
        tmpPerm = []
        # Calculate sum of processing times and sort
        for i in range(len(jobList)):
            jobPool.append((i,sum(jobList[i].ProcessingTime(x) for x in range(len(jobList[i].Operations)))))
        jobPool.sort(key=lambda x: x[1], reverse=True)

        # Initalize input
        tmpNEHOrder = [x[0] for x in jobPool]
        tmpPerm.append(tmpNEHOrder[0])
        tmpSolution = Solution(jobList,tmpPerm)

        # Add next jobs in a loop and check all permutations
        for i in range(1,len(tmpNEHOrder)):
            # add next job to end and calculate makespan
            
            if len(tmpPerm) > 1:
                self.EvaluationLogic.DetermineBestInsertionAccelerated(tmpSolution, tmpNEHOrder[i])
                # self.EvaluationLogic.DetermineMakespanInsertion(tmpSolution, tmpNEHOrder[i])
            else:
                self.EvaluationLogic.DetermineBestInsertion(tmpSolution, tmpNEHOrder[i])
        
        return tmpSolution

    def Run(self, inputData, solutionMethod):
        print('Generating an initial solution according to ' + solutionMethod + '.')

        solution = None 
        
        if solutionMethod == 'FCFS':
            solution = self.FirstComeFirstServe(inputData.InputJobs)
        elif solutionMethod == 'SPT':
            solution = self.ShortestProcessingTime(inputData.InputJobs)
        elif solutionMethod == 'LPT':
            solution = self.LongestProcessingTime(inputData.InputJobs)
        elif solutionMethod == 'ROS':
            solution = self.ROS(inputData.InputJobs, self.RandomRetries, self.RandomSeed)
        elif solutionMethod == 'NEH':
            solution = self.NEH(inputData.InputJobs)
        else:
            print('Unkown constructive solution method: ' + solutionMethod + '.')

        self.SolutionPool.AddSolution(solution)
