import os
from datetime import datetime
from typing import Tuple

from cls.InputData import InputData
from cls.EvaluationLogic import EvaluationLogic
from cls.Solution import Solution
from cls.ConstructiveHeuristic import ConstructiveHeuristics
from cls.SolutionPool import SolutionPool
from cls.Neighborhood import BlockNeighborhoodK3, InsertionNeighborhood, SwapNeighborhood, TwoEdgeExchangeNeighborhood
from cls.Solver import Solver
from cls.ImprovementAlgorithm import IterativeImprovement, TabuSearch

def runTimeStats(path: str) -> Tuple[Solution, datetime]:
    start = datetime.now()
    data = InputData(path)
    solver = Solver(data, 42)
    tabu = TabuSearch(data, 10, neighborhoodEvaluationStrategy = "BestImprovement", neighborhoodTypes = ['Swap', 'Insertion', 'BlockK3', 'TwoEdgeExchange'])
    bestSol = solver.RunLocalSearch("greedy", tabu)
    end = datetime.now()
    return bestSol, end - start

if __name__ == "__main__":
    #path = os.getcwd()
    path = os.path.dirname(os.path.abspath(__file__))
    #path = "/home/henry/Downloads/GitHub/Multiple-Knapsack-Problem-with-Tabu-Search/Code with list representation/Testinstanzen"

    data = InputData(os.path.join(path, "Testinstanzen", "Instance6_m10_n100.json"))
    # print(data)

    # sol = Solution([2,2,-1,1,-1,0,2,1,1,2,2,-1,1,0,1,-1,2,2,-1,1])

    # eva = EvaluationLogic(data).calcProfit(sol)
    # print(sol)

    # sol.printSolution()

    # pool = SolutionPool()
    # heuristik = ConstructiveHeuristics(EvaluationLogic(data), pool)
    # heuristik.Run(data, "greedy")
    # print(pool)

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

    # solver = Solver(data, 42)
    # tabu = TabuSearch(data, 10, neighborhoodEvaluationStrategy = "BestImprovement", neighborhoodTypes = ['Swap', 'Insertion', 'BlockK3', 'TwoEdgeExchange'])
    # bestSol = solver.RunLocalSearch("greedy", tabu)