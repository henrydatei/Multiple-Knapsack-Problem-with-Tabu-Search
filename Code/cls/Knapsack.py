from dataclasses import dataclass
import dataclasses

@dataclass
class Knapsack:
    id: int
    capacity: int
    penalty: int