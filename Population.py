from ProblemManager import ProblemManager
from Chromosome import Chromosome
import random
from random import randint
import multiprocessing

from pathos.multiprocessing import ProcessingPool as Pool

class Population:
    def __init__(self, ps, seed, max_len, tournament_s = 7):
        self.tournament_size = tournament_s
        self.seed = seed
        self.best_fitness = 1
        self.best_individual = None
        self.manager = ProblemManager()
        self.manager.constructProblems() 
        self.max_chromosome_length = max_len
        self.individuals = []
        self.population_size = ps
        random.seed(self.seed)  #random.random()
        use_seed = self.seed + 1
        for i in range(0, self.population_size):
            selection_ids = []
            placement_ids = []
            
            use_seed = use_seed + 1
            random.seed(use_seed)
            for i in range(0, self.max_chromosome_length):
                
                selection_ids.append(randint(0, 4))
                placement_ids.append(randint(0, 3))

            random.seed(self.seed)
       
            begin_problems = self.manager.returnNProblems(0, 5)
            self.individuals.append(Chromosome(self.seed, begin_problems, self.max_chromosome_length, selection_ids, placement_ids))
            
            

    def applyGeneticOperator(self):
        choice = self.getRandomInt(0, 100)
        
        if choice < 30:
            parents = self.tournamentSelection(2)
            new_individuals = parents[0].crossover1(parents[1])
        elif choice < 60:
            parents = self.tournamentSelection(2)
            new_individuals = parents[0].crossover2(parents[1])
        elif choice < 80:
            parents = self.tournamentSelection(1)
            new_individuals = parents[0].mutate1()
        elif choice < 88:
            parents = self.tournamentSelection(1)
            new_individuals = parents[0].mutate2()
        else:
            parents = self.tournamentSelection(1)
            new_individuals = [parents[0].copy()]
            
        return new_individuals

    def tournamentSelection(self, num_parents_p):
        selection_pool = []
        parents = []
        
        
        for i in range(0, self.tournament_size):
            index = self.getRandomInt(0, len(self.individuals) - 1)
         
            selection_pool.append(self.individuals[index].copy())
        
        selection_pool.sort(key=lambda x: x.fitness, reverse=False)
        
        for i in range(0, num_parents_p):
            parents.append(selection_pool.pop(0))
        
        # print("TOURNAMENT PARENT SELECTION FItnESSES")
        # for p in parents:
        #     print(p.fitness)
        return parents
    
    
            
    def getRandomInt(self, a, b):
        self.seed = self.seed + 1
        random.seed(self.seed)  #random.random()
        rand_int =  randint(a, b)
        return rand_int
    
    def evaluateHelper(self, individual):
        
        individual.evaluateChromosome(self.num_gen)
      
                
        return individual
        
    def evaluatePopulation(self, num_gen = 1):
        
        self.num_gen = num_gen
        vals = Pool().map(self.evaluateHelper, self.individuals) 
    
            
        self.individuals = vals
        self.individuals.sort(key=lambda x: x.fitness, reverse=False)
        # print("create new pop")
        # for i in self.individuals:
        #     print("fit: " + str(i.fitness))
            
        if self.best_fitness > self.individuals[0].fitness:
            self.best_fitness = self.individuals[0].fitness
            self.best_individual = self.individuals[0].copy()
            print("BEST FITNESS: " + str(self.individuals[0].fitness))
        
        
        # for o in self.individuals[0].problems:
        #     print(len(o.used_objects))
        #     for s in o.used_objects:
        #         print(s.shapes)
            
        self.createNewPopulation(num_gen)
              
        
    def testSolution(self, num_gen = 1):
        new_problems = self.manager.returnNProblems(0, 5)
        self.best_individual.addProblems(new_problems)
        
            
        # self.num_gen = num_gen
        # vals = Pool().map(self.evaluateHelper, self.individuals) 
    
        self.best_individual = self.evaluateHelper(self.best_individual)
       
        print("testing pop")
    
        print("BEST FITNESS: " + str(self.best_individual.fitness))
        print("used objects: " + str(len(self.best_individual.used_objects)))
        for o in self.best_individual.used_objects:
            print(o.shapes)
        
        
    def createNewPopulation(self, num_gen = 1):
        
        # print("create new population")
        new_individuals = []
        index = 0
        while index < len(self.individuals):
            kids = self.applyGeneticOperator()
            index = index + len(kids)
            for k in range(0, len(kids)):
                new_individuals.append(kids[k])
                
        self.individuals = new_individuals
        if num_gen % 2 == 0:
            adder = - 1
        else:
            adder = + 1
        for i in range(0, len(self.individuals)):
            new_problems = self.manager.returnNProblems(num_gen + adder, (num_gen + adder) + 5)
           
            self.individuals[i].addProblems(new_problems)
        
            