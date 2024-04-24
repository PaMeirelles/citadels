from enum import Enum
from dataclasses import dataclass
from typing import List
from option import Option
import csv
from random import shuffle

class DistrictType(Enum):
    Trade = 0
    Military = 1
    Religious = 2
    Noble = 3
    
    
def string_type_to_enum(str_type):
    str_type = str_type.lower()
    if str_type == 'trade':
        return DistrictType.Trade
    elif str_type == 'military':
        return DistrictType.Military
    elif str_type == 'religious':
        return DistrictType.Religious
    elif str_type == 'noble':
        return DistrictType.Noble
    else:
        raise ValueError("Invalid district type")


class Character(Enum):
    Assassin = 1
    Thief = 2
    Magician = 3
    King = 4
    Bishop = 5
    Merchant = 6
    Architect = 7
    Warlord = 8


@dataclass
class District:
    district_type: DistrictType
    cost: int
    name: str


class Player:
    def __init__(self):
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[District] = []
        self.districts: List[District] = []


def retrieve_cards():
    cards = []
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for _ in range(int(row['quantity'])):
                cards.append(District(string_type_to_enum(row['type']), int(row['cost']), row['name'].capitalize()))
    return cards


class Game:
    def __init__(self, num_players):
        self.players = [Player() for _ in range(num_players)]
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


game = Game(6)
print("oi")
