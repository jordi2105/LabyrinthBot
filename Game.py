import pygame as p

from Generator import Generator
import Visuals
from GameState import GameState
from Visuals import Visuals
from Bot import Bot
from Action import Action
from Player import Player
import math

FPS = 60


class Game:
    def __init__(self, gamestate: GameState, visuals_on=True):
        self.gamestate = gamestate
        self.visuals_on = visuals_on
        self.visuals = Visuals()
        self.clock = p.time.Clock()

    def initialize(self):
        pass

    def run(self):
        running = True
        while running:

            #print(dt)

            # for i in range(1000000):
            #             #     a = math.sqrt(52352)
            #             #     b = a*a

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

            #if self.visuals_on:
            self.visuals.draw_board(self.gamestate)
            p.display.flip()
            dt = self.clock.tick(FPS)

            # if isinstance(self.gamestate.player_in_turn, Bot):
            #     self.gamestate.player_in_turn.do_turn()

            self.gamestate.current_action.distance_moved += 2


if __name__ == '__main__':
    board, tile_left = Generator.generate_random_full_board()
    p1 = Bot()
    action = Action('left', 4, 15, p1)
    gs = GameState(players=[p1], board=board, current_tile=tile_left, current_action=action)
    game = Game(gs)
    game.run()

# def initialize_board():