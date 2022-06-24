class EvaluationLogic:
    def __init__(self, inputData):
        self.InputData = inputData

    def calcProfit(self, solution) -> bool:
        valid = True
        totalEarnings = 0
        totalPenalty = 0
        maxCapacities = [knapsack.Capacity for knapsack in self.InputData.InputKnapsacks]
        penalties = [knapsack.Penalty for knapsack in self.InputData.InputKnapsacks]
        currentCapacities = [0] * self.InputData.NumKnapSacks
        for itemID, knapsackID in enumerate(solution.allocation):
            if knapsackID >= 0:
                item = self.InputData.findItemByID(itemID)
                currentCapacities[knapsackID] += item.Weight
                totalEarnings += item.Profit

        # check if solution is valid
        for currentCap, maxCap, penalty in zip(currentCapacities, maxCapacities, penalties):
            if currentCap > maxCap:
                valid = False
            else:
                totalPenalty += (maxCap - currentCap) * penalty

        if valid:
            solution.penalty = totalPenalty
            solution.earnings = totalEarnings
            solution.profit = totalEarnings - totalPenalty
        return valid