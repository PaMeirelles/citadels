from typing import List
from option import Option
from models import Character, District, PublicInfo, EndTurn, Ability, Build, Action


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[District] = []
        self.districts: List[District] = []
        self.used_ability = False

    def get_public_info(self):
        return PublicInfo(self.gold, len(self.cards), self.districts)

    def generate_actions(self, built) -> List[Action]:
        actions = [EndTurn()]
        if not self.used_ability:
            actions.append(Ability(self.character.value))

        if built == 0 or (built < 3 and self.character == Character.Architect):
            for i, c in enumerate(self.cards):
                if c.cost <= self.gold:
                    actions.append(Build(c, i))
        return actions
