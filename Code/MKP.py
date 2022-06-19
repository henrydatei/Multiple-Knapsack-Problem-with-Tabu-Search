from cls.TabuEntry import TabuEntry
from cls.Solution import Solution
from cls.Solver import Solver

import os

if __name__ == "__main__":
    path = "/Users/henryhaustein/Downloads/Github/Multiple-Knapsack-Problem-with-Tabu-Search/Code"
    #path = "/home/henry/Downloads/GitHub/Multiple-Knapsack-Problem-with-Tabu-Search/Code"

    solver = Solver(os.path.join(path, 'Instance01_m3_n20.json'))

    sol3 = solver.greedyAllocation()
    sol3.calcProfit()
    #print(sol3)
    #solver.solutionPool.append(sol3)
    #solver.generateNeighboorhood(sol3, type = "insert", maxIterations = 10000)
    #solver.generateNeighboorhood(solver.getBestSolutionFromSolutionPool(), type = "swap", maxIterations = 10000)
    # print(solver)
    #print(solver.getBestSolutionFromSolutionPool())

    bestSol = solver.tabuSearch(sol3, maxIterationsNeighboorhood = 10000)
    print(bestSol)

    # print("===================")
    # print([(sol.allocation, sol.profit) for sol in solver.solutionPool])
    # print("===================")
    # print(solver.getBestSolutionFromSolutionPool())

    newSol = Solution(solver.inputdata, [[13, 5], [19, 7, 14, 3, 12, 8], [6, 17, 16, 10, 9, 0, 1]])
    print(newSol.calcProfit(), newSol.profit)
