import dataclasses
from copy import deepcopy
from .Solution import Solution

@dataclasses.dataclass
class SolutionPool:
    Solutions: list = dataclasses.field(init = False, default_factory = list)

    def AddSolution(self, newSolution):
        self.Solutions.append(deepcopy(newSolution))

    def GetLowestProfitSolution(self) -> Solution:
        self.Solutions.sort(key = lambda solution: solution.profit)

        return deepcopy(self.Solutions[0])