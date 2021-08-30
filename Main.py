from Population import Population
import time

seed = round(time.time() * 1000)
seed = 12

population = Population(1, seed, 40)
print("population constructed")
population.evaluatePopulation()

