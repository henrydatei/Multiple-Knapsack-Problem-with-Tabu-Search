from dataclasses import dataclass
import dataclasses

@dataclass
class Solution:
    allocation: list = dataclasses.field(default_factory=list)
    penalty: int = dataclasses.field(init = False)
    earnings: int = dataclasses.field(init = False)
    profit: int = dataclasses.field(init = False)
    
    def __init__(self, allocation) -> None:
        self.allocation = allocation