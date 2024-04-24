from game import Game
from random import seed

seed(12)

game = Game(6)

game.play()

print(game.evaluate())
