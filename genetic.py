import math
from math import log
from typing import List, Tuple

import numpy as np

from engine import EngineInterface
from models import Character, District, Resource, Action, WarlordTarget, MagicianPower, SwapHands, \
    NoTarget, WarlordOption, Ability, Build, PublicInfo, DistrictType
from random import choice, sample
from player import Player


def log(value, base):
    if base < 0:
        print(base)
        raise ValueError
    if value == 0: return 0
    return math.log(value, base)


def get_biggest_hand(public_info: PublicInfo):
    biggest_hand = sorted([(i, x.num_cards) for i, x in enumerate(public_info.player_public_info)],
                          key=lambda x: -x[1])[0]

    return biggest_hand


def calculate_hit_chance(len_role_options):
    num_opt_before = 8 - len_role_options
    num_opt_after = len_role_options - 1

    if num_opt_before == 0:
        chance_before = 0
    else:
        chance_before = (num_opt_before - 1) / num_opt_before

    if num_opt_after == 0:
        chance_after = 0
    else:
        chance_after = (num_opt_after - 1) / num_opt_after

    return chance_before, chance_after


def get_best_genetic():
    best_genes = [-0.47799918628651966, -0.760409716185604, 0.5269611955962961, 1.6572582167933207, -0.2528053409757393,
                  -0.49067756119790285, -0.5882979974517359]
    chromosome = np.clip(best_genes, -0.99, 1)

    return Genetic(chromosome[0], chromosome[1] * 5 + 5, chromosome[2] * 5 + 5, chromosome[3], chromosome[4],
                   chromosome[5],
                   chromosome[6])


def get_my_genetic():
    return Genetic(2, 2,3, 0.2, .1, .1, .1)


