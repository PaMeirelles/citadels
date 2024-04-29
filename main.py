from math import ceil, floor

import numpy as np

from basic_genetic import get_best_basic_genetic
from game import Game
from random import seed
from tqdm import tqdm

from utility import get_engine_by_name

seed(1)

print_every = 1000

positions_sum = [0 for _ in range(6)]
bc = [0 for _ in range(6)]
counter = 0

while True:
    counter += 1
    game = Game(6, [get_engine_by_name("fast_builder")] + [get_engine_by_name("basic_genetic") for _ in range(5)])
    game.play()
    scores = [x for x in game.evaluate()]
    score_counts = {}
    positions = [0 for _ in range(6)]

    for i, score in enumerate(scores):
        score_counts.setdefault(score, []).append(i)

    current_position = len(scores) - 1
    for score in sorted(score_counts.keys()):
        count = len(score_counts[score])
        if count == 1:
            me = score_counts[score][0]
            positions[me] = current_position
        else:
            for i in range(count):
                positions[score_counts[score][i]] = (2 * current_position - count + 1) / 2
        current_position -= count

    if positions[0].is_integer():
        bc[int(positions[0])] += 1
    else:
        bc[int(ceil(positions[0]))] += .5
        bc[int(floor(positions[0]))] += .5
    for i in range(6):
        positions_sum[i] += (1 + positions[i])

    if counter % print_every == 0:
        print(positions_sum)
        print(f"WATCHED: {round(positions_sum[0] / counter, 3)}")
        print(f"CONTROL: {round(sum(positions_sum[1:]) / (5 * counter), 3)}")
        print(f"Games: {counter}")

        for i in range(6):
            print(f"{i+1}: {round(bc[i] * 100 / sum(bc), 3)}%")
        print('-' * 80)