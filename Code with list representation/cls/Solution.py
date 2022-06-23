from dataclasses import dataclass
import dataclasses
import json
import os

@dataclass
class Solution:
    allocation: list = dataclasses.field(default_factory=list)
    penalty: int = dataclasses.field(init = False, default = -99999999)
    earnings: int = dataclasses.field(init = False, default = -99999999)
    profit: int = dataclasses.field(init = False, default = -99999999)

    def to_json(self, filename, includeEarnings = False, includePenalty = False, force = False) -> None:
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

    def printSolution(self):
        for knapsackID in range(max(self.allocation) + 1):
            itemIDs = [i for i, x in enumerate(self.allocation) if x == knapsackID]
            print("Knapsack " + str(knapsackID) + ": " + str(itemIDs))