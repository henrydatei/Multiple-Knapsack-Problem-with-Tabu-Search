import json
from .Item import Item
from .Knapsack import Knapsack

class InputData:
    numKnapsacks: int = 0
    numItems: int = 0
    knapsacks: list = []
    items: list = []
    path: str

    def __init__(self, path) -> None:
        self.path = path

        with open(path) as f:
            data = json.load(f)
            self.numItems = data["NumItems"]
            self.numKnapsacks = data["NumKnapSacks"]
            for knapsack in data["KnapSacks"]:
                k = Knapsack(id = knapsack["Id"], capacity = knapsack["Capacity"], penalty = knapsack["Penalty"])
                self.knapsacks.append(k)
            for item in data["Items"]:
                i = Item(id = item["Id"], weight = item["Weight"], profit = item["Profit"])
                self.items.append(i)

        # sanity check
        if self.numItems != len(self.items):
            print(f"Wrong number of items: Found {len(self.items)} items but should {self.numItems} items")
        if self.numKnapsacks != len(self.knapsacks):
            print(f"Wrong number of knapsacks: Found {len(self.knapsacks)} knapsacks but should {self.numKnapsacks} knapsacks")

    def __repr__(self) -> str:
        return f"InputData({self.path = }, {self.numItems = }, {self.numKnapsacks = }, {self.knapsacks = }, {self.items = })"