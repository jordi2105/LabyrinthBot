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
from TileType import TileType
from Phase import Phase
from Card import Card
from Objective import Objective
from Game import Game
import random


class Tournament:

    def __init__(self, nr_of_runs, logging_on, visuals_on):
        self.nr_of_runs = nr_of_runs
        self.logging_on = logging_on
        self.visuals_on = visuals_on

    def run(self):
        winners = []
        for r in range(self.nr_of_runs):
            seed = random.random()
            board, tile_left = Generator.generate_random_full_board(seed)
            all_tiles = [item for sublist in board for item in sublist]
            red_tile = next((t for t in all_tiles if t.starting_point_color == 'RED'), None)
            blue_tile = next((t for t in all_tiles if t.starting_point_color == 'BLUE'), None)
            first_bot = FirstBot(name='FirstBot', current_location=red_tile, color=p.Color(255, 0, 0, 150), seed=seed)
            random_bot = RandomBot(name='RandomBot', current_location=blue_tile, color=p.Color(255, 0, 0, 150), seed=seed)
            players = [random_bot, first_bot]
            Generator.deal_cards(players=players, nr_of_cards_pp=4)
            gs = GameState(players=players, board=board, current_tile=tile_left, current_player=players[0])

            game = Game(gs, visuals_on=self.visuals_on)
            game.run()
            winner = game.gamestate.player_won
            winners.append(winner)


if __name__ == '__main__':
    tournament = Tournament(30, logging_on=True, visuals_on=False)
    tournament.run()
