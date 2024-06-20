import play


class Scoring:
    player_score = {}
    score_table = {}

    # calculate scores of each round
    def current_hand(self, players):
        round_wins = play.Game.round_wins
        bids = play.Game.bids
        round_scores = {}
        for player in players:
            round_scores[player] = 0
        for player in players:
            if round_wins[player] == bids[player]:
                if bids[player] == 0:
                    score = 50
                    round_scores[player] = score
                elif bids[player] == 9:
                    score = 900
                    round_scores[player] = score
                else:
                    score = 50 + round_wins[player] * 50
                    round_scores[player] = score
            if round_wins[player] > bids[player]:
                score = round_wins[player] * 10
                round_scores[player] = score
            if round_wins[player] < bids[player]:
                if round_wins[player] > 0:
                    score = round_wins[player]*10
                    round_scores[player] = score
                if round_wins[player] == 0:
                    score = -500
                    round_scores[player] = score
        # store results of bids and scores per player in dictionary
        score_dict = {
            "Players": players,
            "Bids": [bids[player] for player in players],
            "Scores": [round_scores[player] for player in players]
        }

        Scoring.score_table = score_dict
        for player in players:
            Scoring.player_score[player] = round_scores[player]

        round_score_values = round_scores.values()
        for value in round_wins:
            if sum(round_score_values) > 9:
                round_wins[value] = 0

        # reset round_win values to zero after each deal
        for player in players:
            play.Game.round_wins[player] = 0

        return score_dict

    def calculate_total_scores(self, score_table):
        total_scores = {}
        # Iterate through each round's scores in the scores_table
        for round_scores in score_table.values():
            players = round_scores['Players']
            scores = round_scores['Scores']
            for i in range(len(players)):
                player = players[i]
                score = scores[i]
                if player in total_scores:
                    total_scores[player] += score
                else:
                    total_scores[player] = score
        return total_scores

    # determine if player deserves bonus
    def deserves_bonus(self, players):
        round_wins = play.Game.round_wins
        bids = play.Game.bids
        bonus_table = {}
        for player in players:
            if round_wins[player] == bids[player]:
                bonus_table[player] = 1
            else:
                bonus_table[player] = 0
        return bonus_table
