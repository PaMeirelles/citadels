from game import Game
from random import seed
from tqdm import tqdm

seed(2)

averages = []

n = 10 ** 6
print_every = 10**4
c = ["Assassin", "Thief", "Magician", "King", "Bishop", "Merchant", "Architect", "Warlord"]

for played in tqdm(range(n), desc='Simulating Games'):
    game = Game(6)
    game.play()
    averages.append(game.stats.process_averages(game.evaluate()))
    if (played+1) % print_every == 0:
        print()
        for i in range(8):
            print(f"{c[i]}: {round(sum([a[i] for a in averages]) / played, 3)}")


