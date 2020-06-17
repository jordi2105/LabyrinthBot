import pygame as p
import Tile
from Objective import Objective
from GameState import GameState

class HelpFunctions:

    @staticmethod
    def make_rounded_rect(surface, rect, color, radius=0.4):
        rect = p.Rect(rect)
        color = p.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = p.Surface(rect.size, p.SRCALPHA)

        circle = p.Surface([min(rect.size) * 3] * 2, p.SRCALPHA)
        p.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = p.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=p.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=p.BLEND_RGBA_MIN)

        return surface.blit(rectangle, pos)

    @staticmethod
    def color_to_str(color):
        if color.r == 255 and color.g == 255:
            return 'YELLOW'
        elif color.r == 255:
            return 'RED'
        elif color.g == 255:
            return 'GREEN'
        elif color.b == 255:
            return 'BLUE'

    # @staticmethod
    # def simulate_next_state(state: GameState, rotate_current_tile: int, side: str, index: int, ):



    @staticmethod
    def apply_tile_action(gamestate: GameState):
        action = gamestate.current_tile_action
        side = action.selected_side
        index = action.selected_index

        if side == 'left':
            new_tiles, new_current_tile = HelpFunctions.shift_tiles(gamestate, gamestate.board[index], 1)
            gamestate.board[index] = new_tiles
        elif side == 'right':
            new_tiles, new_current_tile = HelpFunctions.shift_tiles(gamestate, gamestate.board[index], -1)
            gamestate.board[index] = new_tiles
        elif side in ['top', 'bottom']:
            if side == 'top':
                n = 1
            elif side == 'bottom':
                n = -1
            new_tiles, new_current_tile = HelpFunctions.shift_tiles(gamestate, [r[index] for r in gamestate.board], n)
            for i, row in enumerate(gamestate.board):
                gamestate.board[i][index] = new_tiles[i]

        gamestate.current_tile = new_current_tile

        # Check if a player is pushed off the board
        for player in gamestate.players:
            if player.current_location == gamestate.current_tile:
                if side in ['left', 'top']:
                    player.current_location = new_tiles[0]
                elif side in ['right', 'bottom']:
                    player.current_location = new_tiles[-1]

    @staticmethod
    def shift_tiles(gamestate, tiles, n):
        new_tile = gamestate.current_tile
        if n > 0:
            new_current_tile = tiles[-1]
            tiles = [new_tile] + tiles[:-n]
        elif n < 0:
            new_current_tile = tiles[0]
            tiles = tiles[-n:] + [new_tile]
        return tiles, new_current_tile



