class SolutionPool:
    def __init__(self):
        self.Solutions = []

    def AddSolution(self, newSolution):
        self.Solutions.append(newSolution)

    def GetLowestProfitSolution(self):
        self.Solutions.sort(key = lambda solution: solution.profit)

        return self.Solutions[0]