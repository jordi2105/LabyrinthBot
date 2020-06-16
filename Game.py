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
import random

FPS = 120

TILE_SIZE = 80


class Game:
    def __init__(self, gamestate: GameState, tile_speed, move_speed, visuals_on=True):
        self.gamestate = gamestate
        self.visuals_on = visuals_on
        self.tile_speed = tile_speed
        self.move_speed = move_speed
        if visuals_on:
            self.visuals = Visuals()
        self.clock = p.time.Clock()

    def initialize(self):
        pass

    def run(self):
        running = True
        while not self.gamestate.player_won and running:

            if self.visuals_on:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    if isinstance(self.gamestate.current_player, Human):
                        if e.type == p.MOUSEBUTTONDOWN:
                            self.gamestate.last_mouse_click_location = p.mouse.get_pos()

            if isinstance(self.gamestate.current_player, Bot):
                if self.gamestate.current_phase == Phase.CHOOSING_PAWN:
                    self.gamestate.current_player.move_pawn(self.gamestate)
                elif self.gamestate.current_phase == Phase.CHOOSING_TILE:
                    self.gamestate.current_player.place_tile(self.gamestate)

            if self.gamestate.current_phase == Phase.TILE_MOVING:
                self.update_current_tile_action()
            elif self.gamestate.current_phase == Phase.PAWN_MOVING:
                self.update_current_move_action()

            if self.visuals_on:
                self.visuals.draw_screen(self.gamestate)
                p.display.flip()


    def next_player(self):
        index = self.gamestate.players.index(self.gamestate.current_player)
        self.gamestate.current_player = self.gamestate.players[(index + 1) % len(self.gamestate.players)]

    def update_current_move_action(self):
        action = self.gamestate.current_move_action
        player = self.gamestate.current_player
        dt = int(self.clock.tick(FPS))
        print(dt)
        if action.on_last_tile():
            self.next_phase()
            if player.is_located_at_current_objective():
                player.next_card()
            elif player.going_back_to_starting_point() and player.is_on_starting_point():
                self.gamestate.player_won = player
        else:
            action.next_tile(self.gamestate)

    def update_current_tile_action(self):
        action = self.gamestate.current_tile_action

        action.distance_moved += self.tile_speed
        if action.distance_moved > TILE_SIZE:
            action.distance_moved = TILE_SIZE
            self.update_board()
            self.next_phase()

    def next_phase(self):
        self.gamestate.re_calculate_state_variables()
        if self.gamestate.current_phase == Phase.CHOOSING_TILE:
            self.gamestate.current_phase = Phase.TILE_MOVING
        elif self.gamestate.current_phase == Phase.TILE_MOVING:
            self.gamestate.current_tile_action = None
            self.gamestate.current_phase = Phase.CHOOSING_PAWN
        elif self.gamestate.current_phase == Phase.CHOOSING_PAWN:
            self.gamestate.current_phase = Phase.PAWN_MOVING
        elif self.gamestate.current_phase == Phase.PAWN_MOVING:
            self.gamestate.current_move_action = None
            self.gamestate.current_phase = Phase.CHOOSING_TILE
            self.next_player()

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

        # Check if a player is pushed off the board
        for player in self.gamestate.players:
            if player.current_location == self.gamestate.current_tile:
                if side in ['left', 'top']:
                    player.current_location = new_tiles[0]
                elif side in ['right', 'bottom']:
                    player.current_location = new_tiles[-1]

    def shift_tiles(self, tiles, n):
        new_tile = self.gamestate.current_tile
        if n > 0:
            new_current_tile = tiles[-1]
            tiles = [new_tile] + tiles[:-n]
        elif n < 0:
            new_current_tile = tiles[0]
            tiles = tiles[-n:] + [new_tile]
        return tiles, new_current_tile


def test_stuff(all_tiles, board):
    curved_tiles = [t for t in all_tiles if t.type == TileType.CURVED and t.starting_point_color is None]
    three_way_tiles = [t for t in all_tiles if t.type == TileType.THREE_WAY]
    straight_tiles = [t for t in all_tiles if t.type == TileType.STRAIGHT]
    tile1 = curved_tiles[0]
    tile2 = curved_tiles[1]
    tile3 = curved_tiles[2]
    tile4 = three_way_tiles[0]
    tile5 = straight_tiles[0]
    tile6 = curved_tiles[3]

    tile1.turn_clock_wise()
    tile1.turn_clock_wise()

    tile2.turn_clock_wise()
    tile2.turn_clock_wise()
    tile2.turn_clock_wise()

    tile3.turn_clock_wise()

    tile5.turn_clock_wise()

    Generator.place_tiles_on_board(board, [tile1, tile2, tile3, tile4, tile5, tile6],
                                   [(0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3)])
