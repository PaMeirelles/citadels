from typing import List
from option import Option, NONE, Some
from engine import EngineInterface
from models import Character, District, Resource, Action, WarlordTarget, MagicianPower, SwapHands, \
    ChangeCards, PublicInfo
from random import randint, choice, random, sample
from player import Player


class RandomChooser(EngineInterface):
    def discard_cards(self, n: int, cards: List[District], public_info: PublicInfo, myself: Player) -> List[int]:
        return sample([i for i in range(len(cards))], n)

    def choose_target(self, character: Character, public_info: PublicInfo, myself:Player) -> Character:
        return choice(list(Character))

    def magician(self, public_info: PublicInfo, myself: Player) -> MagicianPower:
        if random() > .5:
            return SwapHands(randint(0, len(public_info.player_public_info)-1))
        else:
            card_ids = [x for x in range(len(myself.cards)) if random() > .5]
            return ChangeCards(card_ids)

    def warlord(self, public_info: PublicInfo, myself: Player) -> Option[WarlordTarget]:
        player_id = randint(0, len(public_info.player_public_info)-1)
        if len(public_info.player_public_info[player_id].districts) == 0:
            return NONE
        district_id = randint(0, len(public_info.player_public_info[player_id].districts)-1)
        return Some(WarlordTarget(player_id, district_id))

    def choose_action(self, options: List[Action], public_info: PublicInfo, myself: Player) -> Action:
        return choice(options)

    def choose_resource(self, public_info: PublicInfo, myself: Player) -> Resource:
        return choice(list(Resource))

    def choose_card(self, cards: List[District], public_info: PublicInfo, myself: Player) -> int:
        return randint(0, len(cards)-1)

    def choose_character(self, available_options: List[Character], public_info: PublicInfo, myself:Player) -> int:
        return randint(0, len(available_options)-1)
