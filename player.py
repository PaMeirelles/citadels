from typing import List
from option import Option

from engine import get_engine_by_name
from models import Character, District, PublicInfo, EndTurn, Ability, Build


class Player:
    def __init__(self, player_id, engine_name):
        self.player_id = player_id
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[District] = []
        self.districts: List[District] = []
        self.engine = get_engine_by_name(engine_name)
        self.used_ability = False

    def get_public_info(self):
        PublicInfo(self.gold, len(self.cards), self.districts)

    def generate_actions(self, built):
        actions = [EndTurn]
        if not self.used_ability:
            actions.append(Ability(self.character.value))

        if built == 0 or (built < 3 and self.character == Character.Architect):
            for i, c in enumerate(self.cards):
                if c.cost <= self.gold:
                    actions.append(Build(c, i))
        return actions
