from .InputData import InputData

class Solver:
    seed: int
    path: str
    inputdata: InputData

    def __init__(self, path, seed = 42) -> None:
        self.seed = seed
        self.path = path
        self.inputdata = InputData(path)

    def __repr__(self) -> str:
        return f"Solver({self.seed = }, {self.path = }, {self.inputdata = })"

    def greedyAllocation(self) -> None:
        pass
        # sortedItems = sorted(self.items, key = lambda item: item.profit/item.weight, reverse = True)
        # knapsackIdx = 0
        # for item in sortedItems:
        #     knapsack = self.knapsacks[knapsackIdx]
        #     if knapsack.currentWeight + item.weight <= knapsack.capacity:
        #         knapsack.addItem(item)
        #     else:
        #         if knapsackIdx == self.numKnapsacks:
        #             break
        #         knapsackIdx += 1
        #         self.knapsacks[knapsackIdx].addItem(item)