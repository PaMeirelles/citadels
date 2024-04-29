from typing import List

from option import Option, Some, NONE
from basic_consistency import BasicConsistency
from models import Character, WarlordTarget, MagicianPower, SwapHands, PublicInfo
from random import choice, shuffle, randint
from player import Player


class BasicAbilities(BasicConsistency):
    def __init__(self):
        super().__init__()
        self.role_options = []

    def choose_target(self, character: Character, public_info: PublicInfo, myself: Player) -> Character:
        if character == Character.Assassin:
            if len(self.role_options) > 4:
                return choice([x for x in self.role_options if x != Character.Assassin])
            else:
                return choice([x for x in list(Character) if x not in self.role_options])
        elif character == Character.Thief:
            characters_after = [x for x in self.role_options if x != Character.Thief and x != Character.Assassin]
            characters_before = [x for x in list(Character) if x not in self.role_options and x != Character.Assassin]

            numbers = [x for x in range(len(public_info.player_public_info))]
            player_order = numbers[public_info.crown:] + numbers[:public_info.crown]
            my_index = player_order.index(myself.player_id)

            players_before = player_order[:my_index]
            players_after = player_order[(my_index + 1):]

            if len(characters_before) <= 1:
                return choice([x for x in characters_after if x != Character.Assassin])

            if len(characters_after) <= 1:
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
        lst = [(i, x.num_cards) for i, x in enumerate(public_info.player_public_info)]
        shuffle(lst)
        biggest_hand = sorted(lst, key=lambda x: -x[1])[0][0]

        return SwapHands(biggest_hand)

    def warlord(self, public_info: PublicInfo, myself: Player) -> Option[WarlordTarget]:
        lst = list(enumerate(public_info.player_public_info))
        shuffle(lst)
        for i, p in lst:
            if i == myself.player_id:
                continue
            for j, d in enumerate(public_info.player_public_info[i].districts):
                if d.cost == 1:
                    return Some(WarlordTarget(i, j))
        return NONE

    def choose_character(self, available_options: List[Character], public_info: PublicInfo, myself:Player) -> int:
        self.role_options = available_options
        return randint(0, len(available_options)-1)
