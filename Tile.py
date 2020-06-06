from TileType import TileType
from Objective import Objective


class Tile:

    def __init__(self, tile_type: TileType, image_file_url: str, objective: Objective = None,
                 starting_point_color=None):
        self.type = tile_type
        self.objective = objective
        self.image_file_url = image_file_url
        self.on_board = False
        self.starting_point_color = starting_point_color
        self.open_sides = self.initialize_open_sides()

    def initialize_open_sides(self):
        # open_sides: top, right, bottom, left
        if self.type == TileType.STRAIGHT:
            return [True, False, True, False]
        elif self.type == TileType.CURVED:
            return [True, False, False, True]
        elif self.type == TileType.THREE_WAY:
            return [True, True, False, True]
