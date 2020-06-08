from Player import Player
from TileAction import TileAction
from MoveAction import MoveAction
from Phase import Phase

import random


class Bot(Player):
    def do_turn(self, gamestate):
        self.place_tile(gamestate)
        self.move_pawn(gamestate)

    def place_tile(self, gamestate):
        action = TileAction(selected_side='top', selected_index=1, player=gamestate.current_player)
        gamestate.current_tile_action = action

    def move_pawn(self, gamestate):
        routes = self.possible_routes(gamestate, [[self.current_location]])
        for r in routes:
            r[-1].reachability_mark = True
        random_route = random.choice(routes)
        move_action = MoveAction(self, random_route)
        gamestate.current_move_action = move_action
