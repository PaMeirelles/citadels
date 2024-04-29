from random import random, seed

import numpy as np
import trueskill

from game import Game
from utility import get_engine_by_name

env = trueskill.TrueSkill(draw_probability=0)  # uses default settings

r1 = env.create_rating()
r2 = env.create_rating()
r3 = env.create_rating()


human_names = ["Random Chooser", "Basic Consistency", "Basic Abilities", "Basic Genetic", "Fast Builder",
               "Smart Discard"]
engine_names = ["random_chooser", "basic_consistency", "basic_abilities", "basic_genetic", "fast_builder",
                "smart_discard"]

engines = [get_engine_by_name(name) for name in engine_names]
ratings = [env.create_rating() for _ in range(len(engines))]

seed(2)
pe = 10 ** 3

for c in range(10 ** 6):
    game = Game(6, engines)
    rating_groups = [(r,) for r in ratings]
    game.play()
    random_values = np.random.random(6)
    scores = [-x + random() for x in game.evaluate()]
    post_match_rate = env.rate(rating_groups, ranks=scores)
    ratings = [r[0] for r in post_match_rate]
    if c % pe == 0:
        for i in range(6):
            print(f"{human_names[i]} = {env.expose(ratings[i])} {ratings[i]}")
        print()
