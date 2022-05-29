import os
import random
import re

class TestInstanceSDST:

    def __init__(self, path):
        self.path = path
        self.nJobs, self.nMachines, self.Jobs = self.ReadTextFile()
        self.setuptimes = self.ExtendData()

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

        tmpSetupList = []
        for m in range(self.nMachines):
            tmpSetupList.append([])
            for i in range(self.nJobs + 1):
                tmpSetupList[m].append([])
                for j in range(self.nJobs + 1):
                    if i == j or j == 0:
                        tmpSetupList[m][i].append(0)
                    else:
                        tmpSetupList[m][i].append(random.randint(25,50))
        
        for m in range(len(tmpSetupList)):
            for i in range(len(tmpSetupList[m])):
                for j in range(1, len(tmpSetupList[m][i])):
                    if j != i:
                        for k in range(1, len(tmpSetupList)):
                            if k != i and k != j:
                                while tmpSetupList[m][i][j] > tmpSetupList[m][i][k] + tmpSetupList[m][k][j]:
                                    print("Invalid!")
                                    tmpSetupList[m][i][j] = random.randint(25, tmpSetupList[m][i][k]+tmpSetupList[m][k][j])
        tmpNewSetupList = []

        for j in range(self.nJobs + 1):
            tmpNewSetupList.append([])
            for m in range(self.nMachines):
                tmpNewSetupList[j].append(tmpSetupList[m][j])

        return tmpNewSetupList

            

    def WriteData(self, newpath):
        
        tmpFileName = self.path[65:-7] + "SDST.txt"

        with open(os.path.join(newpath,tmpFileName), "w") as newFile:
            newFile.write("%s %s \n" % (self.nJobs, self.nMachines))

            for job in self.Jobs:
                for element in job:
                    newFile.write("%s " % element)
                newFile.write("\n")
            
            for j in range(len(self.setuptimes)):
                newFile.write("%s \n" % str(j-1))

                for m in range(len(self.setuptimes[j])):
                    for element in self.setuptimes[j][m]:
                        newFile.write("%s " % element)
                    newFile.write("\n")



path = "/Users/benedikt/Downloads/InstancesAndBounds/VRF_Instances/Small/VFR10_5_1_Gap.txt"
path2 = "/Users/benedikt/Desktop"

instance = TestInstanceSDST(path)

instance.WriteData(path2)

print(len(instance.setuptimes))

for i in range(-1, 5):
    print(i)

'''
if __name__ == "__main__":

    path = "/Users/benedikt/Downloads/InstancesAndBounds/VRF_Instances"

    storage = "/Users/benedikt/Documents/002 - Arbeit TU Dresden/104 - Lehre/Aktuelle Themen des Industriellen Management/HeuristicDesignCourse/TestInstances"

    for folder in os.listdir(path):
        
        if folder in ["Small", "Large"]:

            extendedPath = os.path.join(path,folder)
            print(extendedPath)
            for file in os.listdir(extendedPath):

                if file.endswith("_20_1_Gap.txt"):
                    print(os.path.join(extendedPath, file))
                    instance = TestInstance(os.path.join(extendedPath, file))

                    #instance.ReadTextFile()

                    instance.ExtendData()

                    #instance.WriteData(storage)'''



