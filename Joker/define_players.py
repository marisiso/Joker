import random


class Players:
    players = []

    def __init__(self, players):
        self.players = players

    # define who is the last player in the game
    def player_sequence(self):
        last_player = random.choice(self.players)
        last_player_index = self.players.index(last_player)
        player_list = self.players[last_player_index + 1:] + self.players[: last_player_index + 1]
        Players.update_players(player_list)
        return player_list

    def update_players(value):
        Players.players = value
