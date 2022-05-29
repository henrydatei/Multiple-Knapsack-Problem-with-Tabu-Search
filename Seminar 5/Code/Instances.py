import os
import random
import re

class TestInstance:

    def __init__(self, path):
        self.path = path
        self.nJobs, self.nMachines, self.Jobs = self.ReadTextFile()

    def ReadTextFile(self):

        with open(self.path, "r") as newFile:

            content = newFile.readlines()
        
        content = [x.strip() for x in content]

        nJobs, nMachines = content[0].split("  ")
        nJobs, nMachines = int(nJobs), int(nMachines)

        tmpList = []

        content.pop(0)

        for jobLine in content:
            newTmpList = re.findall("\S+", jobLine)
            tmpList.append([int(element) for element in newTmpList])
        
        return nJobs, nMachines, tmpList
    
    def ExtendData(self):

        for job in self.Jobs:
            for m in range(self.nMachines):
                job.insert(m+1+2*m, random.randint(int(0.1*job[m+1+2*m]), int(0.5*job[m+1+2*m])))

            processTime = sum([job[s] for s in range(1, len(job), 3)]) + sum([job[s] for s in range(2, len(job), 3)])
            job.append(random.randint(int(processTime*0.8), int(processTime*1.4)))
            job.append(random.randint(5,20)*10)

    def WriteData(self, newpath):
        
        tmpFileName = self.path[59:-7] + "SIST.txt"

        with open(os.path.join(newpath,tmpFileName), "w") as newFile:
             newFile.write("%s %s \n" % (self.nJobs, self.nMachines))

             for job in self.Jobs:
                for element in job:
                    newFile.write("%s " % element)
                newFile.write("\n")

if __name__ == "__main__":

    path = "/Users/benedikt/Downloads/InstancesAndBounds/VRF_Instances"

    storage = "/Users/benedikt/Documents/002 - Arbeit TU Dresden/104 - Lehre/Aktuelle Themen des Industriellen Management/HeuristicDesignCourse/TestInstances"

    for folder in os.listdir(path):
        
        if folder in ["Small", "Large"]:

            extendedPath = os.path.join(path,folder)
            print(extendedPath)
            for file in os.listdir(extendedPath):

                if file.endswith(".txt"):
                    print(os.path.join(extendedPath, file))
                    instance = TestInstance(os.path.join(extendedPath, file))

                    instance.ReadTextFile()

                    instance.ExtendData()

                    instance.WriteData(storage)



