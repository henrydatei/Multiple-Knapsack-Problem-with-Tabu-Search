import sys
import csv

from InputData import *

class OutputJob(DataJob):

    def __init__(self, dataJob):
        super().__init__(dataJob.JobId, [dataJob.ProcessingTime(i) for i in range(len(dataJob.Operations))], [dataJob.SetupTime(i) for i in range(len(dataJob.Operations))], dataJob.DueDate, dataJob.TardCost)
        
        self.StartSetups = [0]*len(self.Operations)
        self.EndSetups = [0]*len(self.Operations)        
        self.StartTimes = [0]*len(self.Operations)
        self.EndTimes = [0]*len(self.Operations)
        self.Tardiness = 0

# class OutputMachine(DataMachine):

#     def __init__(self, id_machine, number_of_jobs):
#         super().__init__(id_machine)
#         self.__starttimes = [0]*len(number_of_jobs)
#         self.__endtimes = [0]*len(number_of_jobs)

#     def __str__(self):
#         result = "Machine " + str(self.mach_id)

#         return result
        
#     @property
#     def mach_id(self):
#         return super().MachineId
    
#     @property
#     def starttimes(self):
#         return self.__starttimes
    
#     @starttimes.setter
#     def starttimes(self, id, t):
#         self.__starttimes[id] = t
    
#     @property
#     def endtimes(self):
#         return self.__endtimes
    
#     @endtimes.setter
#     def endtimes(self, id, t):
#         self.__endtimes[id] = t

class Solution:
    def __init__(self, jobList, permutation):
        self.OutputJobs = {}
        for jobId, job in enumerate(jobList):
            self.OutputJobs[jobId] = OutputJob(job)
        self.Permutation = permutation
        self.Makespan = -1
        self.TotalTardiness = -1
        self.TotalWeightedTardiness = -1

    def __str__(self):
        return "The permutation " + str(self.Permutation) + " results in a Makespan of " + str(self.Makespan)

    def SetPermutation(self, permutation):
        self.Permutation = permutation

    def WriteSolToCsv(self, fileName):
        csv_file = open(fileName, "w")
        csv_file.write('Machine,Job,Start_Setup,End_Setup,Start,End\n')
        for job in self.OutputJobs.values():
            for i in range(len(job.EndTimes)):
                csv_file.write(str(i + 1) + "," + str(job.JobId) + "," + str(job.StartSetups[i]) + "," + str(job.EndSetups[i]) + "," + str(job.StartTimes[i]) + "," + str(job.EndTimes[i]) + "\n")

class SolutionPool:
    def __init__(self):
        self.Solutions = []

    def AddSolution(self, newSolution):
        self.Solutions.append(newSolution)

    def GetLowestMakespanSolution(self):
        self.Solutions.sort(key = lambda solution: solution.Makespan) # sort solutions according to makespan

        return self.Solutions[0]
