from Card import Card
from Objective import Objective
from abc import ABC, abstractmethod

import random


class TestPlayer(ABC):

    current_location: object

    def __init__(self, name, seed):
        self.name = name
        self.cards = None
        self.current_card = None
        self.reachable_tiles = []
        random.seed(seed)

    def update_properties(self, gamestate):
        self.update_reachable_tiles(gamestate)

    def update_reachable_tiles(self, gamestate, possible_routes=None):
        if possible_routes is None:
            possible_routes = self.possible_routes(gamestate, None, [[self.current_location]])
        flat_list = [item for sublist in possible_routes for item in sublist]
        self.reachable_tiles = set(flat_list)


    # def possible_routes(self, gamestate, routes):
    #     for route in routes:
    #         reachable_neighbors = route[-1].reachable_neighbors(gamestate)
    #         for neighbor in reachable_neighbors:
    #             if neighbor not in [r[-1] for r in routes]:
    #                 new_route = route.copy()
    #                 new_route.append(neighbor)
    #                 routes.append(new_route)
    #                 self.possible_routes(gamestate, routes)
    #     return routes

    def possible_routes(self, gamestate, tile, routes):
        for neighbor in tile.reachable_neighbors(gamestate):
            if neighbor not in [r[-1] for r in routes]:
                route = next((r for r in routes if r[-1] == tile), None)
                new_route = route.copy()
                new_route.append(neighbor)
                routes.append(new_route)
                self.possible_routes(gamestate, neighbor, routes)

        return routes

    def route_to_tile(self, tile, gamestate):
        routes = self.possible_routes(gamestate=gamestate, tile=None, routes=[[None]])
        route = next((r for r in routes if r[-1] == tile), None)
        return route

    def deal_cards(self, cards: [Card]):
        self.cards = cards
        self.current_card = cards[0]

    def is_located_at_current_objective(self):
        return self.current_card is not None and None.objective == self.current_card.objective

    def next_card(self):
        new_index = self.cards.index(self.current_card) + 1
        if new_index < len(self.cards):
            self.current_card = self.cards[new_index]
        else:
            self.current_card = None

    def going_back_to_starting_point(self) -> bool:
        return self.current_card is None

    # def is_on_starting_point(self):
    #     if self.current_location.starting_point_color == 'YELLOW':
    #         return self.color.r == 255 and self.color.g == 255
    #     elif self.current_location.starting_point_color == 'RED':
    #         return self.color.r == 255
    #     elif self.current_location.starting_point_color == 'BLUE':
    #         return self.color.b == 255
    #     elif self.current_location.starting_point_color == 'GREEN':
    #         return self.color.g == 255

