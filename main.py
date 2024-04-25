from game import Game
from random import seed
from tqdm import tqdm

seed(2)

averages = []
special_dict = {}

n = 5 * 10 ** 5
print_every = 5 * 10**3
update_progress_bar_every = 10**3
c = ["Assassin", "Thief", "Magician", "King", "Bishop", "Merchant", "Architect", "Warlord"]

for played in tqdm(range(n), desc='Simulating Games', mininterval=1):
    game = Game(6)
    game.play()
    averages.append(game.stats.process_averages(game.evaluate()))
    for k, v in game.stats.special_dict.items():
        special_dict.setdefault(k, []).append(v)
    if (played+1) % print_every == 0:
        '''print()
        for i in range(8):
            print(f"{c[i]}: {round(sum([a[i] for a in averages]) / played, 3)}")'''
        for k, v in special_dict.items():
            print(f"{k}: {round(sum(v)/len(v), 3)}")


