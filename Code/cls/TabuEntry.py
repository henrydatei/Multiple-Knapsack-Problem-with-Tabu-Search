from dataclasses import dataclass
from .Solution import Solution

@dataclass
class TabuEntry:
    solution: Solution
    time_remaining: int

    def update(self):
        self.time_remaining = self.time_remaining - 1