import os
from cls.InputData import InputData
from cls.EvaluationLogic import EvaluationLogic
from cls.Solution import Solution
from cls.ConstructiveHeuristic import ConstructiveHeuristics
from cls.SolutionPool import SolutionPool
from cls.Neighborhood import BlockNeighborhoodK3, InsertionNeighborhood, SwapNeighborhood, TwoEdgeExchangeNeighborhood
from cls.Solver import Solver
from cls.ImprovementAlgorithm import IterativeImprovement, TabuSearch

if __name__ == "__main__":
    #path = "/Users/henryhaustein/Downloads/Github/Multiple-Knapsack-Problem-with-Tabu-Search/Code"
    path = "/home/henry/Downloads/GitHub/Multiple-Knapsack-Problem-with-Tabu-Search/Code with list representation"

    data = InputData(os.path.join(path, 'Instance03_m5_n40.json'))
    # print(data)

    # sol = Solution([2,2,-1,1,-1,0,2,1,1,2,2,-1,1,0,1,-1,2,2,-1,1])

    # eva = EvaluationLogic(data).calcProfit(sol)
    # print(sol)

    # sol.printSolution()

    pool = SolutionPool()
    heuristik = ConstructiveHeuristics(EvaluationLogic(data), pool)
    heuristik.Run(data, "greedy")
    print(pool)

    # swapN = SwapNeighborhood(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    # swapN.DiscoverMoves()
    # swapN.EvaluateMoves("BestImprovement")
    # pool.AddSolution(swapN.MakeBestMove())

    # insertN = InsertionNeighborhood(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    # insertN.DiscoverMoves()
    # insertN.EvaluateMoves("BestImprovement")
    # pool.AddSolution(insertN.MakeBestMove())

    # k3N = BlockNeighborhoodK3(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    # k3N.DiscoverMoves()
    # k3N.EvaluateMoves("BestImprovement")
    # print(k3N.MakeBestMove())

    # twoEN = TwoEdgeExchangeNeighborhood(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    # twoEN.DiscoverMoves()
    # twoEN.EvaluateMoves("BestImprovement")
    # print(twoEN.MakeBestMove())

    # iterative = IterativeImprovement(data, 'BestImprovement', ['Swap','Insertion'])
    # iterative.Initialize(EvaluationLogic(data), pool)
    # iterative.Run(pool.GetLowestProfitSolution())
    # print(pool)

    #solver = Solver(data, 42)
    #tabu = TabuSearch(data, 100, neighborhoodEvaluationStrategy = "BestImprovement", neighborhoodTypes = ['Swap', 'Insertion', 'BlockK3', 'TwoEdgeExchange'])
    #solver.RunLocalSearch("greedy", tabu)

    insertion = IterativeImprovement(data, 'BestImprovement', ['Swap'])
    insertion.Initialize(EvaluationLogic(data), pool)
    print("")
    print("===================== is currently =====================")
    print(insertion.Run(pool.GetLowestProfitSolution()))

    sol = Solution([4, -1, -1, -1, -1, -1, -1, 0, -1, 3, -1, 1, 0, 1, 4, -1, -1, 3, -1, 0, 2, -1, -1, 0, 4, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 2, -1])
    EvaluationLogic(data).calcProfit(sol)
    print("")
    print("===================== should be =====================")
    print(sol)
    

