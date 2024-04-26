from typing import List

from genetic import Genetic, calculate_hit_chance, get_biggest_hand
from models import Character, PublicInfo, DistrictType
from player import Player


def get_best_basic_genetic():
    best_genes = [0.9783701214983467, 0.9665306151785001, 0.6122460569228687, 1.0678189251978236, 0.3282948123261767,
                  0.599630362630095, 1.1112367557854417, 0.25914538633473455]

    return BasicGenetic(best_genes[0], best_genes[1], best_genes[2], best_genes[3], best_genes[4], best_genes[5],
                        best_genes[6], best_genes[7])


class BasicGenetic(Genetic):
    def __init__(self, aw, tw, mw, gw, bw, cw, qw, ww):
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
                ave = self.calculate_average_gold_expectation(public_info, myself)
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
