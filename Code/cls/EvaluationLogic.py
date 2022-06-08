class EvalutationLogic:
    inputData = None

    def __init__(self, inputdata) -> None:
        self.inputData = inputdata

    def calcProfit(self, solution):
        totalEarnings = 0
        totalPenalty = 0
        for knapsackID, itemList in enumerate(solution.allocation):
            items = [self.inputData.items[i] for i in itemList]
            weight = sum([item.weight for item in items])
            if self.inputData.knapsacks[knapsackID].capacity < weight:
                #print(items)
                raise Exception(f"Capacity for knapsack {knapsackID} to small: {weight}/{self.inputData.knapsacks[knapsackID].capacity}")
            earnings = sum([item.profit for item in items])
            penalty = (self.inputData.knapsacks[knapsackID].capacity - weight) * self.inputData.knapsacks[knapsackID].penalty
            totalEarnings += earnings
            totalPenalty += penalty
        solution.penalty = totalPenalty
        solution.earnings = totalEarnings
        solution.profit = totalEarnings - totalPenalty