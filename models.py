from enum import Enum
from dataclasses import dataclass
from typing import List


class DistrictType(Enum):
    Trade = 0
    Military = 1
    Religious = 2
    Noble = 3
    Special = 4


def string_type_to_enum(str_type):
    str_type = str_type.lower()
    if str_type == 'trade':
        return DistrictType.Trade
    elif str_type == 'military':
        return DistrictType.Military
    elif str_type == 'religious':
        return DistrictType.Religious
    elif str_type == 'noble':
        return DistrictType.Noble
    elif str_type == 'special':
        return DistrictType.Special
    else:
        raise ValueError("Invalid district type")


class Character(Enum):
    Assassin = 1
    Thief = 2
    Magician = 3
    King = 4
    Bishop = 5
    Merchant = 6
    Architect = 7
    Warlord = 8


class Resource(Enum):
    Gold = 1
    Cards = 2


@dataclass
class District:
    district_type: DistrictType
    cost: int
    name: str


@dataclass
class PublicInfo:
    gold: int
    num_cards: int
    districts: List[District]


@dataclass
class Action:
    pass


@dataclass
class Build(Action):
    district: District
    card_id: int


@dataclass
class Ability(Action):
    character: Character


@dataclass
class EndTurn(Action):
    pass


@dataclass
class Marker:
    pass


@dataclass
class AssassinMarker(Marker):
    pass


@dataclass
class ThiefMarker(Marker):
    player_id: int


@dataclass
class MagicianPower:
    pass


@dataclass
class SwapHands(MagicianPower):
    target: int


@dataclass
class ChangeCards(MagicianPower):
    cards: List[int]


@dataclass
class WarlordTarget:
    player_id: int
    district_id: int
