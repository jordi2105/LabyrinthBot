from Players.Player import Player
from Players.Bot import Bot
from Players.RandomBot import RandomBot
from TileAction import TileAction
from MoveAction import MoveAction
from HelpFunctions import HelpFunctions

import random


# This Bot is the same as random bot, except that it goes to the objective if the objective is reachable.
class FirstBot(RandomBot):

    def determine_route(self, gamestate):
        routes = self.possible_routes(gamestate, [[self.current_location]])
        all_tiles = [item for sublist in gamestate.board for item in sublist]
        if self.going_back_to_starting_point():
            color_str = HelpFunctions.color_to_str(self.color)
            starting_location_tile = next((t for t in all_tiles if t.starting_point_color == color_str), None)
            route = self.route_to_tile(starting_location_tile, gamestate)
        else:
            tile_with_objective = next((t for t in all_tiles if t.objective == self.current_card.objective), None)
            route = self.route_to_tile(tile_with_objective, gamestate)

        if route is None:
            route = random.choice(routes)

        return route


