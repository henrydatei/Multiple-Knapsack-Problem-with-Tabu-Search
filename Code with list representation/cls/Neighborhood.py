from copy import deepcopy
from .Solution import Solution
from .InputData import InputData
from .EvaluationLogic import EvaluationLogic
from .SolutionPool import SolutionPool

from typing import Tuple, List

class BaseNeighborhood:
    def __init__(self, inputData: InputData, initialAllocation: list, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool):
        self.InputData = inputData
        self.Allocation = initialAllocation
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool

        self.Moves = []
        self.MoveSolutions = []

        self.Type = 'None'

    def DiscoverMoves(self) -> None:
        raise Exception('DiscoverMoves() is not implemented for the abstract BaseNeighborhood class.')

    def EvaluateMoves(self, evaluationStrategy: str) -> None:
        if evaluationStrategy == 'BestImprovement':
            self.EvaluateMovesBestImprovement()
        elif evaluationStrategy == 'FirstImprovement':
            self.EvaluateMovesFirstImprovement()
        else:
            raise Exception(f'Evaluation strategy {evaluationStrategy} not implemented.')

    def EvaluateMove(self, move) -> Tuple[bool, Solution]:
        moveSolution = Solution(move.Allocation)
        valid = self.EvaluationLogic.calcProfit(moveSolution)

        return valid, moveSolution

    """ Evaluate all moves. """
    def EvaluateMovesBestImprovement(self) -> None:
        for move in self.Moves:
            valid, moveSolution = self.EvaluateMove(move)

            if valid:
                self.MoveSolutions.append(moveSolution)

    """ Evaluate all moves until the first one is found that improves the best solution found so far. """
    def EvaluateMovesFirstImprovement(self) -> None:
        bestObjective = self.SolutionPool.GetHighestProfitSolution().profit

        for move in self.Moves:
            valid, moveSolution = self.EvaluateMove(move)

            if valid:
                self.MoveSolutions.append(moveSolution)

            if moveSolution.profit > bestObjective:
                # abort neighborhood evaluation because an improvement has been found
                return

    def MakeBestMove(self) -> Tuple[Solution, List[Solution]]:
        if len(self.MoveSolutions) > 0:
            self.MoveSolutions.sort(key = lambda solution: solution.profit, reverse = True) # sort solutions according to profit
            bestNeighborhoodSolution = self.MoveSolutions[0]
        else:
            bestNeighborhoodSolution = self.SolutionPool.GetHighestProfitSolution()

        return deepcopy(bestNeighborhoodSolution), deepcopy(self.MoveSolutions)

    def Update(self, permutation: list) -> None:
        self.Allocation = permutation

        self.Moves.clear()
        self.MoveSolutions.clear()

    def LocalSearch(self, neighborhoodEvaluationStrategy: str, solution: Solution) -> List[Solution]:
        #bestCurrentSolution = self.SolutionPool.GetLowestMakespanSolution() ## TO.DO: Lösung übergeben?

        hasSolutionImproved = True

        while hasSolutionImproved:
            self.Update(solution.allocation)
            self.DiscoverMoves()
            self.EvaluateMoves(neighborhoodEvaluationStrategy)

            bestNeighborhoodSolution, neighboorhoodSolutions = self.MakeBestMove()

            if bestNeighborhoodSolution.profit > solution.profit:
                #print("New best solution has been found!")
                #print(bestNeighborhoodSolution)

                self.SolutionPool.AddSolution(bestNeighborhoodSolution)

                solution.allocation = bestNeighborhoodSolution.allocation
                solution.profit = bestNeighborhoodSolution.profit
                solution.earnings = bestNeighborhoodSolution.earnings
                solution.penalty = bestNeighborhoodSolution.penalty

                return neighboorhoodSolutions
            else:
                #print(f"Reached local optimum of {self.Type} neighborhood. Stop local search.")
                hasSolutionImproved = False        

""" Represents the swap of the element at IndexA with the element at IndexB for a given permutation (= solution). """
class SwapMove:
    def __init__(self, initialAllocation, indexA, indexB):
        self.Allocation = list(initialAllocation) # create a copy of the permutation
        self.IndexA = indexA
        self.IndexB = indexB

        self.Allocation[indexA] = initialAllocation[indexB]
        self.Allocation[indexB] = initialAllocation[indexA]
        
