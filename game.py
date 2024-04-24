from random import shuffle

from option import Some

from models import Character, Action, EndTurn, Build, Ability, AssassinMarker, ThiefMarker, SwapHands, \
    ChangeCards, DistrictType
from player import Player
from utility import retrieve_cards, has_all_types


class Game:
    def __init__(self, num_players):
        self.players = [Player(i, "random_chooser") for (i, _) in enumerate(range(num_players))]
        self.deck = retrieve_cards(True)
        self.deal_cards()
        self.deal_gold()

        self.markers = {}
        self.crowed = 1
        self.finishing_order = []

    def deal_cards(self):
        shuffle(self.deck)
        for p in self.players:
            self.draw(p, 4)

    def deal_gold(self):
        for p in self.players:
            p.gold = 2

    def get_public_info(self):
        return [p.get_public_info() for p in self.players]

    def role_selection(self):
        characters = list(Character)
        shuffle(characters)
        characters.pop()

        public_info = self.get_public_info()

        for p in self.players[self.crowed:] + self.players[:self.crowed]:
            chosen_id = p.engine.choose_character(characters, public_info)
            p.character = Some(characters.pop(chosen_id))

    def draw(self, player, amount=1):
        for _ in range(amount):
            player.cards.append(self.deck.pop())

    def execute_action(self, action: Action, player):
        if isinstance(action, Build):
            player.gold -= action.district.cost
            player.cards.pop(action.card_id)
            if len(player.districts) == 7:
                self.finishing_order.append(player.player_id)
        elif isinstance(action, Ability):
            if action.character == Character.Assassin:
                target = player.engine.choose_target(Character.Assassin, self.get_public_info())
                self.markers.setdefault(target, []).append(AssassinMarker)
            elif action.character == Character.Thief:
                target = player.engine.choose_target(Character.Thief, self.get_public_info())
                self.markers.setdefault(target, []).append(ThiefMarker)
            elif action.character == Character.Magician:
                mp = player.engine.magician()
                if isinstance(mp, SwapHands):
                    player.cards, self.players[mp.target].cards = self.players[mp.target].cards, player.cards
                elif isinstance(mp, ChangeCards):
                    for card_id in mp.cards:
                        self.deck.append(player.cards.pop(card_id))
                        self.draw(player)
            elif action.character == Character.King:
                for card in player.cards:
                    if card.district_type == DistrictType.Noble:
                        player.gold += 1
                self.crowed = player.player_id
            elif action.character == Character.Bishop:
                for card in player.cards:
                    if card.district_type == DistrictType.Religious:
                        player.gold += 1
            elif action.character == Character.Merchant:
                for card in player.cards:
                    if card.district_type == DistrictType.Trade:
                        player.gold += 1
                player.gold += 1
            elif action.character == Character.Architect:
                self.draw(player, 2)
            elif action.character == Character.Warlord:
                wt = player.engine.warlord(self.get_public_info())
                player_target = self.players[wt.player_id]
                if player_target.character != Character.Bishop and player_target not in self.finishing_order:
                    player.gold -= (player_target.districts.pop(wt.district_id).cost + 1)

    def play_turns(self):
        self.players.sort(key=lambda x: x.character.value)
        for p in self.players:
            markers = self.markers.get(p.character, [])
            killed = False
            for m in markers:
                if isinstance(m, AssassinMarker):
                    killed = True
                    break
                elif isinstance(m, ThiefMarker):
                    self.players[m.player_id].gold += p.gold
                    p.gold = 0

            if killed:
                continue

            public_info = self.get_public_info()
            built = 0
            while True:
                options = p.generate_actions(built)
                action = p.engine.choose_action(options, public_info)
                self.execute_action(action, p)
                if isinstance(action, EndTurn):
                    break
                elif isinstance(action, Build):
                    built += 1

    def evaluate(self):
        scores = [0 for _ in self.players]
        for i, p in enumerate(self.players):
            for d in p.districts:
                scores[i] += d.cost
            if self.finishing_order[0] == i:
                scores[i] += 4
            elif i in self.finishing_order:
                scores[i] += 2

            if has_all_types(p.districts):
                scores[i] += 2
        return scores

    def play(self):
        while len(self.finishing_order) == 0:
            self.role_selection()
            self.play_turns()
