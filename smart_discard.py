from typing import List

from fast_builder import FastBuilder
from models import District, PublicInfo, DistrictType
from player import Player


def rate_cards(cards, myself, cheapest=False):
    card_scores = [[0, i] for i in range(len(cards))]
    names_built = set([x.name for x in myself.districts])
    types_built = set([x.district_type for x in myself.districts])

    if cheapest:
        price_mod = -1
    else:
        price_mod = 1

    for i, c in enumerate(cards):
        if c.name in names_built:
            card_scores[i][0] -= 100
        if c.district_type not in types_built and c.district_type != DistrictType.Special:
            card_scores[i][0] += 10
        card_scores[i][0] += c.cost * price_mod

    return card_scores


class SmartDiscard(FastBuilder):
    def __init__(self):
        super().__init__()

    def discard_cards(self, n: int, cards: List[District], public_info: PublicInfo, myself: Player) -> List[int]:
        card_scores = rate_cards(cards, myself)

        card_scores.sort(key=lambda x: x[0])
        return [x[1] for x in card_scores[:n]]

    def choose_card(self, cards: List[District], public_info: PublicInfo, myself: Player) -> int:
        can_afford = []
        cant_afford = []
        for c in cards:
            if c.cost <= myself.gold:
                can_afford.append(c)
            else:
                cant_afford.append(c)
        if len(can_afford) > 0:
            options = can_afford
            cheapest = False
        else:
            options = cant_afford
            cheapest = True

        card_scores = rate_cards(options, myself, cheapest=cheapest)
        card_scores.sort(key=lambda x: x[0])
        card = options[card_scores[-1][1]]
        return cards.index(card)
