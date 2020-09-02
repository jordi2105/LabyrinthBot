from abc import ABC, abstractmethod
from Players.Player import Player
from TileAction import TileAction
from MoveAction import MoveAction
from HelpFunctions import HelpFunctions
import random


class Bot(Player):

    def place_tile(self, gamestate):
        side, index, rotation_n = self.determine_side_and_index_and_rotation(gamestate)
        gamestate.current_tile.turn_clock_wise(rotation_n)
        action = TileAction(selected_side=side, selected_index=index, player=gamestate.current_player)
        gamestate.current_tile_action = action

    @abstractmethod
    def determine_side_and_index_and_rotation(self, gamestate) -> (str, int, int):
        pass

    def move_pawn(self, gamestate):
        route = self.determine_route(gamestate)
        move_action = MoveAction(self, route)
        gamestate.current_move_action = move_action

    @abstractmethod
    def determine_route(self, gamestate):
        pass

    # def choose_random_route(self, gamestate, routes):
    #     random_route = random.choice(routes)
    #     return random_route
