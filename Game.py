import pygame as p

from Generator import Generator
import Visuals
from GameState import GameState
from Visuals import Visuals
from Bot import Bot
from Human import Human
from TileAction import TileAction
from Player import Player
import math

FPS = 120
TILE_SPEED = 8


class Game:
    def __init__(self, gamestate: GameState, visuals_on=True):
        self.gamestate = gamestate
        self.end_of_turn = False
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
                if isinstance(self.gamestate.current_player, Human):
                    if e.type == p.MOUSEBUTTONDOWN:
                        self.gamestate.last_mouse_click_location = p.mouse.get_pos()

            if isinstance(self.gamestate.current_player, Bot) and self.gamestate.current_tile_action is None:
                self.gamestate.current_player.do_turn(self.gamestate)

            self.update_current_tile_action()

            if self.visuals_on:
                self.visuals.draw_screen(self.gamestate)
                p.display.flip()

    def set_next_player(self):
        index = self.gamestate.players.index(self.gamestate.current_player)
        self.gamestate.current_player = players[(index + 1) % len(players)]

    def perform_end_of_turn(self):
        self.gamestate.current_tile_action = None
        self.set_next_player()

    def update_current_tile_action(self):
        action = self.gamestate.current_tile_action
        if action is not None:
            action.distance_moved += TILE_SPEED
            if action.distance_moved > self.visuals.get_tile_size():
                self.update_board()
                self.perform_end_of_turn()

    def update_board(self):
        action = self.gamestate.current_tile_action
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
    all_tiles = [item for sublist in board for item in sublist]
    red_tile = next((t for t in all_tiles if t.starting_point_color == 'RED'), None)
    blue_tile = next((t for t in all_tiles if t.starting_point_color == 'BLUE'), None)
    bot = Bot(name='Bot', current_location=red_tile, color='RED')
    human = Human(name='Human', current_location=blue_tile, color='BLUE')
    players = [human, bot]
    gs = GameState(players=players, board=board, current_tile=tile_left, current_player=players[0])
    game = Game(gs)
    game.run()

# def initialize_board():
