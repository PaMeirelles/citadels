from typing import List

from engine import EngineInterface
from models import Character, PublicInfo, District, Resource, Action, WarlordTarget, MagicianPower, SwapHands, \
    ChangeCards
from random import randint, choice, random

from player import Player


class RandomChooser(EngineInterface):
    def choose_target(self, character: Character, public_info: List[PublicInfo]) -> Character:
        return choice(list(Character))

    def magician(self, public_info: List[PublicInfo], myself: Player) -> MagicianPower:
        if random() > .5:
            return SwapHands(randint(0, len(public_info)))
        else:
            card_ids = [x for x in range(len(myself.cards)) if random() > .5]
            return ChangeCards(card_ids)

    def warlord(self, public_info: List[PublicInfo]) -> WarlordTarget:
        player_id = randint(0, len(public_info))
        district_id = randint(0, len(public_info[player_id].districts))
        return WarlordTarget(player_id, district_id)

    def choose_action(self, options: List[Action], public_info: List[PublicInfo]) -> Action:
        return choice(options)

    def choose_resource(self, public_info: List[PublicInfo]) -> Resource:
        return choice(list(Resource))

    def choose_card(self, cards: (District, District), public_info: List[PublicInfo]) -> int:
        return randint(0, 2)

    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        return randint(0, len(available_options))
