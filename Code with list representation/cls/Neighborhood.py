from OutputData import *
from copy import deepcopy
class BaseNeighborhood:
    def __init__(self, inputData, initialPermutation, evaluationLogic, solutionPool):
        self.InputData = inputData
        self.Permutation = initialPermutation
        self.EvaluationLogic = evaluationLogic
        self.SolutionPool = solutionPool

        self.Moves = []
        self.MoveSolutions = []

        self.Type = 'None'

    def DiscoverMoves(self):
        raise Exception('DiscoverMoves() is not implemented for the abstract BaseNeighborhood class.')

    def EvaluateMoves(self, evaluationStrategy):
        if evaluationStrategy == 'BestImprovement':
            self.EvaluateMovesBestImprovement()
        elif evaluationStrategy == 'FirstImprovement':
            self.EvaluateMovesFirstImprovement()
        else:
            raise Exception(f'Evaluation strategy {evaluationStrategy} not implemented.')

    def EvaluateMove(self, move):
        moveSolution = Solution(self.InputData.InputJobs, move.Permutation)
        self.EvaluationLogic.DefineStartEnd(moveSolution)

        return moveSolution

    """ Evaluate all moves. """
    def EvaluateMovesBestImprovement(self):
        for move in self.Moves:
            moveSolution = self.EvaluateMove(move)

            self.MoveSolutions.append(moveSolution)

    """ Evaluate all moves until the first one is found that improves the best solution found so far. """
    def EvaluateMovesFirstImprovement(self):
        bestObjective = self.SolutionPool.GetLowestMakespanSolution().Makespan

        for move in self.Moves:
            moveSolution = self.EvaluateMove(move)

            self.MoveSolutions.append(moveSolution)

            if moveSolution.Makespan < bestObjective:
                # abort neighborhood evaluation because an improvement has been found
                return

    def MakeBestMove(self):
        self.MoveSolutions.sort(key = lambda solution: solution.Makespan) # sort solutions according to makespan

        bestNeighborhoodSolution = self.MoveSolutions[0]

        return bestNeighborhoodSolution

    def Update(self, permutation):
        self.Permutation = permutation

        self.Moves.clear()
        self.MoveSolutions.clear()

    def LocalSearch(self, neighborhoodEvaluationStrategy, solution):
        #bestCurrentSolution = self.SolutionPool.GetLowestMakespanSolution() ## TO.DO: Lösung übergeben?

        hasSolutionImproved = True

        while hasSolutionImproved:
            self.Update(solution.Permutation)
            self.DiscoverMoves()
            self.EvaluateMoves(neighborhoodEvaluationStrategy)

            bestNeighborhoodSolution = self.MakeBestMove()

            if bestNeighborhoodSolution.Makespan < solution.Makespan:
                # print("New best solution has been found!")
                # print(bestNeighborhoodSolution)

                self.SolutionPool.AddSolution(bestNeighborhoodSolution)

                solution.Permutation = bestNeighborhoodSolution.Permutation
                solution.Makespan = bestNeighborhoodSolution.Makespan
            else:
                # print(f"Reached local optimum of {self.Type} neighborhood. Stop local search.")
                hasSolutionImproved = False        

""" Represents the swap of the element at IndexA with the element at IndexB for a given permutation (= solution). """
class SwapMove:
    def __init__(self, initialPermutation, indexA, indexB):
        self.Permutation = list(initialPermutation) # create a copy of the permutation
        self.IndexA = indexA
        self.IndexB = indexB

        self.Permutation[indexA] = initialPermutation[indexB]
        self.Permutation[indexB] = initialPermutation[indexA]
        
""" Contains all $n choose 2$ swap moves for a given permutation (= solution). """
class SwapNeighborhood(BaseNeighborhood):
    def __init__(self, inputData, initialPermutation, evaluationLogic, solutionPool):
        super().__init__(inputData, initialPermutation, evaluationLogic, solutionPool)

        self.Type = 'Swap'

    """ Generate all $n choose 2$ moves. """
    def DiscoverMoves(self):
        for i in range(len(self.Permutation)):
            for j in range(len(self.Permutation)):
                if i < j:
                    swapMove = SwapMove(self.Permutation, i, j)
                    self.Moves.append(swapMove)

