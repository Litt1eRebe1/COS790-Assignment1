import random

class SelectionHeuristic:
    def __init__(self, id, seed):
        self.id = id
        self.seed = seed
        random.seed(self.seed)  #random.random()
    
    def applyHeuristic(self, problem):
        id = self.id
        if id == 0: # First Fit (FF). Consider the opened objects in turn in a fixed order and place the item in the first one where it fits.
            return problem.shapes.pop(0)
        elif id == 1: # First Fit Decreasing (FFD). Sort pieces in decreasing order, and the largest one is placed according to FF
            problem.shapes.sort(key=lambda x: x.area, reverse=True)
            
            return problem.shapes.pop(0)
        elif id == 2: # First Fit Increasing (FFI). Sort pieces in increasing order, and the smallest one is placed according to FF
            problem.shapes.sort(key=lambda x: x.area, reverse=False)
            return problem.shapes.pop(0)
        elif id == 3: # Filler + FFD. This places as many pieces as possible within the open objects. If at least one piece has been placed, the algorithm stops. The FFD algorithm is applied, otherwise
            return problem.shapes.pop(0)
        else: # Worst Fit (WF). It places the item in the opened object where it worst fits (that is, with the largest available room).
            # print("............................ Worst Fit (WF) .......................")
            # print(len(problem.shapes))
            ret_shape = problem.shapes.pop(0)
            problem.shapes.append(ret_shape)
            # print(len(problem.shapes))
            return ret_shape
            
            
   
    
    