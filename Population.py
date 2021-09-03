from ProblemManager import ProblemManager
from Chromosome import Chromosome
import random
from random import randint
import multiprocessing

from pathos.multiprocessing import ProcessingPool as Pool

class Population:
    def __init__(self, ps, seed, max_len, tournament_s = 3):
        self.tournament_size = tournament_s
        self.seed = seed
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
        elif choice < 74:
            parents = self.tournamentSelection(1)
            new_individuals = parents[0].mutate1()
        elif choice < 88:
            new_individuals = parents[0].mutate2()
        else:
            parents = self.tournamentSelection(1)
            new_individuals = [parent[0].copy()]
            
        return new_individuals

    def tournamentSelection(self, num_parents_p):
        selection_pool = []
        parents = []
        
        
        for i in range(0, self.tournament_size):
            index = self.getRandomInt(0, len(self.individuals) - 1)
            selection_pool.append(self.individuals[index])
        
        selection_pool.sort(key=lambda x: x.fitness, reverse=False)
        
        for i in range(0, num_parents_p):
            parents.append(selection_pool.pop(0))
        
    
        for p in parents:
            print(p.fitness)
        return parents
    
    
            
    def getRandomInt(self, a, b):
        rand_int =  randint(a, b)
        return rand_int
    
    def evaluateHelper(self, individual):
        
        individual.evaluateChromosome()
      
                
        return individual
        
    def evaluatePopulation(self):
     
        # if __name__ == "Population":
        #     processes = []
        #     ret_values = []
        #     for i in range(0, len(self.individuals)):
        #         ret_value = multiprocessing.Value("d", self.individuals[i], lock=False)
        #         p = multiprocessing.Process(target=self.evaluateHelper, args=(ret_value,))
        #         ret_values.append(ret_value)
        #         processes.append(p)
        #         p.start()
                
        #     for p in processes:
        #         p.join()
                
        #     for v in ret_values:
        #         print(v.value)
            
                
        #     p = multiprocessing.Process(target=self.createNewPopulation)
        #     p.start()
        #     p.join()
        vals = Pool().map(self.evaluateHelper, self.individuals) 
    
            
        self.individuals = vals
        self.createNewPopulation()
              
                

       
            # output = process_pool.starmap(self.evaluateHelper, self.individuals)
           
        # for i in range(0, len(self.individuals)):
        #     print("==============================<><><><>>>>>>>>>>>>>   " + str(i))
        #     self.individuals[i].evaluateChromosome()
        #     print("\n")
        #     print(i)
        #     print("FINAL FITNESSSSSSSSS: " + str(self.individuals[i].fitness))
        #     print("\n")
            
    def createNewPopulation(self):
        print("create new pop")
        for i in self.individuals:
            print("fit: " + str(i.fitness))
        
        new_individuals = []
        index = 0
        while index < len(self.individuals):
            kids = self.applyGeneticOperator()
            index = index + len(kids)
            for k in range(0, len(kids)):
                new_individuals.append(kids[k])
                
        self.individuals = new_individuals