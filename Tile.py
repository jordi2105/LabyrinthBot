from TileType import TileType
from Objective import Objective
from HelpFunctions import HelpFunctions

import pygame as p


class Tile:

    def __init__(self, tile_type: TileType, image_file_url: str, objective: Objective = None,
                 starting_point_color=None):
        self.type = tile_type
        self.objective = objective
        self.image_file_url = image_file_url
        self.starting_point_color = starting_point_color
        self._open_sides = self.initialize_open_sides()
        self.reachability_mark = False

        image = p.image.load(image_file_url)
        self.image = p.transform.scale(image, (80, 80))
        self.rotate_image_using_open_sides()


    def initialize_open_sides(self):
        # open_sides: top, right, bottom, left
        if self.type == TileType.STRAIGHT:
            return [True, False, True, False]
        elif self.type == TileType.CURVED:
            return [True, False, False, True]
        elif self.type == TileType.THREE_WAY:
            return [True, True, False, True]

    def turn_clock_wise(self):
        a = 1 % len(self.open_sides)
        self.open_sides = self._open_sides[-a:] + self._open_sides[:-a]

    def reachable_neighbors(self, gamestate):
        board = gamestate.board
        r, c = HelpFunctions.get_location_of_tile(board, self)
        reachable_neighbors = []
        if r > 0:
            neighbor = board[r - 1][c]
            if self._open_sides[0] and neighbor.open_sides[2]:
                reachable_neighbors.append(neighbor)
        if r < 6:
            neighbor = board[r + 1][c]
            if self._open_sides[2] and neighbor.open_sides[0]:
                reachable_neighbors.append(neighbor)
        if c > 0:
            neighbor = board[r][c - 1]
            if self._open_sides[3] and neighbor.open_sides[1]:
                reachable_neighbors.append(neighbor)
        if c < 6:
            neighbor = board[r][c + 1]
            if self._open_sides[1] and neighbor.open_sides[3]:
                reachable_neighbors.append(neighbor)

        return reachable_neighbors

    def rotate_image_using_open_sides(self):
        if self.type == TileType.STRAIGHT:
            if not self._open_sides[0]:
                self.image = p.transform.rotate(self.image, 90)
        elif self.type == TileType.CURVED:
            if self._open_sides == [True, True, False, False]:
                self.image = p.transform.rotate(self.image, 270)
            elif self._open_sides == [False, True, True, False]:
                self.image = p.transform.rotate(self.image, 180)
            elif self._open_sides == [False, False, True, True]:
                self.image = p.transform.rotate(self.image, 90)
        elif self.type == TileType.THREE_WAY:
            if not self._open_sides[3]:
                self.image = p.transform.rotate(self.image, 270)
            elif not self._open_sides[0]:
                self.image = p.transform.rotate(self.image, 180)
            elif not self._open_sides[1]:
                self.image = p.transform.rotate(self.image, 90)

    @property
    def open_sides(self):
        return self._open_sides

    @open_sides.setter
    def open_sides(self, open_sides):
        self._open_sides = open_sides
        self.rotate_image_using_open_sides()

