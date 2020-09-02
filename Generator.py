from Objective import Objective
from Tile import Tile
from TileType import TileType
from HelpFunctions import HelpFunctions
from Card import Card
from Players.Player import Player

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
        board[0][0].turn_clock_wise(2)
        board[0][6] = next(t for t in tiles if t.starting_point_color == 'YELLOW')
        board[0][6].turn_clock_wise(3)
        board[6][0] = next(t for t in tiles if t.starting_point_color == 'GREEN')
        board[6][0].turn_clock_wise(1)
        board[6][6] = next(t for t in tiles if t.starting_point_color == 'BLUE')

        board[0][2] = next(t for t in tiles if t.objective == Objective.BOOK)
        board[0][4] = next(t for t in tiles if t.objective == Objective.BAG_OF_GOLD_COINS)

        board[2][0] = next(t for t in tiles if t.objective == Objective.TREASURE_MAP)
        board[2][0].turn_clock_wise(1)
        board[2][2] = next(t for t in tiles if t.objective == Objective.GOLD_CROWN)
        board[2][4] = next(t for t in tiles if t.objective == Objective.SET_OF_KEYS)
        board[2][4].turn_clock_wise(2)
        board[2][6] = next(t for t in tiles if t.objective == Objective.SKULL)
        board[2][6].turn_clock_wise(3)

        board[4][0] = next(t for t in tiles if t.objective == Objective.GOLD_RING)
        board[4][0].turn_clock_wise(1)
        board[4][2] = next(t for t in tiles if t.objective == Objective.TREASURE_CHEST)
        board[4][4] = next(t for t in tiles if t.objective == Objective.JEWEL)
        board[4][4].turn_clock_wise(3)
        board[4][6] = next(t for t in tiles if t.objective == Objective.SWORD)
        board[4][6].turn_clock_wise(3)

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
    def generate_random_full_board(seed) -> ([[Tile]], Tile):
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

    @staticmethod
    def deal_cards(players: [Player], nr_of_cards_pp=None, predefined_objectives=None):
        images_directory = 'card_images/'
        if predefined_objectives:
            for i, objectives in enumerate(predefined_objectives):
                cards = []
                for objective in objectives:
                    file_name_url = images_directory + objective.name + '.jpg'
                    card = Card(objective, file_name_url)
                    cards.append(card)
                players[i].deal_cards(cards)
            return

        cards = []
        for obj in Objective:
            if 'STARTING_POINT' not in obj.name:
                file_name_url = images_directory + obj.name + '.jpg'
                card = Card(obj, file_name_url)
                cards.append(card)

        random.shuffle(cards)
        n = len(cards)
        if nr_of_cards_pp is None:
            nr_of_cards_pp = int(n/len(players))

        for i in range(0, len(players)):
            first_card_i = i*nr_of_cards_pp
            last_card_i = first_card_i + nr_of_cards_pp
            p_cards = cards[first_card_i:last_card_i]
            players[i].deal_cards(p_cards)


    # Adjustments: a list of (row, column, url, nr of rotations)
    @staticmethod
    def adjust_board(gamestate, adjustments: [(int, int, str, int)]):
        board = gamestate.board
        for (row, column, url, rotation_n) in adjustments:
            tile = HelpFunctions.get_tile_by_url(board, url)
            tile.turn_clock_wise(rotation_n)
            old_tile = board[row][column]
            board[row][column] = tile
            board[tile.row][tile.column] = old_tile












