from typing import List
from option import Option
from models import Character, District, PublicInfo


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[District] = []
        self.districts: List[District] = []

    def get_public_info(self):
        PublicInfo(self.gold, len(self.cards), self.districts)