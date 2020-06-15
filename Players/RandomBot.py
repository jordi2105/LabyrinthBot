from Players.Player import Player
from Players.Bot import Bot
from TileAction import TileAction
from MoveAction import MoveAction

import random


class RandomBot(Bot):

    def do_turn(self, gamestate, seed):
        self.place_tile(gamestate)
        self.move_pawn(gamestate)

    def place_tile(self, gamestate):
        index = random.choice([1, 3, 5])
        side = random.choice(['top', 'bottom', 'left', 'right'])
        action = TileAction(selected_side=side, selected_index=index, player=gamestate.current_player)
        gamestate.current_tile_action = action

    def move_pawn(self, gamestate):
        routes = self.possible_routes(gamestate, [[self.current_location]])
        urls = [r[-1].image_file_url for r in routes]
        print("Tiles Reachable for " + self.name + ": " + ", ".join(urls))
        random_route = random.choice(routes)
        print(str(routes.index(random_route)))
        move_action = MoveAction(self, random_route)
        print(move_action)
        gamestate.current_move_action = move_action
