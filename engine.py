from abc import ABC, abstractmethod
from typing import List, Tuple
from models import Character, PublicInfo, Resource, District, Action, MagicianPower, WarlordTarget, WarlordOption
from player import Player


class EngineInterface(ABC):
    @abstractmethod
    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        pass

    @abstractmethod
    def choose_resource(self, public_info: List[PublicInfo]) -> Resource:
        pass

    @abstractmethod
    def choose_card(self, cards: List[District], public_info: List[PublicInfo]) -> int:
        pass

    @abstractmethod
    def choose_action(self, options: List[Action], public_info: List[PublicInfo]) -> Action:
        pass

    @abstractmethod
    def choose_target(self, character: Character, public_info: List[PublicInfo]) -> Character:
        pass

    @abstractmethod
    def discard_cards(self, n: int, cards: List[District], public_info: List[PublicInfo]) -> List[int]:
        pass

    @abstractmethod
    def magician(self, public_info: List[PublicInfo], myself: Player) -> MagicianPower:
        pass

    @abstractmethod
    def warlord(self, public_info: List[PublicInfo]) -> WarlordOption:
        pass



