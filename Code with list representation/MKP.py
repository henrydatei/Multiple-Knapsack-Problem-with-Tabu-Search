import os
from datetime import datetime
from typing import Tuple
import json

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

    data = InputData(os.path.join(path, "Testinstanzen", "Instance5_m20_n60.json"))
    # print(data)

    # sol = Solution([2,2,-1,1,-1,0,2,1,1,2,2,-1,1,0,1,-1,2,2,-1,1])

    # eva = EvaluationLogic(data).calcProfit(sol)
    # print(sol)

    # sol.printSolution()

    # pool = SolutionPool()
    # heuristik = ConstructiveHeuristics(EvaluationLogic(data), pool)
    # heuristik.Run(data, "greedy")
    # print(pool)

    # swapN = SwapNeighborhood(data, pool.GetHighestProfitSolution().allocation, EvaluationLogic(data), pool)
    # swapN.DiscoverMoves()
    # swapN.EvaluateMoves("BestImprovement")
    # pool.AddSolution(swapN.MakeBestMove())

    # insertN = InsertionNeighborhood(data, pool.GetHighestProfitSolution().allocation, EvaluationLogic(data), pool)
    # insertN.DiscoverMoves()
    # insertN.EvaluateMoves("BestImprovement")
    # pool.AddSolution(insertN.MakeBestMove())

    # k3N = BlockNeighborhoodK3(data, pool.GetHighestProfitSolution().allocation, EvaluationLogic(data), pool)
    # k3N.DiscoverMoves()
    # k3N.EvaluateMoves("BestImprovement")
    # print(k3N.MakeBestMove())

    # twoEN = TwoEdgeExchangeNeighborhood(data, pool.GetHighestProfitSolution().allocation, EvaluationLogic(data), pool)
    # twoEN.DiscoverMoves()
    # twoEN.EvaluateMoves("BestImprovement")
    # print(twoEN.MakeBestMove())

    # iterative = IterativeImprovement(data, 'BestImprovement', ['Swap','Insertion'])
    # iterative.Initialize(EvaluationLogic(data), pool)
    # iterative.Run(pool.GetHighestProfitSolution())
    # print(pool)

    solver = Solver(data, 42)
    tabu = TabuSearch(data, maxSeconds = 600, maxIterations = 30, neighborhoodEvaluationStrategy = "BestImprovement", neighborhoodTypes = ['Swap', 'Insertion', 'BlockK3', 'TwoEdgeExchange'])
    bestSol = solver.RunLocalSearch("greedy", tabu)

    # times = [('Instance05_m10_n60.json', 11.906224, 16785), ('Instance03_m5_n40.json', 1.207680, 265), ('Instance00_m2_n20.json', 0.309486, 185), ('Instance04_m10_n40.json', 2.194069, 4308), ('Instance13_m30_n60.json', 6.122341, -17099), ('Instance08_m15_n75.json', 31.630841, 21926), ('Instance5_m20_n60.json', 9.97702, 19553), ('Instance07_m5_n75.json', 8.99894, 730), ('Instance1_m10_n40.json', 1.164635, 2679), ('Instance7_m9_n100.json', 28.843242, 16349), ('Instance01_m3_n20.json', 0.220167, 89), ('Instance09_m10_n100.json', 73.475136, 38445), ('Instance0_m20_n20.json', 0.328872, 1734), ('Instance02_m3_n40.json', 1.130685, 230), ('Instance06_m10_n60.json', 8.638092, 13214), ('Instance8_m12_n48.json', 3.242127, 11705), ('Instance6_m10_n100.json', 32.769826, 15680)]

    # times2 = []
    # for file in os.listdir(os.path.join(path, "Testinstanzen")):
    #     if file.endswith(".json"):
    #         data = InputData(os.path.join(path, "Testinstanzen", file))
    #         pool = SolutionPool()
    #         heuristik = ConstructiveHeuristics(EvaluationLogic(data), pool)
    #         heuristik.Run(data, "greedy")
    #         times2.append(pool.GetHighestProfitSolution().profit)

    # with open(os.path.join(path, "ShortSolutionStatistics.json")) as f:
    #     jsonData = json.load(f)

    # print("Testinstanz", "Zeit in Sekunden", "konstruktive Lösung", "gefundene Lösung", "prozentuale Verbesserung", "optimale Lösung", "Optimalität der gefundenen Lösung", sep = ",")
    # for idx, time in enumerate(times):
    #     try:
    #         best = jsonData[time[0].split(".")[0]]["Objective Value"]
    #         percent = str(round(time[2] / best * 100, 2)) + " %"
    #     except:
    #         best = ""
    #         percent = ""
    #     conSol = times2[idx]
    #     if conSol <= 0:
    #         improvement = abs(round((time[2] - conSol) / time[2] * 100, 2))
    #     else:
    #         improvement = abs(round((time[2] - conSol) / conSol * 100, 2))
    #     print(time[0], time[1], conSol, time[2], str(improvement) + " %", best, percent, sep = ",")