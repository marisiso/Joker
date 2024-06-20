import random


class Deck:
    lead_suit = ''
    current_cards = {}
    player_cards = {}

    def __init__(self):
        self.deck = []

    def generate_deck(self):
        SUITS = ["clubs", "diamonds", "hearts", "spades"]
        RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6']
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = [rank, suit]
                self.deck.append(card)
        self.deck.append('Joker')
        self.deck.append('Joker')
        self.deck.remove(['6', 'clubs'])
        self.deck.remove(['6', 'spades'])
        random.shuffle(self.deck)
        return self.deck

    def update_current_cards(value):
        Deck.current_cards = value

    def update_player_cards(value):
        Deck.player_cards = value

    def update_lead(value):
        Deck.lead_suit = value

    # generate cards for each player
    def generate_cards_other_players(self, players):
        player_cards = {}
        for player in players:
            cards = random.sample(self.deck, 9)
            for card in cards:
                self.deck.remove(card)
            player_cards[player] = cards
        Deck.update_player_cards(player_cards)
        return player_cards
