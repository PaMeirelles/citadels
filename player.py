from typing import List
from option import Option
from models import Character, District, PublicInfo, EndTurn, Ability, Build, Action, Forge, ThievesLair


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
        names = set([x.name for x in self.districts])

        if not self.used_ability:
            actions.append(Ability(self.character.value))

        if built == 0 or (built < 3 and self.character.value == Character.Architect):
            for i, c in enumerate(self.cards):
                if c.name == "Thieves lair" and len(self.cards) - 1 + self.gold >= c.cost:
                    for g in range(max(0, c.cost - len(self.cards) + 1), min(self.gold+1, 6)):
                        actions.append(ThievesLair(c, i, g))
                elif c.cost <= self.gold and (c.name not in names or "Quarry" in names):
                    actions.append(Build(c, i))

        if "Forge" in names and self.gold >= 2:
            actions.append(Forge())

        return actions
