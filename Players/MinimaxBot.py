from Players.Player import Player
from Players.Bot import Bot
from TileAction import TileAction
from MoveAction import MoveAction
from GameState import GameState
from HelpFunctions import HelpFunctions

import random
import sys
#import copy
from copy import copy


# This bot only works with two players
class MinimaxBot(Bot):

    def determine_side_and_index_and_rotation(self, gamestate) -> (str, int, int):
        a = self.minimax(state=gamestate, depth=1, maximizingPlayer=True)
        print(a)
        index = random.choice([1, 3, 5])
        side = random.choice(['top', 'bottom', 'left', 'right'])
        rotation_n = random.randint(0, 3)
        return side, index, rotation_n

    def determine_route(self, gamestate):
        # routes = self.possible_routes(gamestate, [[self.current_location]])
        # random_route = random.choice(routes)
        return random_route

    def minimax(self, state, depth, maximizingPlayer):
        if depth == 0:
            return self.fitness(state)

        if maximizingPlayer:
            max_eval = -sys.maxsize - 1
            children = self.get_children_of_state(state)
            for child in children:
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = sys.maxsize
            children = self.get_children_of_state(state)
            for child in children:
                eval = self.minimax(child, depth - 1, True)
                min_eval = max(min_eval, eval)
            return min_eval

    def fitness(self, state: GameState):
        # Here I must give a fitness value to a state

        fitness = 0

        player = next(p for p in state.players if p.name == self.name)
        other_player = next(p for p in state.players if p.name != self.name)
        fitness -= len(player.cards)
        #fitness += len(other_player.cards)
        if len(player.cards) == 0:
            a = 1
        if state.player_won == player:
            fitness = sys.maxsize
        return fitness

    def get_children_of_state(self, state):
        children = []
        for side in ['top', 'bottom', 'left', 'right']:
            for index in [1, 3, 5]:
                for rotate_n in range(4):
                    child_state_for_tile_action = HelpFunctions.copy_gamestate(state)
                    child_state_for_tile_action.current_tile.turn_clock_wise(rotate_n)

                    # Create a TileAction
                    tile_action = TileAction(selected_side=side, selected_index=index, player=child_state_for_tile_action.current_player)
                    child_state_for_tile_action.current_tile_action = tile_action
                    HelpFunctions.apply_tile_action(gamestate=child_state_for_tile_action)
                    child_state_for_tile_action.recalculate_state_variables()

                    routes = child_state_for_tile_action.current_player.possible_routes(
                        gamestate=child_state_for_tile_action,
                        tile=child_state_for_tile_action.current_player.current_location,
                        routes=[[child_state_for_tile_action.current_player.current_location]])

                    for route in routes:
                        # Create a MoveAction
                        child_state = HelpFunctions.copy_gamestate(child_state_for_tile_action)
                        move_action = MoveAction(player=child_state.current_player, route=route, current_tile=child_state.current_player.current_location)
                        child_state.current_move_action = move_action
                        HelpFunctions.apply_full_move_action(gamestate=child_state, player=child_state.current_player)
                        child_state.recalculate_state_variables
                        children.append(child_state)

        return children
