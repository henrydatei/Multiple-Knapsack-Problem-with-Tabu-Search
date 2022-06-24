import os
from cls.InputData import InputData
from cls.EvaluationLogic import EvaluationLogic
from cls.Solution import Solution
from cls.ConstructiveHeuristic import ConstructiveHeuristics
from cls.SolutionPool import SolutionPool
from cls.Neighborhood import BlockNeighborhoodK3, InsertionNeighborhood, SwapNeighborhood, TwoEdgeExchangeNeighborhood

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
    heuristik.Run(data, "greedy")
    print(pool)

    swapN = SwapNeighborhood(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    swapN.DiscoverMoves()
    swapN.EvaluateMoves("BestImprovement")
    print(swapN.MakeBestMove())

    insertN = InsertionNeighborhood(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    insertN.DiscoverMoves()
    insertN.EvaluateMoves("BestImprovement")
    print(insertN.MakeBestMove())

    k3N = BlockNeighborhoodK3(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    k3N.DiscoverMoves()
    k3N.EvaluateMoves("BestImprovement")
    print(k3N.MakeBestMove())

    twoEN = TwoEdgeExchangeNeighborhood(data, pool.GetLowestProfitSolution().allocation, EvaluationLogic(data), pool)
    twoEN.DiscoverMoves()
    twoEN.EvaluateMoves("BestImprovement")
    print(twoEN.MakeBestMove())
    
