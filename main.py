import numpy as np

from basic_genetic import get_best_basic_genetic
from game import Game
from random import seed
from tqdm import tqdm

from genetic import get_best_genetic, get_my_genetic
from utility import get_engine_by_name

seed(2)

print_every = 1000

positions_sum = [0 for _ in range(6)]
bc = [0 for _ in range(6)]
counter = 0

while True:
    counter += 1
    game = Game(6, [get_best_basic_genetic()] + [get_engine_by_name("basic_abilities") for _ in range(5)])
    game.play()
    scores = [-x for x in game.evaluate()]
    positions = np.argsort(np.argsort(scores)).tolist()

    bc[positions[0]] += 1
    for i in range(6):
        positions_sum[i] += (1 + positions[i])

    if counter % print_every == 0:
        print(positions_sum)
        print(f"GE: {round(positions_sum[0] / counter, 3)}")
        print(f"BA: {round(sum(positions_sum[1:]) / (5 * counter), 3)}")
        print(f"Games: {counter}")

        for i in range(6):
            print(f"{i+1}: {round(bc[i] * 100 / sum(bc), 3)}%")
        print('-' * 80)