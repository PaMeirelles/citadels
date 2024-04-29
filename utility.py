import csv
from typing import List

from basic_abilities import BasicAbilities
from basic_consistency import BasicConsistency
from basic_genetic import get_best_basic_genetic
from constants import HAUNTED_NEIGHBORHOOD
from fast_builder import FastBuilder
from models import District, string_type_to_enum, DistrictType, Character
from random_chooser import RandomChooser


def retrieve_cards(avoid_special=False):
    cards = []
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for _ in range(int(row['quantity'])):
                t = string_type_to_enum(row['type'])
                if t == DistrictType.Special and avoid_special: continue
                cards.append(District(t, int(row['cost']), row['name'].capitalize()))
    return cards


def has_all_types(districts: List[District]):
    types = set([x.district_type for x in districts])
    types.discard(DistrictType.Special)

    types_count = len(types)
    if HAUNTED_NEIGHBORHOOD in [x.name for x in districts]:
        types_count += 1

    return types_count >= 4


def get_engine_by_name(name):
    if name == "random_chooser":
        return RandomChooser()
    elif name == "basic_consistency":
        return BasicConsistency()
    elif name == "basic_abilities":
        return BasicAbilities()
    elif name == "fast_builder":
        return FastBuilder()
    elif name == "basic_genetic":
        return get_best_basic_genetic()
    else:
        raise ValueError


def get_order(character: Character):
    if character == Character.Assassin: return 1
    if character == Character.Thief: return 2
    if character == Character.Magician: return 3
    if character == Character.King: return 4
    if character == Character.Bishop: return 5
    if character == Character.Merchant: return 6
    if character == Character.Architect: return 7
    if character == Character.Warlord: return 8
