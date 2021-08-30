from ProblemManager import ProblemManager
from Chromosome import Chromosome
import random

class Population:
    def __init__(self, ps, seed, max_len):
        self.seed = seed
        self.manager = ProblemManager()
        self.manager.constructProblems() 
        self.max_chromosome_length = max_len
        self.individuals = []
        self.population_size = ps
        
        for i in range(0, self.population_size):
            begin_problems = self.manager.returnNProblems(0, 5)
            self.individuals.append(Chromosome(self.seed, begin_problems, self.max_chromosome_length))

        


    def evaluatePopulation(self):
     
        for i in range(0, len(self.individuals)):
            self.individuals[i].evaluateChromosome()