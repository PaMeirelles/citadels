from abc import ABC, abstractmethod
from typing import List
from models import Character, PublicInfo


class EngineInterface(ABC):
    @abstractmethod
    def choose_character(self, available_options: List[Character], public_info: List[PublicInfo]) -> int:
        pass