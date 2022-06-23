import os
from cls.InputData import InputData
from cls.EvaluationLogic import EvaluationLogic
from cls.Solution import Solution
from cls.ConstructiveHeuristic import ConstructiveHeuristics
from cls.SolutionPool import SolutionPool

if __name__ == "__main__":
    #path = "/Users/henryhaustein/Downloads/Github/Multiple-Knapsack-Problem-with-Tabu-Search/Code"
    path = "/home/henry/Downloads/GitHub/Multiple-Knapsack-Problem-with-Tabu-Search/Code"

    data = InputData(os.path.join(path, 'Instance01_m3_n20.json'))
    print(data)

    sol = Solution([2,2,-1,1,-1,0,2,1,1,2,2,-1,1,0,1,-1,2,2,-1,1])

    eva = EvaluationLogic(data).calcProfit(sol)
    print(sol)

    sol.printSolution()

    pool = SolutionPool()
    heuristik = ConstructiveHeuristics(EvaluationLogic(data), pool)
    heuristik.Run(data, "ROS")
    
