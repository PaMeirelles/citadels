from abc import ABC, abstractmethod
from typing import List
from models import Character, PublicInfo, Resource, District, Action, MagicianPower, WarlordTarget
from player import Player
from random_chooser import RandomChooser


class EngineInterface(ABC):
    @abstractmethod
    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        pass

    @abstractmethod
    def choose_resource(self, public_info: List[PublicInfo]) -> Resource:
        pass

    @abstractmethod
    def choose_card(self, cards: (District, District), public_info: List[PublicInfo]) -> int:
        pass

    @abstractmethod
    def choose_action(self, options: List[Action], public_info: List[PublicInfo]) -> Action:
        pass

    @abstractmethod
    def choose_target(self, character: Character, public_info: List[PublicInfo]) -> Character:
        pass

    @abstractmethod
    def magician(self, public_info: List[PublicInfo], myself: Player) -> MagicianPower:
        pass

    @abstractmethod
    def warlord(self, public_info: List[PublicInfo]) -> WarlordTarget:
        pass


def get_engine_by_name(name):
    if name == "random_chooser":
        return RandomChooser()
    else:
        raise ValueError
