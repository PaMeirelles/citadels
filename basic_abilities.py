from typing import List
from engine import EngineInterface
from models import Character, District, Resource, Action, WarlordTarget, MagicianPower, SwapHands, \
    ChangeCards, NoTarget, WarlordOption, Ability, Build, PublicInfo
from random import randint, choice, random, sample
from player import Player


class BasicAbilities(EngineInterface):
    def __init__(self):
        super().__init__()
        self.role_options = []

    def discard_cards(self, n: int, cards: List[District], public_info: PublicInfo) -> List[int]:
        return sample([i for i in range(len(cards))], n)

    def choose_target(self, character: Character, public_info: PublicInfo, myself: Player) -> Character:
        if character == Character.Assassin:
            if len(self.role_options) > 4:
                return choice([x for x in self.role_options if x != Character.Assassin])
            else:
                return choice([x for x in list(Character) if x not in self.role_options])
        elif character == Character.Thief:
            characters_after = [x for x in self.role_options if x != Character.Thief]
            characters_before = [x for x in list(Character) if x not in self.role_options]

            numbers = [x for x in range(len(public_info.player_public_info))]
            player_order = numbers[public_info.crown:] + numbers[:public_info.crown]
            my_index = player_order.index(myself.player_id)

            players_before = player_order[:my_index]
            players_after = player_order[(my_index + 1):]

            if len(players_before) == 0:
                return choice([x for x in characters_after if x != Character.Assassin])

            if len(players_after) == 0:
                return choice([x for x in characters_before if x != Character.Assassin])

            player_gold_before = [public_info.player_public_info[i].gold for i in players_before]
            player_gold_after = [public_info.player_public_info[i].gold for i in players_after]

            average_player_gold_before = sum(player_gold_before) / len(players_before)
            average_player_gold_after = sum(player_gold_after) / len(players_after)

            average_gold_gain_if_before = len(players_before) / (len(players_before) + 1) * average_player_gold_before
            average_gold_gain_if_after = len(players_after) / (len(players_after) + 1) * average_player_gold_after

            if average_gold_gain_if_before > average_gold_gain_if_after:
                options = characters_before
            else:
                options = characters_after

            return choice([x for x in options if x != Character.Assassin])
        raise ValueError

    def magician(self, public_info: PublicInfo, myself: Player) -> MagicianPower:
        biggest_hand = sorted([(i, x.num_cards) for i, x in enumerate(public_info.player_public_info)],
                              key=lambda x: -x[1])[0][0]

        return SwapHands(biggest_hand)

    def warlord(self, public_info: PublicInfo, myself: Player) -> WarlordOption:
        for i, p in enumerate(public_info.player_public_info):
            if i == myself.player_id:
                continue
            for j, d in enumerate(public_info.player_public_info[i].districts):
                if d.cost == 1:
                    return WarlordTarget(i, j)
        return NoTarget()

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

    def choose_character(self, available_options: List[Character], public_info: PublicInfo) -> int:
        self.role_options = [x for x in available_options]
        return randint(0, len(available_options) - 1)
