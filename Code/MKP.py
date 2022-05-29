from cls.EvaluationLogic import EvalutationLogic
from cls.Solution import Solution
from cls.InputData import InputData
from cls.Solver import Solver

if __name__ == "__main__":
    data = InputData('/home/henry/Downloads/Beleg_PRE/Code/Instance0_m20_n20.json')
    sol = Solution([[1], [2], [3]])
    sol2 = Solution([[2], [3], [], [5]])

    EvalutationLogic(data).calcProfit(sol)
    print(sol)
    EvalutationLogic(data).calcProfit(sol2)
    print(sol2)