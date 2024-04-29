from typing import List, Tuple

from basic_abilities import BasicAbilities
from models import Character, PublicInfo, DistrictType
from player import Player

BEST_GENES = [0.9783701214983467, 0.9665306151785001, 0.6122460569228687, 1.0678189251978236, 0.3282948123261767,
              0.599630362630095, 1.1112367557854417, 0.25914538633473455]


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


def get_best_basic_genetic():
    return BasicGenetic(BEST_GENES[0], BEST_GENES[1], BEST_GENES[2], BEST_GENES[3], BEST_GENES[4], BEST_GENES[5],
                        BEST_GENES[6], BEST_GENES[7])


def calculate_average_gold_expectation(public_info, myself) -> Tuple[float, float]:
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


class BasicGenetic(BasicAbilities):
    def __init__(self, aw, tw, mw, gw, bw, cw, qw, ww):
        super().__init__()
        self.aw = aw
        self.tw = tw
        self.mw = mw
        self.gw = gw
        self.cw = cw
        self.qw = qw
        self.bw = bw
        self.ww = ww

    def choose_character(self, available_options: List[Character], public_info: PublicInfo, myself: Player) -> int:
        self.role_options = [x for x in available_options]
        role_scores = [0 for _ in available_options]
        for i, role in enumerate(available_options):
            if role == Character.Assassin:
                hc = calculate_hit_chance(len(self.role_options))
                chance_to_hit = max(hc)
                role_scores[i] += chance_to_hit * self.aw
            elif role == Character.Thief:
                ave = calculate_average_gold_expectation(public_info, myself)
                average_gold_expectation = max(ave)
                role_scores[i] += average_gold_expectation * self.tw
            elif role == Character.Magician:
                biggest_hand = get_biggest_hand(public_info)
                role_scores[i] += (biggest_hand[1] - len(myself.cards)) * self.mw

            elif role == Character.King:
                noble_d = len([x for x in myself.districts if x.district_type == DistrictType.Noble])
                role_scores[i] += noble_d * self.gw
                role_scores[i] += self.cw
            elif role == Character.Bishop:
                religious_d = len([x for x in myself.districts if x.district_type == DistrictType.Religious])
                role_scores[i] += religious_d * self.gw + self.bw
            elif role == Character.Merchant:
                trade_d = len([x for x in myself.districts if x.district_type == DistrictType.Trade])
                role_scores[i] += (1 + trade_d) * self.gw
            elif role == Character.Architect:
                role_scores[i] += self.qw
            elif role == Character.Warlord:
                military_d = len([x for x in myself.districts if x.district_type == DistrictType.Military])
                role_scores[i] += military_d * self.gw  # income
                role_scores[i] += self.ww

        highest_score = max(role_scores)
        highest_score_index = role_scores.index(highest_score)
        return highest_score_index
