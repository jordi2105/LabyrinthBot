from Players.Player import Player
from Players.Bot import Bot
from Players.FirstBot import FirstBot
from TileAction import TileAction
from MoveAction import MoveAction
from GameState import GameState
from HelpFunctions import HelpFunctions
from Tile import Tile

import random
import sys
# import copy
from copy import copy


# This bot only looks one tile placement ahead by attaching a fitness to every option
class FitnessBasedBot(FirstBot):

    def determine_side_and_index_and_rotation(self, gamestate) -> (str, int, int):
        children_states = self.get_children_of_state(gamestate)
        max_fitness = -sys.maxsize - 1
        best = None
        for (side, index, rotation_n, child, route) in children_states:
            fitness = self.fitness(child)
            if fitness > max_fitness:
                max_fitness = fitness
                best = (side, index, rotation_n, child, route)

        #print('max: ' + str(max_fitness))
        return best[0], best[1], best[2]

    # def determine_route(self, gamestate):
    #     pass

    def fitness(self, state: GameState):
        fitness = 0
        player = next(p for p in state.players if p.name == self.name)
        # reachable_tiles = state.current_player.reachable_tiles
        fitness -= player.nr_of_cards_left()
        fitness += state.player_won == player
        #fitness -= distance_to_objective
        return fitness

    def get_children_of_state(self, state: GameState) -> [(str, int, int, GameState, [Tile])]:
        children = []
        for side in ['top', 'bottom', 'left', 'right']:
            for index in [1, 3, 5]:
                for rotate_n in range(4):
                    child_state_for_tile_action = state.copy()
                    HelpFunctions.check_gamestates_different(state, child_state_for_tile_action)
                    child_state_for_tile_action.current_tile.turn_clock_wise(rotate_n)

                    # Create a TileAction
                    tile_action = TileAction(selected_side=side, selected_index=index,
                                             player=child_state_for_tile_action.current_player)
                    child_state_for_tile_action.current_tile_action = tile_action
                    HelpFunctions.apply_tile_action(gamestate=child_state_for_tile_action)
                    child_state_for_tile_action.recalculate_state_variables()

                    routes = child_state_for_tile_action.current_player.possible_routes(
                        gamestate=child_state_for_tile_action,
                        tile=child_state_for_tile_action.current_player.current_location,
                        routes=[[child_state_for_tile_action.current_player.current_location]])

                    for route in routes:
                        # Create a MoveAction
                        child_state = child_state_for_tile_action.copy()
                        HelpFunctions.check_gamestates_different(child_state_for_tile_action, child_state)
                        move_action = MoveAction(player=child_state.current_player, route=route,
                                                 current_tile=child_state.current_player.current_location)
                        child_state.current_move_action = move_action
                        HelpFunctions.apply_full_move_action(gamestate=child_state, player=child_state.current_player)
                        child_state.recalculate_state_variables
                        children.append((side, index, rotate_n, child_state, route))

        return children
