from Action import Action

class GameState:
    def __init__(self, players, board=None, current_tile=None, player_in_turn=None, current_action=None):
        self.board = board # 2d array of Tiles
        self.current_tile = current_tile
        self.players = players
        self.player_in_turn = players[0]
        self.current_action = current_action

