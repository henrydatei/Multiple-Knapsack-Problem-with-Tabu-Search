from dataclasses import dataclass
import dataclasses
from .InputData import InputData

@dataclass
class Solution:
    inputData: InputData
    allocation: list = dataclasses.field(default_factory=list)
    penalty: int = dataclasses.field(init = False)
    earnings: int = dataclasses.field(init = False)
    profit: int = dataclasses.field(init = False)

    def __post_init__(self):
        self.calcProfit()

    def calcProfit(self):
        totalEarnings = 0
        totalPenalty = 0
        for knapsackID, itemList in enumerate(self.allocation):
            items = [self.inputData.items[i] for i in itemList]
            weight = sum([item.weight for item in items])
            if self.inputData.knapsacks[knapsackID].capacity < weight:
                raise Exception(f"Capacity for knapsack {knapsackID} to small: {weight}/{self.inputData.knapsacks[knapsackID].capacity}")
            earnings = sum([item.profit for item in items])
            penalty = (self.inputData.knapsacks[knapsackID].capacity - weight) * self.inputData.knapsacks[knapsackID].penalty
            totalEarnings += earnings
            totalPenalty += penalty
        self.penalty = totalPenalty
        self.earnings = totalEarnings
        self.profit = totalEarnings - totalPenalty