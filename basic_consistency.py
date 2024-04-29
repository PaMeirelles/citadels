from typing import List
from models import District, Resource, Action, Ability, Build, PublicInfo
from random import choice
from player import Player
from random_chooser import RandomChooser


class BasicConsistency(RandomChooser):
    def choose_action(self, options: List[Action], public_info: PublicInfo, myself: Player) -> Action:
        most_expensive = None
        for op in options:
            if isinstance(op, Ability):
                return op
            elif isinstance(op, Build):
                if most_expensive is None:
                    most_expensive = op
                else:
                    if op.district.cost > most_expensive.district.cost:
                        most_expensive = op

        if most_expensive and most_expensive.district.cost <= myself.gold:
            return choice([x for x in options if isinstance(x, Build)])
        return choice(options)

    def choose_resource(self, public_info: PublicInfo, myself: Player) -> Resource:
        names = [x.name for x in myself.districts]
        if len([x for x in myself.cards if x.name not in names]) == 0:
            return Resource.Cards
        else:
            return Resource.Gold

    def choose_card(self, cards: List[District], public_info: PublicInfo, myself: Player) -> int:
        can_afford = []
        cant_afford = []
        for i, c in enumerate(cards):
            if c.cost <= myself.gold:
                can_afford.append(i)
            else:
                cant_afford.append(i)
        if len(can_afford) > 0:
            return sorted(can_afford, key=lambda x: -cards[x].cost)[0]
        else:
            return sorted(cant_afford, key=lambda x: cards[x].cost)[0]
