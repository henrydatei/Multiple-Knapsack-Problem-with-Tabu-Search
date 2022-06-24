import dataclasses
from .Solution import Solution

@dataclasses.dataclass
class SolutionPool:
    Solutions: list = dataclasses.field(init = False, default_factory = list)

    def AddSolution(self, newSolution):
        self.Solutions.append(newSolution)

    def GetLowestProfitSolution(self) -> Solution:
        self.Solutions.sort(key = lambda solution: solution.profit)

        return self.Solutions[0]