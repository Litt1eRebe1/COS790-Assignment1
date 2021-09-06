
from SelectionHeuristic import SelectionHeuristic
from PlacementHeuristics import PlacementHeuristics


import random
from random import randint

class Chromosome:
    def __init__(self, seed, problems, max_len, selection_ids, placement_ids):
    
        self.selection_ids = selection_ids
        self.placement_ids = placement_ids
        self.problems = problems
        self.seed = seed
        self.fitness = 1
        self.genes = []
        random.seed(self.seed)  #random.random()
        self.length = self.getRandomInt(4, max_len)
        
        
        for i in range(0, self.length):
            selection_heuristic = SelectionHeuristic(selection_ids[i], self.seed)
            placement_heuristic = PlacementHeuristics(placement_ids[i], self.seed)
            gene = Gene(self.seed, selection_heuristic, placement_heuristic)
            self.genes.append(gene)
        
     
        
    def getRandomInt(self, a, b):
        self.seed = self.seed + 1
        random.seed(self.seed)  #random.random()
        rand_int =  randint(a, b)
        return rand_int
    
    def copy(self):
        new_chrom = Chromosome(self.seed, self.problems.copy(), self.length, self.selection_ids.copy(), self.placement_ids.copy())
        new_genes = []
        for g in self.genes:
            new_genes.append(g.copy())
         
        new_chrom.genes = new_genes
        return new_chrom
        
    
    def crossover1(self, chromosome):
        # print("cross 1 ")
        index = self.getRandomInt(1, len(self.genes) - 2)
        
        if index >= len(chromosome.genes):
            index = self.getRandomInt(1, len(chromosome.genes) - 2)
        
        parent1 = self.copy()
        parent2 = chromosome.copy()
        # print("P1 : " + str(len(parent1.genes)))
        # print("P2 : " + str(len(parent2.genes)))
        p1_genes = []
        p2_genes = []
        for i in range(0, index):
            p1_genes.append(self.genes[i].copy())
            p2_genes.append(chromosome.genes[i].copy())
        
        
        for i in range(index, len(chromosome.genes)):
            p1_genes.append(chromosome.genes[i].copy())
            
        for i in range(index, len(self.genes)):
            p2_genes.append(self.genes[i].copy())
            
        
        parent1.genes = p1_genes
        parent2.genes = p2_genes
        # print("P1 - a : " + str(len(parent1.genes)))
        # print("P2 - a: " + str(len(parent2.genes)))
        
        return [parent1, parent2]
    
    def crossover2(self, chromosome):
        # print("cross 2 ")
        
        num_copy = int(len(self.genes) / 10)
        
        parent1 = self.copy()
        parent2 = chromosome.copy()
        # print("P1  : " + str(len(parent1.genes)))
        # print("P2 : " + str(len(parent2.genes)))
     
        if len(parent1.genes) > 0 and len(chromosome.genes) > 0:
            for i in range(0, num_copy):
                index_s = self.getRandomInt(0, len(parent1.genes) - 1)
                index_c = self.getRandomInt(0, len(chromosome.genes) - 1)
                parent1.genes[index_s] = chromosome.genes[index_c]
            
        
        num_copy = int(len(chromosome.genes) / 10)
        for i in range(0, num_copy):
            index_s = self.getRandomInt(0, len(parent2.genes) - 1)
            index_c = self.getRandomInt(0, len(self.genes) - 1)
      
            parent2.genes[index_s] = self.genes[index_c]
            
        # print("P1 - a : " + str(len(parent1.genes)))
        # print("P2 - a: " + str(len(parent2.genes)))
        return [parent1, parent2]
    
    def mutate1(self):
        # print("mutate 1")
        selection_heuristic = SelectionHeuristic(self.getRandomInt(0, 4), self.seed)
        placement_heuristic = PlacementHeuristics(self.getRandomInt(0, 3), self.seed)
   
        new_gene = Gene(self.seed, selection_heuristic, placement_heuristic)
        
        new_chrom = self.copy()
        # print(len(new_chrom.genes))
        new_chrom.genes.append(new_gene)
        # print(len(new_chrom.genes))
        return [new_chrom]
    
    def mutate2(self):
        # print("mutate 2")
        index = self.getRandomInt(0, len(self.genes) - 1)
        
        new_chrom = self.copy()
        # print(len(new_chrom.genes))
        if len(new_chrom.genes) > index:
            new_chrom.genes.pop(index)
        
        # print(len(new_chrom.genes))
        return [new_chrom]
 
        
    def addProblems(self, problems):
        self.problems = []
        for p in problems:
            self.problems.append(p.copy())
    
    def evaluateChromosome(self, gen):
        # print("evaluating")
        # for p in range(0, len(self.problems)): # for each problem  @TODO
        curr_fit = 0
        
        shape_area = 0
        for p in range(0, 5): # for each problem 
            object_area = 0
            curr_fit = 0
            problem_solved = False
        
            while not problem_solved:
                # print("evaluateChromosome")
                # print(len(self.genes))
                for g in self.genes: # apply each low level heuristic
    
                    if len(self.problems[p].shapes) > 0:
             
                        self.problems[p] = g.applyHeuristic(self.problems[p])
                    else:
                        break
                
                problem_solved =  len(self.problems[p].shapes) == 0
             
                # print("\nOBJECTS USED")
                # print(len(self.problems[p].used_objects))
                # print((self.problems[p].used_objects))
                for o in self.problems[p].used_objects:
                    object_area = object_area + (1000 * 1000)
                    # print("---")
                    # print(len(o.shapes))
                    # print(o.shapes)  
                    for s in o.shapes:
               
                        shape_area = shape_area + s.area
        
            
            curr_fit = curr_fit + (self.problems[p].solution_fitness - ( shape_area /  object_area))
         
            
        self.fitness = curr_fit / 5
        if self.fitness < 0:
            self.fitness = self.fitness * -1

        # print("self FITNESSSSS : " + str(self.fitness))
    
    
        
        
    
            
  
        


class Gene:
    def __init__(self, seed, selection_heuristic, placement_heuristic):
        
        self.seed = seed
        self.selection_heuristic = selection_heuristic
        self.placement_heuristic = placement_heuristic
  
        random.seed(self.seed)  #random.random()
       
    
    def applyHeuristic(self, problem):
        
        new_problem = self.placement_heuristic.applyHeuristic(problem, self.selection_heuristic)
        
        return new_problem
    
    def copy(self):
     
        new_gene = Gene(self.seed, self.selection_heuristic, self.placement_heuristic)
        return new_gene