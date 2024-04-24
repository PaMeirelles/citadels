from abc import ABC, abstractmethod
from typing import List
from models import Character, PublicInfo
from random_chooser import RandomChooser


class EngineInterface(ABC):
    @abstractmethod
    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        pass


def get_engine_by_name(name):
    if name == "random_chooser":
        return RandomChooser()
    else:
        raise ValueError