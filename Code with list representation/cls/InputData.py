import json
import dataclasses
from .Item import Item
from .Knapsack import Knapsack

@dataclasses.dataclass
class InputData:
    path: str
    NumKnapSacks: int = dataclasses.field(init = False)
    NumItems: int = dataclasses.field(init = False)
    InputItems: list = dataclasses.field(init = False, default_factory = list)
    InputKnapsacks: list = dataclasses.field(init = False, default_factory = list)

    def __post_init__(self) -> None:
        with open(self.path, "r") as inputFile:
            inputData = json.load(inputFile)
        
        self.NumKnapSacks = inputData['NumKnapSacks']
        self.NumItems = inputData['NumItems']

        for knapsack in inputData['KnapSacks']:
            self.InputKnapsacks.append(Knapsack(**knapsack))

        for item in inputData["Items"]:
            self.InputItems.append(Item(**item))

    def findItemByID(self, itemID) -> Item:
        for item in self.InputItems:
            if item.Id == itemID:
                return item

    def findKnapsackByID(self, knapsackID) -> Knapsack:
        for knapsack in self.InputKnapsacks:
            if knapsack.Id == knapsackID:
                return knapsack