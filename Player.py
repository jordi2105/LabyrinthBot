import Card
from abc import ABC, abstractmethod
from Tile import Tile

import pygame as p


class Player(ABC):

    def __init__(self, name, current_location: Tile, color: p.Color):
        self.name = name
        self.current_location = current_location
        self.color = color

    def possible_routes(self, gamestate, routes):
        for route in routes:
            reachable_neighbors = route[-1].reachable_neighbors(gamestate)
            for neighbor in reachable_neighbors:
                if neighbor not in [r[-1] for r in routes]:
                    new_route = route.copy()
                    new_route.append(neighbor)
                    routes.append(new_route)
                    self.possible_routes(gamestate, routes)
        return routes

    def reachable_tiles(self, gamestate, possible_routes=None):
        if possible_routes is None:
            possible_routes = self.possible_routes(gamestate, [[self.current_location]])
        flat_list = [item for sublist in possible_routes for item in sublist]
        return set(flat_list)

    def route_to_tile(self, tile, gamestate):
        routes = self.possible_routes(gamestate, [[self.current_location]])
        route = next((r for r in routes if r[-1] == tile), None)
        return route




        #
        # reachable_neighbors = tile.reachable_neighbors(gamestate)
        # for neighbor in reachable_neighbors:
        #     if neighbor not in reachable_tiles:
        #         reachable_tiles.append(neighbor)
        #         self.reachable_tiles(gamestate, neighbor, reachable_tiles)
        #
        # return routes

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
