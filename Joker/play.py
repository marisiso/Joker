import ast
import cards


class Game:
    round_wins = {}
    bids = {}
    last_deal_winner = ''

    def __init__(self, players):
        self.players = players

    # define for players to see cards and bid
    def open_cards_and_bid(self, players):
        bids = {}
        for player in players:
            existing_bids = []
            # rules for first player
            if player == players[0]:
                print(cards.Deck.player_cards[player][0:3])
                choose_suits = ['hearts', 'spades', 'clubs', 'diamonds', 'No Lead']
                while True:
                    try:
                        lead_suit = input("Please select leading suit (hearts, spades, clubs, diamonds or No Lead): ")
                        if lead_suit not in choose_suits:
                            raise ValueError
                        cards.Deck.update_lead(lead_suit)
                        break
                    except ValueError:
                        print("Choose one of these: hearts, spades, clubs, diamonds or No Lead")
                print(cards.Deck.player_cards[player])
                while True:
                    try:
                        bids[player] = int(input(f"{player} please make your bid: "))
                        if bids[player] < 0 or bids[player] > 9:
                            raise ValueError
                        existing_bids.append(bids[player])
                        break
                    except ValueError:
                        print("You must enter integer in range 0-9")
            if player == players[1] or player == players[2]:
                print(cards.Deck.player_cards[player])
                while True:
                    try:
                        bids[player] = int(input(f"{player} please make your bid: "))
                        if bids[player] < 0 or bids[player] > 9:
                            raise ValueError
                        existing_bids.append(bids[player])
                        break
                    except ValueError:
                        print("You must enter integer in range 0-9")
            # rules for last player
            if player == players[3]:
                print(cards.Deck.player_cards[player])
                existing_bids = bids.values()
                sum_existing_bids = 0
                for value in existing_bids:
                    sum_existing_bids += int(value)
                not_available_bid = (9 - sum_existing_bids)
                while True:
                    try:
                        bids[player] = int(input(f"{player} please make your bid, except for {not_available_bid}: "))
                        if bids[player] < 0 or bids[player] > 9 or bids[player] == not_available_bid:
                            raise ValueError
                        break
                    except ValueError:
                        print(f"You must enter integer in range 0-9, except for {not_available_bid}")
        Game.bids = bids
        return f"\nBids are: {bids}\n"

    # define which cards players can play
    def play_card(self, players):
        current_cards2 = {}
        lead_card = []
        for player in players:
            if player == players[0]:
                print(f"{player}'s cards are: {cards.Deck.player_cards[player]}")
                while True:
                    try:
                        current_card = input(f"{player} please select a card to play: ")
                        if current_card == 'Joker':
                            lead_card = ['Joker']
                            current_card = ast.literal_eval(current_card)
                            current_cards2[player] = ['Joker']
                        else:
                            current_card = ast.literal_eval(current_card)
                            lead_card = current_card
                            current_cards2[player] = current_card
                        if current_card not in cards.Deck.player_cards[player]:
                            raise SyntaxError

                        cards.Deck.player_cards[player].remove(current_card)
                        break
                    except SyntaxError:
                        print("Please select card from your cards in correct format (e.g. ['8', 'clubs'] or 'Joker')")

            else:
                print(f"{player}'s cards are: {cards.Deck.player_cards[player]}")
                while True:
                    try:
                        current_card = input(f"{player} please select a card to play: ")
                        current_card = ast.literal_eval(current_card)
                        other_player_suits = []
                        if lead_card == 'Joker':
                            lead_player_suit = None
                        else:
                            lead_player_suit = lead_card[1]
                        for card in cards.Deck.player_cards[player]:
                            player_card_suits = card[1]
                            other_player_suits.append(player_card_suits)

                        if current_card not in cards.Deck.player_cards[player]:
                            raise SyntaxError
                        if current_card != 'Joker' and lead_player_suit is not None:
                            if lead_player_suit in other_player_suits and current_card[1] != lead_player_suit:
                                raise ValueError
                        if current_card != 'Joker' and lead_player_suit is not None:
                            if lead_player_suit not in other_player_suits and cards.Deck.lead_suit in other_player_suits and current_card[1] != cards.Deck.lead_suit:
                                raise Exception

                        current_cards2[player] = current_card
                        cards.Deck.player_cards[player].remove(current_card)
                        break
                    except SyntaxError:
                        print("Please select one card from your cards in correct format (e.g. ['8', 'clubs'])")
                    except ValueError:
                        print(f"You can't play this card! Play the card of {lead_player_suit}!")
                    except Exception:
                        print(f"You can't play this card! Play the card of lead suit!")

        cards.Deck.update_current_cards(current_cards2)
        return "This round's cards are: ", current_cards2

    # define which card wins each deal
    def highest_card(self, players):
        values_rank = {'Joker': 1000, 'A': 14, 'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '8': 8, '7': 7, '6': 6}
        suit_rank = {"clubs": 1, "diamonds": 1, "hearts": 1, "spades": 1}
        card_values = {}
        round_wins2 = {}
        # Use joker_counter to add value to second joker in same deal, so that second joker beats first joker
        joker_counter = 0
        for player in players:
            round_wins2[player] = 0
            card = cards.Deck.current_cards.get(player)
            if card == 'Joker':
                joker_counter += 1
                card_value = values_rank[card] + joker_counter
                card_values[player] = card_value
            if cards.Deck.lead_suit in suit_rank:
                if Game.last_deal_winner:
                    first_player = Game.last_deal_winner
                else:
                    first_player = players[0]

                lead_card = cards.Deck.current_cards.get(first_player)
                if card != 'Joker' and card[1] != cards.Deck.lead_suit and card[1] == lead_card[1]:
                    card_value = (values_rank[card[0]]) * (suit_rank[card[1]])
                    card_values[player] = card_value
                # Ensure that if 2, 3 or 4 player plays card of different suit than first player's, he gets zero points
                if card != 'Joker' and card[1] != cards.Deck.lead_suit and card[1] != lead_card[1]:
                    card_value = (values_rank[card[0]]) * (suit_rank[card[1]]) * 0
                    card_values[player] = card_value
                if card != 'Joker' and card[1] == cards.Deck.lead_suit:
                    card_value = values_rank[card[0]] * suit_rank[card[1]] * 10
                    card_values[player] = card_value
            if cards.Deck.lead_suit == "No Lead":
                if card != 'Joker':
                    if Game.last_deal_winner:
                        first_player = Game.last_deal_winner
                    else:
                        first_player = players[0]
                    lead_card = cards.Deck.current_cards.get(first_player)
                    lead_color = lead_card[1]
                    if card[1] == lead_color:
                        card_value = values_rank[card[0]] * suit_rank[card[1]] * 10
                        card_values[player] = card_value
                    else:
                        card_value = values_rank[card[0]] * suit_rank[card[1]]
                        card_values[player] = card_value
        highest_card = max(card_values.items(), key=lambda key_value_pair: key_value_pair[1])
        Game.last_deal_winner = highest_card[0]
        Game.round_wins[highest_card[0]] += 1
        return f"Player {highest_card[0]} wins this deal!\n"
