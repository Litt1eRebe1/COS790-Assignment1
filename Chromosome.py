
from SelectionHeuristic import SelectionHeuristic
from PlacementHeuristics import PlacementHeuristics

import random
from random import randint

class Chromosome:
    def __init__(self, seed, problems, max_len):
        self.problems = problems
        self.seed = seed
        self.genes = []
        random.seed(self.seed)  #random.random()
        self.length = self.getRandomInt(2, max_len)
        
        selection_ids = []
        placement_ids = []
        
        for i in range(0, self.length):
            selection_ids.append(randint(0, 4))
            placement_ids.append(randint(0, 2))
   
            
        for i in range(0, self.length):
            selection_heuristic = SelectionHeuristic(selection_ids[i], self.seed)
            placement_heuristic = PlacementHeuristics(placement_ids[i], self.seed)
            gene = Gene(self.seed, selection_heuristic, placement_heuristic)
            self.genes.append(gene)
        
     
        
    def getRandomInt(self, a, b):
        rand_int =  randint(a, b)
        return rand_int
    
    def evaluateChromosome(self):
        # for p in range(0, len(self.problems)): # for each problem  @TODO
         for p in range(0, 5): # for each problem 
             problem_solved = False
             while not problem_solved:
                for g in self.genes: # apply each low level heuristic
                    if len(self.problems[p].shapes) > 0:
                        self.problems[p] = g.applyHeuristic(self.problems[p])
                    else:
                        break
                
                problem_solved =  len(self.problems[p].shapes) == 0
                print('\n' + str(problem_solved) + '\n')
                print("\nOBJECTS USED")
                print(self.problems[p].used_objects)
                for o in self.problems[p].used_objects:
                    print("---")
                    print(len(o.shapes))
                    print(o.shapes)  
                    for s in o.shapes:
                        print(list(s.exterior.coords))
                    print("---")
                print('\n')
            
  
        


class Gene:
    def __init__(self, seed, selection_heuristic, placement_heuristic):
        self.seed = seed
        self.selection_heuristic = selection_heuristic
        self.placement_heuristic = placement_heuristic
        random.seed(self.seed)  #random.random()
       
    
    def applyHeuristic(self, problem):
        
        new_problem = self.placement_heuristic.applyHeuristic(problem, self.selection_heuristic)
        
        return new_problem