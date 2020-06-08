from TileAction import TileAction
from Phase import Phase


class GameState:
    def __init__(self, players, board=None, current_tile=None, current_player=None, current_tile_action=None,
                 last_mouse_click_location=None, current_move_action=None, current_phase=None):
        self.board = board  # 2d array of Tiles [rows][columns]
        self.current_tile = current_tile
        self.players = players
        self.current_player = current_player
        self.current_tile_action = current_tile_action
        self.last_mouse_click_location = last_mouse_click_location
        self.current_move_action = current_move_action
        if current_phase is None:
            self.current_phase = Phase.TILE
        else:
            self.current_phase = current_phase

    def previous_player(self):
        index = self.players.index(self.current_player)
        return self.players[(index + len(self.players) - 1) % len(self.players)]

