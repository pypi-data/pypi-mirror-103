from copy import deepcopy
from deap import base, creator, tools
import random, numpy as np
import warnings; warnings.filterwarnings('ignore')
if __name__ == "__main__":
    from fml.validates import validate_switch
else:
    from ..validates import validate_switch

def single_ga(X, Y, algo, maxf=10, loo=False, gen=40, ngen=20, cxpb=0.5, mutpb=0.7, verbose=True):
    def bisect_right(a, x, lo=0, hi=None):
        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            if x < a[mid]: hi = mid
            else: lo = mid+1
        return lo
    
    class HallOfFame(object):
        def __init__(self, maxsize):
            self.maxsize = maxsize
            self.keys = list()
            self.items = list()
    
        def update(self, population):
            for ind in population:
                if len(self) == 0 and self.maxsize !=0:
                    # Working on an empty hall of fame is problematic for the
                    # "for else"
                    self.insert(population[0])
                    continue
                if ind.fitness > self[-1].fitness or len(self) < self.maxsize:
                    for hofer in self:
                        # Loop through the hall of fame to check for any
                        # similar individual
                        if ind.all() == hofer.all():
                            break
                    else:
                        # The individual is unique and strictly better than
                        # the worst
                        if len(self) >= self.maxsize:
                            self.remove(-1)
                        self.insert(ind)
    
        def insert(self, item):
            item = deepcopy(item)
            i = bisect_right(self.keys, item.fitness)
            self.items.insert(len(self) - i, item)
            self.keys.insert(i, item.fitness)
    
        def remove(self, index):
            del self.keys[len(self) - (index % len(self) + 1)]
            del self.items[index]
    
        def clear(self):
            del self.items[:]
            del self.keys[:]
    
        def __len__(self):
            return len(self.items)
    
        def __getitem__(self, i):
            return self.items[i]
    
        def __iter__(self):
            return iter(self.items)
    
        def __reversed__(self):
            return reversed(self.items)
    
        def __str__(self):
            return str(self.items)
    
    def varAnd(population, toolbox, cxpb, mutpb):
        offspring = [toolbox.clone(ind) for ind in population]
    
        # Apply crossover and mutation on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < cxpb:
                offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1],
                                                              offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values
    
        for i in range(len(offspring)):
            if random.random() < mutpb:
                offspring[i], = toolbox.mutate(offspring[i])
                del offspring[i].fitness.values
    
        return offspring
    
    def eaSimple(population, toolbox, cxpb, mutpb, ngen,
                 halloffame=None, verbose=True):
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
    
        if halloffame is not None:
            halloffame.update(population)
    
        # Begin the generational process
        for gen in range(1, ngen + 1):
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))
    
            # Vary the pool of individuals
            offspring = varAnd(offspring, toolbox, cxpb, mutpb)
    
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
    
            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)
    
            # Replace the current population by the offspring
            population[:] = offspring
            
            if verbose:
                print(f"Gen {gen}: {halloffame[0].fitness.values[0]}")
        return population
    
    def f(individual, hof=False): # dict
        result = validate_switch(loo, algo, X[:, individual], Y)
        if hof:
            return result
        else:
            if len(set(Y.tolist())) > 8:
                return result["rmse"],
            else:
                return 1/result["accuracy_score"],
    
    def gen_ind(container, *argvs):
        if maxf == -1:
            flen = np.random.randint(2, X.shape[1])
        else:
            flen = np.random.randint(2, maxf)
        ind = np.random.choice(np.arange(X.shape[1]), flen, replace=False)
        return container(ind)
    
    def cxTwoPoint(ind1, ind2):
        cxpoint1, cxpoint2 = np.random.randint(0, len(ind1)), np.random.randint(0, len(ind2))
        ind1, ind2 = np.concatenate([ind1[:cxpoint1], ind2[cxpoint2:]]), np.concatenate([ind2[:cxpoint2], ind1[cxpoint1:]])
        ind1, ind2 = np.unique(ind1), np.unique(ind2)
        ind1 = creator.Individual(ind1)
        ind2 = creator.Individual(ind2)
        return ind1, ind2
    
    def mutate(indpb, individual):
        
        pool = set(individual.tolist()).difference(set(np.arange(X.shape[1]).tolist()))
        pool = np.array(list(pool))
        if len(pool) == 0:
            return individual,
        else:
            for i in range(len(individual)):
                if np.random.random() < indpb:
                    individual[i] = np.random.choice(pool, 1)
            return individual,
        
    
    creator.create("FitnessMax", base.Fitness, weights=(-1.0, ))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("evaluate", f)
    
    toolbox.register("individual", gen_ind, creator.Individual)
    toolbox.register("mate", cxTwoPoint)
    toolbox.register("mutate", mutate, 0.05)
    toolbox.register("select", tools.selTournament, tournsize=10)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, gen)
    population = toolbox.population()
    halloffame = HallOfFame(1)
    eaSimple(population, toolbox, cxpb, mutpb, ngen, halloffame=halloffame, verbose=verbose)
    return np.array(halloffame[0])

if __name__ == "__main__":
    
    from lightgbm import LGBMRegressor
    algo = LGBMRegressor
    from sklearn.datasets import load_boston
    X, Y = load_boston(return_X_y=True)
    loo = False
    best_individual = single_ga(X, Y, algo, 5)
    result = validate_switch(True, algo, X[:, best_individual], Y)


