from cls.TabuEntry import TabuEntry
from cls.Solution import Solution
from cls.Solver import Solver

import os

if __name__ == "__main__":
    path = "/Users/henryhaustein/Downloads/Github/Multiple-Knapsack-Problem-with-Tabu-Search/Code"
    #path = "/home/henry/Downloads/GitHub/Multiple-Knapsack-Problem-with-Tabu-Search/Code"

    solver = Solver(os.path.join(path, 'Instance01_m3_n20.json'))

    sol3 = solver.greedyAllocation()
    print(sol3)
    solver.solutionPool.append(sol3)
    #solver.generateNeighboorhood(sol3, type = "insert", maxIterations = 10000)
    #solver.generateNeighboorhood(solver.getBestSolutionFromSolutionPool(), type = "swap", maxIterations = 100000)
    # print(solver)
    #print(solver.getBestSolutionFromSolutionPool())

    # bestSol = solver.tabuSearch(sol3)
    # print(bestSol)

    newSol = Solution(solver.inputdata, [[14, 12], [8, 7, 3, 16, 6, 0, 19], [9, 10, 13, 17, 5, 1]])
    print(newSol)
    solver.solutionPool.append(newSol)

    print("===================")
    print(solver.solutionPool)
    print("===================")
    print(solver.getBestSolutionFromSolutionPool())
