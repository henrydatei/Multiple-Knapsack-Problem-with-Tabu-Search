from dataclasses import dataclass
import dataclasses
from .InputData import InputData
import json
import os

@dataclass
class Solution:
    inputData: InputData
    allocation: list = dataclasses.field(default_factory=list)
    penalty: int = dataclasses.field(init = False)
    earnings: int = dataclasses.field(init = False)
    profit: int = dataclasses.field(init = False)

    def calcProfit(self) -> bool:
        valid = True
        totalEarnings = 0
        totalPenalty = 0
        for knapsackID, itemList in enumerate(self.allocation):
            items = [self.inputData.items[i] for i in itemList]
            weight = sum([item.weight for item in items])
            if self.inputData.knapsacks[knapsackID].capacity < weight:
                #raise Exception(f"Capacity for knapsack {knapsackID} to small: {weight}/{self.inputData.knapsacks[knapsackID].capacity}")
                valid = False
            earnings = sum([item.profit for item in items])
            penalty = (self.inputData.knapsacks[knapsackID].capacity - weight) * self.inputData.knapsacks[knapsackID].penalty
            totalEarnings += earnings
            totalPenalty += penalty
        self.penalty = totalPenalty
        self.earnings = totalEarnings
        self.profit = totalEarnings - totalPenalty
        return valid

    def to_json(self, filename, includeEarnings = False, includePenalty = False, force = False):
        if not force and os.path.exists(filename):
            print(f"File {filename} exists. Use force = True to override.")
        else:
            with open(filename, "w") as file:
                solution = {"assignment": self.allocation, "score": self.profit}
                if includeEarnings:
                    solution["earnings"] = self.earnings
                if includePenalty:
                    solution["penalty"] = self.penalty
                json.dump(solution, file, indent = 4, sort_keys = True)