import pygame as p

from Generator import Generator
import Visuals
from GameState import GameState
from Visuals import Visuals
from Bot import Bot
from Action import Action
from Player import Player
import math

FPS = 120


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

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                if e.type == p.MOUSEBUTTONDOWN:
                    self.gamestate.last_mouse_click_location = p.mouse.get_pos()



            if self.visuals_on:
                self.visuals.draw_screen(self.gamestate)
                p.display.flip()
                dt = self.clock.tick(FPS)
                self.update_current_action()



            # if isinstance(self.gamestate.player_in_turn, Bot):
            #     self.gamestate.player_in_turn.do_turn()

            #self.gamestate.current_action.distance_moved += dt / 40

    def update_current_action(self):
        action = self.gamestate.current_action
        if action is not None:
            action.distance_moved += 4
            if action.distance_moved > self.visuals.get_tile_size():
                self.update_board()
                self.gamestate.current_action = None

    def update_board(self):
        action = self.gamestate.current_action
        side = action.selected_side
        index = action.selected_index

        if side == 'left':
            new_tiles, new_current_tile = self.shift_tiles(self.gamestate.board[index], 1)
            self.gamestate.board[index] = new_tiles
        elif side == 'right':
            new_tiles, new_current_tile = self.shift_tiles(self.gamestate.board[index], -1)
            self.gamestate.board[index] = new_tiles
        elif side in ['top', 'bottom']:
            if side == 'top':
                n = 1
            elif side == 'bottom':
                n = -1
            new_tiles, new_current_tile = self.shift_tiles([r[index] for r in self.gamestate.board], n)
            for i, row in enumerate(self.gamestate.board):
                self.gamestate.board[i][index] = new_tiles[i]

        self.gamestate.current_tile = new_current_tile




    def shift_tiles(self, tiles, n):
        new_tile = self.gamestate.current_tile
        if n > 0:
            new_current_tile = tiles[-1]
            tiles = [new_tile] + tiles[:-n]
        elif n < 0:
            new_current_tile = tiles[0]
            tiles = tiles[-n:] + [new_tile]
        return tiles, new_current_tile

if __name__ == '__main__':
    board, tile_left = Generator.generate_random_full_board()
    p1 = Bot()
    #action = Action('top', 2, 0, p1)
    gs = GameState(players=[p1], board=board, current_tile=tile_left, current_action=None)
    game = Game(gs)
    game.run()

# def initialize_board():
