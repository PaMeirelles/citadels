from abc import ABC, abstractmethod
from typing import List
from models import Character, Resource, District, Action, MagicianPower, WarlordTarget, PublicInfo
from player import Player
from option import Option


class EngineInterface(ABC):

    @abstractmethod
    def choose_character(self, available_options: List[Character], public_info: PublicInfo, myself: Player) -> int:
        pass

    @abstractmethod
    def choose_resource(self, public_info: PublicInfo, myself: Player) -> Resource:
        pass

    @abstractmethod
    def choose_card(self, cards: List[District], public_info: PublicInfo, myself: Player) -> int:
        pass

    @abstractmethod
    def choose_action(self, options: List[Action], public_info: PublicInfo, myself: Player) -> Action:
        pass

    @abstractmethod
    def choose_target(self, character: Character, public_info: PublicInfo, myself: Player) -> Character:
        pass

    @abstractmethod
    def discard_cards(self, n: int, cards: List[District], public_info: PublicInfo, myself: Player) -> List[int]:
        pass

    @abstractmethod
    def magician(self, public_info: PublicInfo, myself: Player) -> MagicianPower:
        pass

    @abstractmethod
    def warlord(self, public_info: PublicInfo, myself: Player) -> Option[WarlordTarget]:
        pass
