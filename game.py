from random import shuffle
from option import Some
from models import Character, Action, EndTurn, Build, Ability, AssassinMarker, ThiefMarker, SwapHands, \
    ChangeCards, DistrictType, Resource, NoTarget
from player import Player
from utility import retrieve_cards, has_all_types, get_engine_by_name, get_order


class Game:
    def __init__(self, num_players):
        self.players = [Player(i) for (i, _) in enumerate(range(num_players))]
        self.deck = retrieve_cards(avoid_special=True)
        self.markers = {}
        self.crowed = 1
        self.finishing_order = []
        self.engines = [get_engine_by_name("random_chooser") for _ in range(num_players)]
        self.turn = 1

        self.deal_cards()
        self.deal_gold()

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
            chosen_id = self.engines[p.player_id].choose_character(characters, public_info)
            p.character = Some(characters.pop(chosen_id))

    def draw(self, player, amount=1):
        for _ in range(amount):
            if len(self.deck) == 0:
                break
            player.cards.append(self.deck.pop())

    def execute_action(self, action: Action, player: Player):
        if isinstance(action, Build):
            player.gold -= action.district.cost
            player.districts.append(player.cards.pop(action.card_id))
            if len(player.districts) == 7:
                self.finishing_order.append(player.player_id)
        elif isinstance(action, Ability):
            player.used_ability = True
            public_info = self.get_public_info()
            engine = self.engines[player.player_id]
            if action.character == Character.Assassin:
                target = engine.choose_target(Character.Assassin, self.get_public_info())
                self.markers.setdefault(target, []).append(AssassinMarker)
            elif action.character == Character.Thief:
                target = engine.choose_target(Character.Thief, self.get_public_info())
                self.markers.setdefault(target, []).append(ThiefMarker)
            elif action.character == Character.Magician:
                mp = engine.magician(public_info, player)
                if isinstance(mp, SwapHands):
                    player.cards, self.players[mp.target].cards = self.players[mp.target].cards, player.cards
                elif isinstance(mp, ChangeCards):
                    to_change = [player.cards[i] for i in range(len(player.cards)) if i in mp.cards]
                    to_keep = [player.cards[i] for i in range(len(player.cards)) if i not in mp.cards]

                    if len(to_change) <= len(self.deck):
                        self.deck += to_change
                        player.cards = to_keep
                        self.draw(player, len(to_change))
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
                w = engine.warlord(self.get_public_info())
                if isinstance(w, NoTarget):
                    return
                player_target = self.players[w.player_id]
                if player_target.character != Character.Bishop and player_target not in self.finishing_order:
                    d = player_target.districts[w.district_id]
                    if player.gold >= d.cost - 1:
                        player.gold -= (d.cost - 1)
                        player_target.districts.pop(w.district_id)
                        self.deck.append(d)

    def play_turns(self):
        ordered_players = sorted(self.players, key=lambda x: get_order(x.character.value))
        for p in ordered_players:
            p.used_ability = False
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
            engine = self.engines[p.player_id]
            chosen_resource = engine.choose_resource(public_info)
            if chosen_resource == Resource.Gold:
                p.gold += 2
            elif chosen_resource == Resource.Cards:
                if len(self.deck) == 0:
                    pass
                elif len(self.deck) == 1:
                    p.cards.append(self.deck.pop())
                    pass
                else:
                    card_1 = self.deck.pop()
                    card_2 = self.deck.pop()
                    chosen_card = engine.choose_card((card_1, card_2), public_info)
                    if chosen_card == 0:
                        p.cards.append(card_1)
                        self.deck.append(card_2)
                    elif chosen_card == 1:
                        p.cards.append(card_2)
                        self.deck.append(card_1)
            built = 0
            while True:
                options = p.generate_actions(built)
                action = engine.choose_action(options, public_info)
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
            self.sanity_check()
            self.turn += 1

    def sanity_check(self):
        total_cards = 54
        cards_in_play = len(self.deck) + sum([len(p.cards) for p in self.players]) + sum([len(p.districts) for p in self.players])
        if cards_in_play != total_cards:
            raise Exception

        for p in self.players:
            if p.gold < 0:
                raise Exception
