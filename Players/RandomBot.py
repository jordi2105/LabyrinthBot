from Players.Player import Player
from Players.Bot import Bot
from TileAction import TileAction
from MoveAction import MoveAction

import random


class RandomBot(Bot):

    def determine_side_and_index_and_rotation(self, gamestate) -> (str, int, int):
        rotation_n = random.randint(0, 3)
        index = random.choice([1, 3, 5])
        side = random.choice(['top', 'bottom', 'left', 'right'])
        return side, index, rotation_n

    def determine_route(self, gamestate):
        routes = self.possible_routes(gamestate=gamestate,
                                      tile=self.current_location,
                                      routes=[[self.current_location]])
        random_route = random.choice(routes)
        return random_route


