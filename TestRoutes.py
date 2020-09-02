import unittest
from Generator import Generator
import Visuals
from GameState import GameState
from Visuals import Visuals
from Players.RandomBot import RandomBot
from Players.Bot import Bot
from Players.FirstBot import FirstBot
from Players.Human import Human
from Players.MinimaxBot import MinimaxBot
from TileType import TileType
from Phase import Phase
from Card import Card
from Objective import Objective
from Game import Game
from MoveAction import MoveAction
from TileAction import TileAction
from HelpFunctions import HelpFunctions

import collections

import pygame as p


class TestRoutes(unittest.TestCase):

    def test_possible_routes(self):
        for i in range(0, 100):
            players_ = {'random1': 'RandomBot', 'minimax': 'MinimaxBot'}
            nr_of_runs = 100
            logging_on = True
            visuals_on = True
            tile_speed = 10
            move_speed = 1
            seed = 6989004  # random.randint(0, 10000000)
            print('seed: ' + str(seed))
            board, tile_left = Generator.generate_random_full_board(seed)
            all_tiles = [item for sublist in board for item in sublist]
            red_tile = next((t for t in all_tiles if t.starting_point_color == 'RED'), None)
            blue_tile = next((t for t in all_tiles if t.starting_point_color == 'BLUE'), None)
            green_tile = next((t for t in all_tiles if t.starting_point_color == 'GREEN'), None)
            players = []
            for name in players_:
                if players_[name] == 'FirstBot':
                    first_bot = FirstBot(name=name, current_location=red_tile, color=p.Color(255, 0, 0, 150),
                                         seed=seed)
                    players.append(first_bot)
                elif players_[name] == 'RandomBot':
                    random_bot = RandomBot(name=name, current_location=blue_tile, color=p.Color(0, 0, 255, 150),
                                           seed=seed)
                    players.append(random_bot)
                elif players_[name] == 'Human':
                    human = Human(name=name, current_location=green_tile, color=p.Color(0, 255, 0, 150),
                                  seed=seed)
                    players.append(human)
                elif players_[name] == 'MinimaxBot':
                    minimaxBot = MinimaxBot(name=name, current_location=green_tile, color=p.Color(0, 255, 0, 150),
                                            seed=seed)
                    players.append(minimaxBot)
                else:
                    raise ValueError('Player has no valid type')
            Generator.deal_cards(players=players, nr_of_cards_pp=1)
            # for pl in players:
            #     print(pl.name + ' has cards: ')
            #     print([c.objective for c in pl.cards])
            gs = GameState(players=players, board=board, current_tile=tile_left, current_player=players[1])
            gs.recalculate_state_variables()
            tile_action = TileAction('top', 1, players[1])
            gs.current_tile_action = tile_action
            HelpFunctions.apply_tile_action(gs)

            #game = Game(gs, tile_speed=self.tile_speed, move_speed=self.move_speed, visuals_on=self.visuals_on)

            for pl in players:
                pl.update_properties(gs)

            for pl in players:
                routes = pl.possible_routes(gamestate=gs, tile=pl.current_location, routes=[[pl.current_location]])
                last_tiles = [item[-1] for item in routes]






