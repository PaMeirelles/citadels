from typing import List
from option import Option

from engine import get_engine_by_name
from models import Character, District, PublicInfo


class Player:
    def __init__(self, player_id, engine_name):
        self.player_id = player_id
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[District] = []
        self.districts: List[District] = []
        self.engine = get_engine_by_name(engine_name)

    def get_public_info(self):
        PublicInfo(self.gold, len(self.cards), self.districts)