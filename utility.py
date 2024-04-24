import csv

from models import District, string_type_to_enum


def retrieve_cards():
    cards = []
    with open('database.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for _ in range(int(row['quantity'])):
                cards.append(District(string_type_to_enum(row['type']), int(row['cost']), row['name'].capitalize()))
    return cards