""" Represents the insertion of the element at IndexA at the new position IndexB for a given permutation (= solution). """
class InsertionMove:
    def __init__(self, initialPermutation, indexA, indexB):
        self.Permutation = [] # create a copy of the permutation
        self.IndexA = indexA
        self.IndexB = indexB

        for k in range(len(initialPermutation)):
            if k == indexA:
                continue

            self.Permutation.append(initialPermutation[k])

        self.Permutation.insert(indexB, initialPermutation[indexA])

""" Contains all $(n - 1)^2$ insertion moves for a given permutation (= solution). """
class InsertionNeighborhood(BaseNeighborhood):
    def __init__(self, inputData, initialPermutation, evaluationLogic, solutionPool):
        super().__init__(inputData, initialPermutation, evaluationLogic, solutionPool)

        self.Type = 'Insertion'

    def DiscoverMoves(self):
        for i in range(len(self.Permutation)):
            for j in range(len(self.Permutation)):
                if i == j or i == j + 1:
                    continue

                insertionMove = InsertionMove(self.Permutation, i, j)
                self.Moves.append(insertionMove)
                
# Exercise in SS21, do not use in SS22
""" Represents the extraction of the sequence of elements starting at IndexA and ending at IndexA + $k$, and the reinsertion at the new position IndexB for a given permutation (= solution) for $k = 3$. """
class BlockMoveK3:
    def __init__(self, initialPermutation, indexA, indexB):
        self.Permutation = [] # create a copy of the permutation
        self.IndexA = indexA
        self.IndexB = indexB
        self.Length = 3 # pass as parameter to constructor to obtain the general block move

        for i in range(len(initialPermutation)):
            if i >= indexA and i < indexA + self.Length:  # if i in range(indexA, indexA + self.Length):
                continue

            self.Permutation.append(initialPermutation[i])

        for i in range(self.Length):
            self.Permutation.insert(indexB + i, initialPermutation[indexA + i])

""" Contains all $(n - k + 1)(n - k) - \max(0, n - 2k + 1)$ block moves for a given permutation (= solution) for $k = 3$. """
class BlockNeighborhoodK3(BaseNeighborhood):
    def __init__(self, inputData, initialPermutation, evaluationLogic, solutionPool):
        super().__init__(inputData, initialPermutation, evaluationLogic, solutionPool)

        self.Type = 'Insertion'
        self.Length = 3

    def DiscoverMoves(self):
        for i in range(len(self.Permutation) - self.Length + 1):
            for j in range(len(self.Permutation) - self.Length + 1):
                # skip if: (the block would be reinserted at its initial position) or (the current block would be swapped with the preceding block to exclude symmetry) 
                if i == j or j == i - self.Length:
                    continue

                blockMove = BlockMoveK3(self.Permutation, i, j)
                self.Moves.append(blockMove)

# Exercise in SS22
class TwoEdgeExchangeMove:
    def __init__(self, initialPermutation, indexA, indexB):
        self.Permutation = []

        self.Permutation.extend(initialPermutation[:indexA])
        self.Permutation.extend(reversed(initialPermutation[indexA:indexB]))
        self.Permutation.extend(initialPermutation[indexB:])

class TwoEdgeExchangeNeighborhood(BaseNeighborhood):
    def __init__(self, inputData, initialPermutation, evaluationLogic, solutionPool):
        super().__init__(inputData, initialPermutation, evaluationLogic, solutionPool)

        self.Type = 'TwoEdgeExchange'
    
    def DiscoverMoves(self):
        for i in range(len(self.Permutation)):
            for j in range(len(self.Permutation)):
                if j < i + 1:
                    continue
                twoEdgeMove = TwoEdgeExchangeMove(self.Permutation, i, j)
                self.Moves.append(twoEdgeMove)

class TaillardInsertionMove:
    def __init__(self, initialPermutation, indexA):
        self.removedJob = initialPermutation[indexA]
        self.Permutation = [x for x in initialPermutation if x != self.removedJob]

class TaillardInsertionNeighborhood(BaseNeighborhood):
    def __init__(self, inputData, initialPermutation, evaluationLogic, solutionPool):
        super().__init__(inputData, initialPermutation, evaluationLogic, solutionPool)

        self.Type = 'TaillardInsertion'

    def DiscoverMoves(self):
        for i in range(len(self.Permutation)):
            bestInsertionMove = TaillardInsertionMove(self.Permutation, i)
            self.Moves.append(bestInsertionMove)

    def EvaluateMove(self, move):
        moveSolution = Solution(self.InputData.InputJobs, move.Permutation)
        self.EvaluationLogic.DetermineBestInsertionAccelerated(moveSolution, move.removedJob)

        return moveSolution
