from Population import Population
import time

seed = round(time.time() * 1000)
seed = 92

if __name__ == "__main__":
    population = Population(50, seed, 40)
    print("population constructed")
    for i in range(0, 10):
        population.evaluatePopulation(i+1)
    population.testSolution()  
    print(seed)
    
    

