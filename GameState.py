from TileAction import TileAction

class GameState:
    def __init__(self, players, board=None, current_tile=None, current_player=None, current_tile_action=None, last_mouse_click_location=None):
        self.board = board # 2d array of Tiles [rows][columns]
        self.current_tile = current_tile
        self.players = players
        self.current_player = current_player
        self.current_tile_action = current_tile_action
        self.last_mouse_click_location = last_mouse_click_location


