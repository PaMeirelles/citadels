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








