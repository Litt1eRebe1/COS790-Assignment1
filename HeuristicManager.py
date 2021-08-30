from SelectionHeuristic import SelectionHeuristic
from PlacementHeuristics import PlacementHeuristics
import random

class HeuristicManager:
    def __init__(self, seed):
        one = 1
        self.seed = seed
        random.seed(self.seed)  #random.random()
    
        
    