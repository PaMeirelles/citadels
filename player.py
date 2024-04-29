from typing import List
from option import Option

from constants import FACTORY, FORGE, QUARRY, THIEVES_LAIR, LABORATORY
from models import Character, District, PlayerPublicInfo, EndTurn, Ability, Build, Action, Forge, ThievesLair, \
    DistrictType, Laboratory


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.character = Option[Character]
        self.gold = 0
        self.cards: List[District] = []
        self.districts: List[District] = []
        self.used_ability = False

    def get_public_info(self):
        return PlayerPublicInfo(self.gold, len(self.cards), self.districts)

    def generate_actions(self, built) -> List[Action]:
        actions = [EndTurn()]
        names = set([x.name for x in self.districts])

        if not self.used_ability:
            actions.append(Ability(self.character.value))

        if built == 0 or (built < 3 and self.character.value == Character.Architect):
            for i, c in enumerate(self.cards):
                discount = 0
                if c.district_type == DistrictType.Special and FACTORY in names:
                    discount = 1
                if c.name == THIEVES_LAIR and len(self.cards) - 1 + self.gold + discount >= c.cost:
                    for g in range(max(0, c.cost - len(self.cards) + 1),
                                   min(self.gold+1, c.cost - discount)):
                        actions.append(ThievesLair(c, i, g))
                elif c.cost - discount <= self.gold and (c.name not in names or QUARRY in names):
                    actions.append(Build(c, i))

        if FORGE in names and self.gold >= 2:
            actions.append(Forge())

        if LABORATORY in names and len(self.cards) >= 1:
            actions.append(Laboratory())

        return actions