""" Contains all $n choose 2$ swap moves for a given permutation (= solution). """
class SwapNeighborhood(BaseNeighborhood):
    def __init__(self, inputData: InputData, initialAllocation: list, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool):
        super().__init__(inputData, initialAllocation, evaluationLogic, solutionPool)

        self.Type = 'Swap'

    """ Generate all $n choose 2$ moves. """
    def DiscoverMoves(self) -> None:
        for i in range(len(self.Allocation)):
            for j in range(len(self.Allocation)):
                if i < j:
                    swapMove = SwapMove(self.Allocation, i, j)
                    self.Moves.append(swapMove)

""" Represents the insertion of the element itemID to the knapsack with knapsackID for a given permutation (= solution). """
class InsertionMove:
    def __init__(self, initialAllocation: list, itemID: int, knapsackID: int):
        self.Allocation = list(initialAllocation) # create a copy of the allocation
        self.itemID = itemID
        self.knapsackID = knapsackID

        self.Allocation[self.itemID] = self.knapsackID

""" Contains all insertion moves for a given permutation (= solution). """
class InsertionNeighborhood(BaseNeighborhood):
    def __init__(self, inputData: InputData, initialAllocation: list, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool):
        super().__init__(inputData, initialAllocation, evaluationLogic, solutionPool)

        self.Type = 'Insertion'

    def DiscoverMoves(self) -> None:
        for itemID in range(len(self.Allocation)):
            for knapsackID in range(-1, max(self.Allocation) + 1):
                if self.Allocation[itemID] == knapsackID:
                    continue

                insertionMove = InsertionMove(self.Allocation, itemID, knapsackID)
                self.Moves.append(insertionMove)
                
# Exercise in SS21, do not use in SS22
""" Represents the extraction of the sequence of elements starting at IndexA and ending at IndexA + $k$, and the reinsertion at the new position IndexB for a given permutation (= solution) for $k = 3$. """
class BlockMoveK3:
    def __init__(self, initialAllocation: list, indexA: int, indexB: int):
        self.Allocation = [] # create a copy of the permutation
        self.IndexA = indexA
        self.IndexB = indexB
        self.Length = 3 # pass as parameter to constructor to obtain the general block move

        for i in range(len(initialAllocation)):
            if i >= indexA and i < indexA + self.Length:  # if i in range(indexA, indexA + self.Length):
                continue

            self.Allocation.append(initialAllocation[i])

        for i in range(self.Length):
            self.Allocation.insert(indexB + i, initialAllocation[indexA + i])

""" Contains all $(n - k + 1)(n - k) - \max(0, n - 2k + 1)$ block moves for a given permutation (= solution) for $k = 3$. """
class BlockNeighborhoodK3(BaseNeighborhood):
    def __init__(self, inputData: InputData, initialAllocation: list, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool):
        super().__init__(inputData, initialAllocation, evaluationLogic, solutionPool)

        self.Type = 'K3'
        self.Length = 3

    def DiscoverMoves(self) -> None:
        for i in range(len(self.Allocation) - self.Length + 1):
            for j in range(len(self.Allocation) - self.Length + 1):
                # skip if: (the block would be reinserted at its initial position) or (the current block would be swapped with the preceding block to exclude symmetry) 
                if i == j or j == i - self.Length:
                    continue

                blockMove = BlockMoveK3(self.Allocation, i, j)
                self.Moves.append(blockMove)

# Exercise in SS22
class TwoEdgeExchangeMove:
    def __init__(self, initialAllocation: list, indexA: int, indexB: int):
        self.Allocation = []

        self.Allocation.extend(initialAllocation[:indexA])
        self.Allocation.extend(reversed(initialAllocation[indexA:indexB]))
        self.Allocation.extend(initialAllocation[indexB:])

class TwoEdgeExchangeNeighborhood(BaseNeighborhood):
    def __init__(self, inputData: InputData, initialAllocation: list, evaluationLogic: EvaluationLogic, solutionPool: SolutionPool):
        super().__init__(inputData, initialAllocation, evaluationLogic, solutionPool)

        self.Type = 'TwoEdgeExchange'
    
    def DiscoverMoves(self) -> None:
        for i in range(len(self.Allocation)):
            for j in range(len(self.Allocation)):
                if j < i + 1:
                    continue
                twoEdgeMove = TwoEdgeExchangeMove(self.Allocation, i, j)
                self.Moves.append(twoEdgeMove)
