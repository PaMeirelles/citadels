from fast_builder import FastBuilder
from game import Game
from random import seed
import numpy as np
from deap import base, creator, tools, algorithms
from utility import get_engine_by_name

seed(2)
GAMES_BY_ROUND = 1000


def eval_func(chromosome):
    to_watch = FastBuilder(chromosome)

    fit_score = 0
    for _ in range(GAMES_BY_ROUND):
        game = Game(6, [to_watch] + [get_engine_by_name("fast_builder") for _ in range(5)])
        game.play()
        scores = [-x for x in game.evaluate()]
        positions = np.argsort(np.argsort(scores)).tolist()
        fit_score -= (positions[0] + 1)

    fit_score /= GAMES_BY_ROUND
    return fit_score,


def create_individual():
    individual = [np.random.uniform(0, 1) for _ in range(8)]
    return individual


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", eval_func)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=.5, sigma=0.2, indpb=0.2)

toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=50)

# Register a statistics object to gather statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("max", np.max)

# Run the algorithm with the stats object
algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=20, stats=stats, verbose=True)

# Best individual
best_individual = tools.selBest(population, k=1)[0]
print("Best individual:", best_individual)
