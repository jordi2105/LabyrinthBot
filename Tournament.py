import copy

import pygame as p

from Generator import Generator
import Visuals
from GameState import GameState
from Visuals import Visuals
from Players.RandomBot import RandomBot
from Players.Bot import Bot
from Players.FirstBot import FirstBot
from Players.Human import Human
from Players.MinimaxBot import MinimaxBot
from Players.FitnessBasedBot import FitnessBasedBot
from TileType import TileType
from Phase import Phase
from Card import Card
from Objective import Objective
from Game import Game
from HelpFunctions import HelpFunctions
import random


class Tournament:

    def __init__(self, nr_of_runs, logging_on, visuals_on, players, nr_of_cards_pp, tile_speed=4, move_speed=4, board_adjustments=[]):
        self.nr_of_runs = nr_of_runs
        self.logging_on = logging_on
        self.visuals_on = visuals_on
        self.tile_speed = tile_speed
        self.move_speed = move_speed
        self.players = players
        self.winners = []
        self.board_adjustments = board_adjustments
        self.nr_of_cards_pp = nr_of_cards_pp

    def run(self):
        for r in range(self.nr_of_runs):
            seed = random.randint(0, 10000000)
            print('seed: ' + str(seed))
            board, tile_left = Generator.generate_random_full_board(seed)
            all_tiles = [item for sublist in board for item in sublist]
            red_tile = next((t for t in all_tiles if t.starting_point_color == 'RED'), None)
            blue_tile = next((t for t in all_tiles if t.starting_point_color == 'BLUE'), None)
            green_tile = next((t for t in all_tiles if t.starting_point_color == 'GREEN'), None)
            players = []
            for name in self.players:
                if self.players[name] == 'FirstBot':
                    first_bot = FirstBot(name=name, current_location=red_tile, color=p.Color(255, 0, 0, 150),
                                         seed=seed)
                    players.append(first_bot)
                elif self.players[name] == 'RandomBot':
                    random_bot = RandomBot(name=name, current_location=blue_tile, color=p.Color(0, 0, 255, 150),
                                           seed=seed)
                    players.append(random_bot)
                elif self.players[name] == 'Human':
                    human = Human(name=name, current_location=green_tile, color=p.Color(0, 255, 0, 150),
                                  seed=seed)
                    players.append(human)
                elif self.players[name] == 'MinimaxBot':
                    minimaxBot = MinimaxBot(name=name, current_location=green_tile, color=p.Color(0, 255, 0, 150),
                                            seed=seed)
                    players.append(minimaxBot)
                elif self.players[name] == 'FitnessBasedBot':
                    fitness_based_bot = FitnessBasedBot(name=name, current_location=green_tile,
                                                        color=p.Color(0, 255, 0, 150),
                                                        seed=seed)
                    players.append(fitness_based_bot)
                else:
                    raise ValueError('Player has no valid type')
            Generator.deal_cards(players=players, nr_of_cards_pp=self.nr_of_cards_pp)
                                 #predefined_objectives=[[Objective.BAT], [Objective.JEWEL]])
            # for pl in players:
            #     print(pl.name + ' has cards: ')
            #     print([c.objective for c in pl.cards])
            gs = GameState(players=players, board=board, current_tile=tile_left, current_player=players[0])

            Generator.adjust_board(gs, self.board_adjustments)

            game = Game(gs, tile_speed=self.tile_speed, move_speed=self.move_speed, visuals_on=self.visuals_on)
            game.run()
            winner = game.gamestate.player_won
            print('The winner of game ' + str(r) + ': ' + winner.name)
            self.winners.append(winner)


if __name__ == '__main__':
    # players = {'random1': 'RandomBot', 'minimax': 'MinimaxBot'}
   # players = {'random': 'RandomBot', 'firstbot': 'FirstBot'}
    players = {'human': 'Human', 'fitness-based': 'FitnessBasedBot'}
    #players = {'fitness-based': 'FitnessBasedBot', 'random': 'RandomBot'}
    #players = {'FirstBot': FirstBot, 'fitness-based': FitnessBasedBot}

    board_adjustments = []#[(3, 0, 'tile_images/BAT.jpg', 1)]

    tournament = Tournament(nr_of_runs=100, logging_on=True, visuals_on=True, players=players, nr_of_cards_pp=1, tile_speed=1,
                            move_speed=1)
    tournament.run()
    winners = tournament.winners
    for name in players:
        c = sum(map(lambda x: x.name == name, winners))
        print('Wins ' + name + ': ' + str(c) + '/' + str(len(winners)))