class Genetic(EngineInterface):
    def __init__(self, turn_c, gold_c, card_c, pos_c, destruction_c, multi_build_c, protection_c, gnt=None):
        super().__init__()
        self.role_options = []
        self.turn_c = turn_c
        self.gold_c = gold_c
        self.card_c = card_c
        self.pos_c = pos_c
        self.destruction_c = destruction_c
        self.multi_build_c = multi_build_c
        self.protection_c = protection_c
        if gnt is None:
            self.gold_next_turn = gold_c
        else:
            self.gold_next_turn = gnt

    def discard_cards(self, n: int, cards: List[District], public_info: PublicInfo) -> List[int]:
        return sample([i for i in range(len(cards))], n)

    def calculate_average_gold_expectation(self, public_info, myself) -> Tuple[float, float]:
        characters_after = [x for x in self.role_options if x != Character.Thief]
        characters_before = [x for x in list(Character) if x not in self.role_options]

        numbers = [x for x in range(len(public_info.player_public_info))]
        player_order = numbers[public_info.crown:] + numbers[:public_info.crown]
        my_index = player_order.index(myself.player_id)

        players_before = player_order[:my_index]
        players_after = player_order[(my_index + 1):]

        player_gold_before = [public_info.player_public_info[i].gold for i in players_before]
        player_gold_after = [public_info.player_public_info[i].gold for i in players_after]

        if len(players_before) == 0:
            average_player_gold_before = 0
        else:
            average_player_gold_before = sum(player_gold_before) / len(players_before)

        if len(players_after) == 0:
            average_player_gold_after = 0
        else:
            average_player_gold_after = sum(player_gold_after) / len(players_after)

        average_gold_gain_if_before = len(players_before) / (len(players_before) + 1) * average_player_gold_before
        average_gold_gain_if_after = len(players_after) / (len(players_after) + 1) * average_player_gold_after

        return average_gold_gain_if_before, average_gold_gain_if_after

    def choose_target(self, character: Character, public_info: PublicInfo, myself: Player) -> Character:
        if character == Character.Assassin:
            hc_before, hc_after = calculate_hit_chance(len(self.role_options))
            if hc_after > hc_before:
                return choice([x for x in self.role_options if x != Character.Assassin])
            else:
                return choice([x for x in list(Character) if x not in self.role_options])
        elif character == Character.Thief:
            characters_after = [x for x in self.role_options if x != Character.Thief]
            characters_before = [x for x in list(Character) if x not in self.role_options]

            average_gold_gain_if_before, average_gold_gain_if_after = \
                self.calculate_average_gold_expectation(public_info, myself)

            if average_gold_gain_if_before > average_gold_gain_if_after or len(characters_after) == 1:
                options = characters_before
            else:
                options = characters_after

            true_options = [x for x in options if x != Character.Assassin]

            if len(true_options) == 0:
                print(characters_after, characters_before, average_gold_gain_if_after, average_gold_gain_if_before)

            return choice(true_options)
        raise ValueError

    def magician(self, public_info: PublicInfo, myself: Player) -> MagicianPower:
        biggest_hand = get_biggest_hand(public_info)

        return SwapHands(biggest_hand[0])

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

    def chance_is_taken(self, character: Character):
        if character in self.role_options:
            return (len(self.role_options) - 2) / (len(self.role_options) - 1)
        else:
            return (7 - len(self.role_options)) / (8 - len(self.role_options))

    def choose_character(self, available_options: List[Character], public_info: PublicInfo, myself: Player) -> int:
        self.role_options = [x for x in available_options]
        role_scores = [0 for _ in available_options]
        for i, role in enumerate(available_options):
            if role == Character.Assassin:
                hc = calculate_hit_chance(len(self.role_options))
                chance_to_hit = max(hc)
                role_scores[i] += chance_to_hit * self.turn_c * (1 / 5)  # premium for killing someone
                chance_is_taken = self.chance_is_taken(Character.Assassin)
                role_scores[i] += chance_is_taken * (47 / 180) * self.turn_c  # premium for not being killed (
                # simplified)
            elif role == Character.Thief:
                ave = self.calculate_average_gold_expectation(public_info, myself)
                average_gold_expectation = max(ave)
                role_scores[i] += (log(myself.gold + average_gold_expectation, self.gold_next_turn) -
                                   log(myself.gold, self.gold_next_turn)) * (6 / 5)  # premium for stealing
                chance_is_taken = self.chance_is_taken(Character.Thief)
                role_scores[i] += chance_is_taken * (47 / 180) * log(myself.gold, self.gold_c)  # premium for not being robbed
            elif role == Character.Magician:
                biggest_hand = get_biggest_hand(public_info)
                role_scores[i] += (log(biggest_hand[1], self.card_c) - log(len(myself.cards), self.card_c)) * (6 / 5)
            elif role == Character.King:
                noble_d = len([x for x in myself.districts if x.district_type == DistrictType.Noble])
                role_scores[i] += log(myself.gold + noble_d, self.gold_c) - log(myself.gold, self.gold_c)  # income
                positions = [x for x in range(len(public_info.player_public_info))]
                my_position = (positions[public_info.crown:] + positions[:public_info.crown]).index(myself.player_id)
                role_scores[i] += self.pos_c * my_position  # Crown value
            elif role == Character.Bishop:
                religious_d = len([x for x in myself.districts if x.district_type == DistrictType.Religious])
                role_scores[i] += log(myself.gold + religious_d, self.gold_c) - log(myself.gold, self.gold_c)  # income
                role_scores[i] += self.protection_c * self.chance_is_taken(Character.Warlord)  # protection
            elif role == Character.Merchant:
                trade_d = len([x for x in myself.districts if x.district_type == DistrictType.Trade])
                role_scores[i] += log(myself.gold + trade_d + 1, self.gold_c) - log(myself.gold, self.gold_c)  # income
            elif role == Character.Architect:
                n_cards = len(myself.cards)
                role_scores[i] += log(n_cards + 2, self.card_c) - log(n_cards, self.card_c)  # cards
                role_scores[i] += self.multi_build_c  # passive
            elif role == Character.Warlord:
                military_d = len([x for x in myself.districts if x.district_type == DistrictType.Military])
                role_scores[i] += log(myself.gold + military_d, self.gold_c) - log(myself.gold, self.gold_c)  # income
                role_scores[i] += self.protection_c * self.chance_is_taken(Character.Warlord)  # protection
                role_scores[i] += self.destruction_c

        highest_score = max(role_scores)
        highest_score_index = role_scores.index(highest_score)
        return highest_score_index
