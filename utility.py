import csv
from typing import List

from models import District, string_type_to_enum, DistrictType


def retrieve_cards(avoid_special=False):
    cards = []
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for _ in range(int(row['quantity'])):
                t = string_type_to_enum(row['type'])
                if type == DistrictType.Special and avoid_special: continue
                cards.append(District(t, int(row['cost']), row['name'].capitalize()))
    return cards


def has_all_types(districts: List[District]):
    types = set([x.district_type for x in districts])
    return (DistrictType.Trade in types and DistrictType.Religious in types and DistrictType.Noble in types and
            DistrictType.Military in types)
