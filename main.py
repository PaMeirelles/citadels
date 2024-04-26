from game import Game
from random import seed
from tqdm import tqdm

seed(2)

print_every = 1000

positions_sum = [0 for _ in range(6)]
bc = [0 for _ in range(6)]
counter = 0

while True:
    counter += 1
    game = Game(6)
    game.play()
    scores = game.evaluate()
    positions = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    bc[positions[0]] += 1
    for i in range(6):
        positions_sum[i] += (1 + positions[i])

    if counter % print_every == 0:
        '''print(positions_sum)
        print(f"BC: {round(positions_sum[0] / counter, 3)}")
        print(f"RC: {round(sum(positions_sum[1:]) / (5 * counter), 3)}")'''
        print(f"Games: {counter}")

        for i in range(6):
            print(f"{i+1}: {round(bc[i] * 100 / sum(bc), 3)}%")
        print('-' * 80)


