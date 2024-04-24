from random import shuffle

from player import Player
from utility import retrieve_cards


class Game:
    def __init__(self, num_players):
        self.players = [Player(i) for (i, _) in enumerate(range(num_players))]
        self.deck = retrieve_cards()
        self.deal_cards()
        self.deal_gold()

    def deal_cards(self):
        shuffle(self.deck)
        for p in self.players:
            for _ in range(4):
                p.cards.append(self.deck.pop())

    def deal_gold(self):
        for p in self.players:
            p.gold = 2
