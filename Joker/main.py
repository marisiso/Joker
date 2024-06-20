import cards
import define_players
import play
import score_calculation


def main():
    players = []
    for player in range(1, 5):
        while len(players) < 4:
            try:
                player = input(f"Please enter player {len(players)+1} name: ")
                if player not in players:
                    players.append(player)
                else:
                    raise ValueError
                break
            except ValueError:
                print("This name is already taken! Please choose another name")
    print("Welcome to the Joker game! Let's start!")
    play.round_wins = {}
    for player in players:
        play.Game.round_wins[player] = 0
    play.bids = {}
    for player in players:
        play.Game.bids[player] = 0
    all_players = define_players.Players(players)
    players_sequence = all_players.player_sequence()
    score_object = score_calculation.Scoring()
    all_scores = {}
    total_summary_scores = {}
    deserves_bonus_table = {}
    set_bonus = {}
    for player in players:
        set_bonus[player] = 0
    for player in players:
        total_summary_scores[player] = 0
    for j in range(1, 5):
        print(f"\nStart set {j} of four rounds")
        if j == 1:
            print("No scores!")
        else:
            print("Total scores: ", total_summary_scores)
        # reset round_wins for each new set of four rounds
        for player in players:
            play.Game.round_wins[player] = 0

        for i in range(1, 5):
            print(f"\nRound {i}")
            if i == 1:
                players_sequence_round = players_sequence
            else:
                # first player becomes dealer
                players_sequence_round = players_sequence_round[1:] + players_sequence_round[:1]

            if i > 1:
                bonus_check = score_object.deserves_bonus(players_sequence)
                deserves_bonus_table[f"Round {i - 1} bonus check"] = bonus_check
                current_score = score_object.current_hand(players_sequence)
                all_scores[f"Set {j}, Round {i-1} scores"] = current_score
                total_summary_scores = score_object.calculate_total_scores(all_scores)
                # update total scores with bonuses
                if j > 1:
                    for player in players:
                        score = total_summary_scores[player]
                        bonus = set_bonus[player]
                        score_with_bonus = score + bonus
                        total_summary_scores[player] = score_with_bonus
                print("Scores table", all_scores)
                print("Total scores", total_summary_scores)
            print(f"Player {players_sequence_round[3]} deals cards. Player {players_sequence_round[0]} starts the game.")
            deck = cards.Deck()
            deck.generate_deck()
            deck.generate_cards_other_players(players_sequence_round)
            print(f"All players have 9 cards. Let's open 3 cards for player {players_sequence_round[0]}")
            card = play.Game(players_sequence_round)
            print(card.open_cards_and_bid(players_sequence_round))
            for a in range(9):
                if a == 0:
                    players_sequence_deal = players_sequence_round
                else:
                    # last deal winner starts play
                    k = players_sequence_round.index(play.Game.last_deal_winner)
                    players_sequence_deal = players_sequence_round[k:] + players_sequence_round[:k]
                print(card.play_card(players_sequence_deal))
                print(card.highest_card(players_sequence_deal))
            print("round wins: ", play.Game.round_wins)
            print("round bids: ", play.Game.bids)
            print("End of round")

            if i == 4:
                bonus_check = score_object.deserves_bonus(players_sequence)
                deserves_bonus_table[f"Round {i} bonus check"] = bonus_check
                current_score = score_object.current_hand(players_sequence)
                all_scores[f"Set {j}, Round {i} scores"] = current_score
                total_summary_scores = score_object.calculate_total_scores(all_scores)
                if j > 1:
                    for player in players:
                        score = total_summary_scores[player]
                        bonus = set_bonus[player]
                        score_with_bonus = score + bonus
                        total_summary_scores[player] = score_with_bonus

        print("Scores table", all_scores)
        print("End of 4 rounds. Let's see the total scores: ", total_summary_scores)

        bonus_summary = {}
        for player in players:
            bonus_summary[player] = 0

        for round_bonus in deserves_bonus_table.values():
            for player, points in round_bonus.items():
                bonus_summary[player] += points

        for player, points in bonus_summary.items():
            if points == 4:
                highest_score = 0
                for round_n, scores_info in all_scores.items():
                    if player in scores_info["Players"]:
                        player_index = scores_info["Players"].index(player)
                        player_score = scores_info['Scores'][player_index]
                        highest_score = max(highest_score, player_score)
                total_summary_scores[player] += highest_score
                set_bonus[player] = highest_score

                print(f"Player {player} deserves bonus of {highest_score}")
        print("Total scores including bonuses: ", total_summary_scores)
    print("End of game. Let's see the final scores: ", total_summary_scores)
    winner = max(total_summary_scores.items(), key=lambda item: item[1])
    print(f"The winner is player {winner}!!!")


if __name__ == "__main__":
    main()
