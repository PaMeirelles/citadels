from enum import Enum
from dataclasses import dataclass
from typing import List
from option import Option


class DistrictType(Enum):
    Trade = 0
    Military = 1
    Religious = 2
    Noble = 3


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
class Building:
    district_type: DistrictType
    cost: int
    name: str


class Player:
    def __init__(self):
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[Building] = []
        self.districts: List[Building] = []


class Game:
    def __init__(self, num_players):
        self.players = [Player() for _ in num_players]

