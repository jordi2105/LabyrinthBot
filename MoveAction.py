from Player import Player
from Tile import Tile


class MoveAction:

    def __init__(self, player: Player, route: [Tile], current_tile=None):
        self.player = player
        self.route = route
        if current_tile is None:
            self.current_tile = player.current_location
        else:
            self.current_tile = current_tile

    def next_tile(self, gamestate):
        current_tile_i = self.route.index(self.current_tile)
        self.current_tile = self.route[current_tile_i + 1]
        self.player.current_location = self.current_tile

    def on_last_tile(self):
        return self.current_tile == self.route[-1]
