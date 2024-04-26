from typing import List
from engine import EngineInterface
from models import Character, PublicInfo, District, Resource, Action, WarlordTarget, MagicianPower, SwapHands, \
    ChangeCards, NoTarget, WarlordOption, Ability, Build
from random import randint, choice, random, sample
from player import Player


class BasicConsistency(EngineInterface):
    def discard_cards(self, n: int, cards: List[District], public_info: List[PublicInfo]) -> List[int]:
        return sample([i for i in range(len(cards))], n)

    def choose_target(self, character: Character, public_info: List[PublicInfo]) -> Character:
        return choice(list(Character))

    def magician(self, public_info: List[PublicInfo], myself: Player) -> MagicianPower:
        if random() > .5:
            return SwapHands(randint(0, len(public_info)-1))
        else:
            card_ids = [x for x in range(len(myself.cards)) if random() > .5]
            return ChangeCards(card_ids)

    def warlord(self, public_info: List[PublicInfo]) -> WarlordOption:
        player_id = randint(0, len(public_info)-1)
        if len(public_info[player_id].districts) == 0:
            return NoTarget()
        district_id = randint(0, len(public_info[player_id].districts)-1)
        return WarlordTarget(player_id, district_id)

    def choose_action(self, options: List[Action], public_info: List[PublicInfo], myself: Player) -> Action:
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

    def choose_resource(self, public_info: List[PublicInfo], myself: Player) -> Resource:
        names = [x.name for x in myself.districts]
        if len([x for x in myself.cards if x.name not in names]) == 0:
            return Resource.Cards
        else:
            return Resource.Gold

    def choose_card(self, cards: List[District], public_info: List[PublicInfo], myself: Player) -> int:
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

    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        return randint(0, len(available_options)-1)
