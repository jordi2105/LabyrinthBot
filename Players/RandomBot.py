from Players.Player import Player
from Players.Bot import Bot
from TileAction import TileAction
from MoveAction import MoveAction

import random


class RandomBot(Bot):

    def determine_side_and_index_and_rotation(self, gamestate) -> (str, int):
        self.turn_tile_randomly(gamestate)
        index = random.choice([1, 3, 5])
        side = random.choice(['top', 'bottom', 'left', 'right'])
        return side, index

    def turn_tile_randomly(self, gamestate):
        n = random.randint(0, 3)
        gamestate.current_tile.turn_clock_wise(n)


    def determine_route(self, gamestate):
        routes = self.possible_routes(gamestate, [[self.current_location]])
        random_route = random.choice(routes)
        return random_route


