from cls.EvaluationLogic import EvalutationLogic
from cls.Solution import Solution
from cls.Solver import Solver

import os

if __name__ == "__main__":
    #path = "/Users/henryhaustein/Downloads/Github/Multiple-Knapsack-Problem-with-Tabu-Search/Code"
    path = "/home/henry/Downloads/GitHub/Multiple-Knapsack-Problem-with-Tabu-Search/Code"

    solver = Solver(os.path.join(path, 'Instance01_m3_n20.json'))

    sol3 = Solution(solver.greedyAllocation())
    EvalutationLogic(solver.inputdata).calcProfit(sol3)
    print(sol3)
    solver.generateNeighboorhood(sol3, type = "insert", maxIterations = 100000)
    solver.generateNeighboorhood(solver.getBestSolutionFromSolutionPool(), type = "swap", maxIterations = 100000)
    print(solver)
    print(solver.getBestSolutionFromSolutionPool())