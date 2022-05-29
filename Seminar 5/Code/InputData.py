import json

class DataMachine:

    def __init__(self, machineId):
        self.__machId = machineId

    def __str__(self):
        result = "Machine " + str(self.__machId)

        return result
        
    @property
    def MachineId(self):
        return self.__machId

class DataJob:
    
    def __init__(self, idJob, processingTimes, setupTimes, dueDate, tardinessCost):
        self.__jobId = idJob
        self.__processingTimes = processingTimes
        self.__dueDate = dueDate
        self.__setupTimes = setupTimes
        self.__tardCost = tardinessCost
        
    def __str__(self):
        result = f"Job {self.__jobId} with {len(self.__processingTimes)} Operations:\n"

        for opId, processingTime in enumerate(self.__processingTimes):
            result += f"Operation {opId} with Processingtime: {processingTime} \n"

        return result
    
    @property
    def JobId(self):
        return self.__jobId

    @property
    def TardCost(self):
        return self.__tardCost
        
    @property
    def DueDate(self):
        return self.__dueDate

    @property
    def Operations(self):
        return [(opId, processingTime) for opId, processingTime in enumerate(self.__processingTimes)]
    
    def SetupTime(self, position):
        return self.__setupTimes[position]

    def ProcessingTime(self, position):
        return self.__processingTimes[position]

class InputData:

    def __init__(self, path):
        self.__path = path
        self.__totalProcessingTime = None
        self.DataLoad()

    def DataLoad(self):

        with open(self.__path, "r") as inputFile:
            inputData = json.load(inputFile)
        
        self.n = inputData['nJobs']
        self.m = inputData['nMachines']
        
        self.InputJobs = list()
        self.InputMachines = list()

        for job in inputData['Jobs']:
            self.InputJobs.append(DataJob(job['Id'], job['ProcessingTimes'], job["SetupTimes"], job['DueDate'], job['TardCosts']))
        
        for k in range(self.m):
            self.InputMachines.append(DataMachine(k))

        self.__totalProcessingTime = sum(x.ProcessingTime(i) for x in self.InputJobs for i in range(len(x.Operations)))

    @property
    def TotalProcessingTime(self):
        return self.__totalProcessingTime