from Objective import Objective
from Tile import Tile
from TileType import TileType
from HelpFunctions import HelpFunctions

import random


class Generator(object):

    @staticmethod
    def generate_tiles() -> [Tile]:
        # First get all tiles with an objective
        tiles = []
        images_directory = 'tile_images/'
        for obj in Objective:
            file_name = images_directory + obj.name + '.jpg'
            type = None
            if obj in [Objective.BAG_OF_GOLD_COINS,
                            Objective.BAT,
                            Objective.BOOK,
                            Objective.DRAGON,
                            Objective.GHOST_IN_BOTTLE,
                            Objective.GHOST_WAVING,
                            Objective.GOLD_CROWN,
                            Objective.GOLD_MENORAH,
                            Objective.GOLD_RING,
                            Objective.HELMET,
                            Objective.JEWEL,
                            Objective.LADY_PIG,
                            Objective.SET_OF_KEYS,
                            Objective.SKULL,
                            Objective.SORCERESS,
                            Objective.SWORD,
                            Objective.TREASURE_CHEST,
                            Objective.TREASURE_MAP]:
                type = TileType.THREE_WAY
            elif obj in [Objective.LIZARD,
                              Objective.MOTH,
                              Objective.OWL,
                              Objective.RAT,
                              Objective.SCARAB,
                              Objective.SPIDER]:
                type = TileType.CURVED

            tile = Tile(type, file_name, obj)
            tiles.append(tile)

        # The starting points tiles
        for color in ['YELLOW', 'BLUE', 'RED', 'GREEN']:
            file_name = images_directory + color + '_STARTING_POINT.jpg'
            type = TileType.CURVED
            tile = Tile(type, file_name, starting_point_color=color)
            tiles.append(tile)

        # The straight tiles
        for i in range(0, 13):
            file_name = images_directory + 'STRAIGHT.jpg'
            type = TileType.STRAIGHT
            tile = Tile(type, file_name)
            tiles.append(tile)

        # The curved tiles
        for i in range(0, 9):
            file_name = images_directory + 'CURVED.jpg'
            type = TileType.CURVED
            tile = Tile(type, file_name)
            tiles.append(tile)

        return tiles

    @staticmethod
    def generate_default_board() -> ([[Tile]], [Tile]):
        w = 7
        h = 7
        board = [[0 for x in range(w)] for y in range(h)]
        tiles = Generator.generate_tiles()

        board[0][0] = next(t for t in tiles if t.starting_point_color == 'RED')
        board[0][0].open_sides = [False, True, True, False]
        board[0][6] = next(t for t in tiles if t.starting_point_color == 'YELLOW')
        board[0][6].open_sides = [False, False, True, True]
        board[6][0] = next(t for t in tiles if t.starting_point_color == 'GREEN')
        board[6][0].open_sides = [True, True, False, False]
        board[6][6] = next(t for t in tiles if t.starting_point_color == 'BLUE')

        board[0][2] = next(t for t in tiles if t.objective == Objective.BOOK)
        board[0][4] = next(t for t in tiles if t.objective == Objective.BAG_OF_GOLD_COINS)

        board[2][0] = next(t for t in tiles if t.objective == Objective.TREASURE_MAP)
        board[2][0].open_sides = [True, True, True, False]
        board[2][2] = next(t for t in tiles if t.objective == Objective.GOLD_CROWN)
        board[2][4] = next(t for t in tiles if t.objective == Objective.SET_OF_KEYS)
        board[2][4].open_sides = [False, True, True, True]
        board[2][6] = next(t for t in tiles if t.objective == Objective.SKULL)
        board[2][6].open_sides = [True, False, True, True]

        board[4][0] = next(t for t in tiles if t.objective == Objective.GOLD_RING)
        board[4][0].open_sides = [True, True, True, False]
        board[4][2] = next(t for t in tiles if t.objective == Objective.TREASURE_CHEST)
        board[4][4] = next(t for t in tiles if t.objective == Objective.JEWEL)
        board[4][4].open_sides = [True, False, True, True]
        board[4][6] = next(t for t in tiles if t.objective == Objective.SWORD)
        board[4][6].open_sides = [True, False, True, True]

        board[6][2] = next(t for t in tiles if t.objective == Objective.GOLD_MENORAH)
        board[6][4] = next(t for t in tiles if t.objective == Objective.HELMET)

        for r in range(7):
            for c in range(7):
                tile = board[r][c]
                if tile is not 0:
                    used_tile = [t for t in tiles if t.objective == tile.objective][0]
                    tiles.remove(used_tile)

        return board, tiles #Tiles left

    @staticmethod
    def generate_random_full_board() -> ([[Tile]], Tile):
        seed = 3877926#random.randint(0, 100000000)
        print(seed)
        random.seed(seed)

        board, tiles_left = Generator.generate_default_board()

        for r in range(7):
            for c in range(7):
                if board[r][c] is 0:
                    tile = random.choice(tiles_left)
                    board[r][c] = tile
                    tiles_left.remove(tile)
        return board, tiles_left[0]

    @staticmethod
    def place_tiles_on_board(board: [[Tile]], tiles: Tile, location: (int, int)):

        for i, tile in enumerate(tiles):
            tile_old_location = HelpFunctions.get_location_of_tile(board, tile)
            r_old = tile_old_location[0]
            c_old = tile_old_location[1]
            r = location[i][0]
            c = location[i][1]
            old_tile = board[r][c]
            board[r][c] = tile

            board[r_old][c_old] = old_tile






