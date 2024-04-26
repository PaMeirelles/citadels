from random import shuffle
from option import Some
from models import Character, Action, EndTurn, Build, Ability, AssassinMarker, ThiefMarker, SwapHands, \
    ChangeCards, DistrictType, Resource, NoTarget, Forge, ThievesLair, PublicInfo
from player import Player
from utility import retrieve_cards, has_all_types, get_engine_by_name, get_order
from stats import Stats


class Game:
    def __init__(self, num_players):
        self.players = [Player(i) for (i, _) in enumerate(range(num_players))]
        self.deck = retrieve_cards()
        self.markers = {}
        self.crowed = 0
        self.finishing_order = []
        self.engines = ([get_engine_by_name("basic_abilities")] +
                        [get_engine_by_name("random_chooser") for _ in range(num_players-1)])
        self.turn = 1
        self.stats = Stats(num_players)

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
        return PublicInfo([p.get_public_info() for p in self.players], self.crowed)

    def role_selection(self):
        characters = list(Character)
        shuffle(characters)
        characters.pop()

        public_info = self.get_public_info()

        for p in self.players[self.crowed:] + self.players[:self.crowed]:
            chosen_id = self.engines[p.player_id].choose_character(characters, public_info)
            p.character = Some(characters.pop(chosen_id))

            self.stats.character_matrix[p.player_id][get_order(p.character.value)-1] += 1

    def draw(self, player, amount=1):
        for _ in range(amount):
            if len(self.deck) == 0:
                break
            player.cards.append(self.deck.pop())

    def execute_action(self, action: Action, player: Player):
        public_info = self.get_public_info()

        if isinstance(action, Build):
            if (action.district.district_type == DistrictType.Special and
                    "Factory" in [x.name for x in player.districts]):
                player.gold += 1
            if isinstance(action, ThievesLair):
                while True:
                    n_cards_to_pay = action.district.cost - action.gold_cost
                    cards_to_pay = self.engines[player.player_id].discard_cards(n_cards_to_pay, player.cards,
                                                                                public_info)
                    if action.card_id not in cards_to_pay:
                        break
                self.deck += [player.cards[i] for i in cards_to_pay]
                player.cards = [player.cards[i] for i in range(len(player.cards)) if i not in cards_to_pay]
                player.gold -= action.gold_cost
                player.cards = [x for x in player.cards if x != action.district]
                self.deck.append(action.district)
            else:
                player.gold -= action.district.cost
                player.districts.append(player.cards.pop(action.card_id))
            if len(player.districts) == 7:
                self.finishing_order.append(player.player_id)
            if action.district.district_type == DistrictType.Special:
                self.stats.special_dict[action.district.name] = player.player_id
        elif isinstance(action, Forge):
            player.gold -= 2
            self.draw(player, 3)
        elif isinstance(action, Ability):
            player.used_ability = True
            engine = self.engines[player.player_id]
            if action.character == Character.Assassin:
                target = engine.choose_target(Character.Assassin, self.get_public_info(), player)
                self.markers.setdefault(target, []).append(AssassinMarker())
            elif action.character == Character.Thief:
                target = engine.choose_target(Character.Thief, self.get_public_info(), player)
                self.markers.setdefault(target, []).append(ThiefMarker(player.player_id))
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
                for card in player.districts:
                    if card.district_type == DistrictType.Noble:
                        player.gold += 1
                if "Magical school" in [x.name for x in player.districts]:
                    player.gold += 1
                self.crowed = player.player_id
            elif action.character == Character.Bishop:
                for card in player.districts:
                    if card.district_type == DistrictType.Religious:
                        player.gold += 1
                if "Magical school" in [x.name for x in player.districts]:
                    player.gold += 1
            elif action.character == Character.Merchant:
                for card in player.districts:
                    if card.district_type == DistrictType.Trade:
                        player.gold += 1
                if "Magical school" in [x.name for x in player.districts]:
                    player.gold += 1
                player.gold += 1
            elif action.character == Character.Architect:
                self.draw(player, 2)
            elif action.character == Character.Warlord:
                for card in player.districts:
                    if card.district_type == DistrictType.Military:
                        player.gold += 1
                if "Magical school" in [x.name for x in player.districts]:
                    player.gold += 1
                w = engine.warlord(self.get_public_info(), player)
                if isinstance(w, NoTarget):
                    return
                player_target = self.players[w.player_id]
                if player_target.character != Character.Bishop and player_target not in self.finishing_order:
                    d = player_target.districts[w.district_id]
                    if player.gold >= d.cost - 1 and d.name != "Keep":
                        player.gold -= (d.cost - 1)
                        player_target.districts.pop(w.district_id)
                        self.deck.append(d)

    def play_turns(self):
        ordered_players = sorted(self.players, key=lambda x: get_order(x.character.value))
        for p in ordered_players:
            p.used_ability = False
            markers = self.markers.get(p.character.value, [])
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
            chosen_resource = engine.choose_resource(public_info, p)
            if chosen_resource == Resource.Gold:
                p.gold += 2
            elif chosen_resource == Resource.Cards:
                if len(self.deck) == 0:
                    pass
                elif len(self.deck) == 1:
                    p.cards.append(self.deck.pop())
                    pass
                else:
                    if "Library" in [x.name for x in p.districts]:
                        self.draw(p, 2)
                    else:
                        if "Laboratory" in [x.name for x in p.districts] and len(self.deck) > 2:
                            card_options = self.deck[:3]
                        else:
                            card_options = self.deck[:2]
                        chosen_card = engine.choose_card(card_options, public_info, p)
                        p.cards.append(self.deck.pop(chosen_card))

            built = 0
            while True:
                options = p.generate_actions(built)
                action = engine.choose_action(options, public_info, p)
                self.execute_action(action, p)
                if isinstance(action, EndTurn):
                    break
                elif isinstance(action, Build):
                    built += 1

    def evaluate(self):
        scores = [0 for _ in self.players]
        for i, p in enumerate(self.players):
            names = set([x.name for x in p.districts])
            for d in p.districts:
                scores[i] += d.cost
            if self.finishing_order[0] == i:
                scores[i] += 4
            elif i in self.finishing_order:
                scores[i] += 2

            if has_all_types(p.districts):
                scores[i] += 2

            if "Dragon's gate" in names:
                scores[i] += 2
            if "Imperial treasure" in names:
                scores[i] += p.gold
            if "Maps room" in names:
                scores[i] += len(p.cards)
            if "Statue" in names and self.crowed == p.player_id:
                scores[i] += 5
            if "Wishing well" in names:
                scores[i] += len([x for x in p.districts if x.district_type == DistrictType.Special])

        return scores

    def play(self):
        while len(self.finishing_order) == 0:
            self.role_selection()
            self.play_turns()
            self.turn += 1
            self.markers = {}
            self.sanity_check()

    def sanity_check(self):
        total_cards = 68
        cards_in_play = (len(self.deck) + sum([len(p.cards) for p in self.players]) +
                         sum([len(p.districts) for p in self.players]))
        if cards_in_play != total_cards:
            raise Exception

        for p in self.players:
            if p.gold < 0:
                raise Exception
