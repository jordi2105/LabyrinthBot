import Card
from abc import ABC, abstractmethod
from Tile import Tile

import pygame as p


class Player(ABC):

    def __init__(self, name, current_location: Tile, color: p.Color):
        self.name = name
        self.current_location = current_location
        self.color = color

    def reachable_tiles(self, gamestate, tile, reachable_tiles):
        reachable_neighbors = tile.reachable_neighbors(gamestate)
        for neighbor in reachable_neighbors:
            if neighbor not in reachable_tiles:
                reachable_tiles.append(neighbor)
                self.reachable_tiles(gamestate, neighbor, reachable_tiles)

        return reachable_tiles

        #
        # for tile in reachable_tiles:
        #     neighbors = tile.reachable_neighbors()
        #     reachable_neighbors = []
        #     for neighbor in neighbors:
        #         if neighbor not in reachable_tiles:
        #             reachable_neighbors.append(neighbor)
        # for reachable_neighbor in self.current_location.reachable_neighbors():
        #     if reachable_neighbor not in reachable_tiles:
        #         tiles.append(reachable_neighbor)
        # if not tiles: # If tiles is empty
        #     return []
        # else:
        #     reachable_tiles.extend(tiles)
        #     return reachable_tiles(gamestate, reachable_tiles)

    @abstractmethod
    def do_turn(self, gamestate):
        pass
