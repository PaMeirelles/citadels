from typing import List

from engine import EngineInterface
from models import Character, PublicInfo
from random import randint


class RandomChooser(EngineInterface):
    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        return randint(0, len(available_options))
