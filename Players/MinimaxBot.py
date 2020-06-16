from Players.Player import Player
from Players.Bot import Bot
from TileAction import TileAction
from MoveAction import MoveAction
from GameState import GameState

import random
import sys


# This bot only works with two players
class MinimaxBot(Bot):

    def do_turn(self, gamestate, seed):
        self.place_tile(gamestate)
        self.move_pawn(gamestate)

    def determine_side_and_index(self, gamestate) -> (str, int):
        index = random.choice([1, 3, 5])
        side = random.choice(['top', 'bottom', 'left', 'right'])
        return side, index

    def determine_route(self, gamestate):
        routes = self.possible_routes(gamestate, [[self.current_location]])
        random_route = random.choice(routes)
        return random_route

    def minimax(self, state, depth, maximizingPlayer):
        if depth == 0:
            return self.fitness(state)

        if maximizingPlayer:
            max_eval = -sys.maxsize
            for child in self.get_children_of_state(state):
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = sys.maxsize
            for child in self.get_children_of_state(state):
                eval = self.minimax(child, depth - 1, True)
                min_eval = max(min_eval, eval)
            return min_eval

    def fitness(self, state: GameState):
        # Here I must give a fitness value to a state

        player = next(p for p in state.players if p.name == self.name)
        pass

    def get_children_of_state(self, state):
        pass
