from Board import Board
import os
from PIL import Image, ImageTk
import pygame as p
import GameState
from TileType import TileType
from TileAction import TileAction

from Button import Button

from HelpFunctions import HelpFunctions



LEFT_MARGIN = 100
RIGHT_MARGIN = 200
TOP_MARGIN = 100
BOTTOM_MARGIN = 100

TILE_SIZE = 80

PAWN_RADIUS = TILE_SIZE/4

BOARD_WIDTH = BOARD_HEIGHT = 7 * TILE_SIZE

CURRENT_TILE_CONTAINER_LEFT_MARGIN = 100
CURRENT_TILE_CONTAINER_WIDTH = 100
CURRENT_TILE_TEXT_BOTTOM_MARGIN = 10
CURRENT_TILE_CONTAINER_X = LEFT_MARGIN + BOARD_WIDTH + CURRENT_TILE_CONTAINER_LEFT_MARGIN

PLACEHOLDERS_MARGIN = 10

WIDTH = LEFT_MARGIN + 7 * TILE_SIZE + RIGHT_MARGIN + CURRENT_TILE_CONTAINER_LEFT_MARGIN + CURRENT_TILE_CONTAINER_WIDTH
HEIGHT = TOP_MARGIN + 7 * TILE_SIZE + BOTTOM_MARGIN

CURRENT_TILE_TEXT_HEIGHT = None


class Visuals:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((0, 0, 0))



    def draw_screen(self, gamestate):
        self.screen.fill((0, 0, 0))
        self.draw_board(gamestate)
        self.draw_current_tile_text()
        self.draw_current_tile(gamestate)
        self.draw_tile_placeholders(gamestate)
        self.draw_turn_button(gamestate)
        self.draw_current_player(gamestate)
        self.draw_pawns(gamestate)

    def draw_pawns(self, gamestate):
        for player in gamestate.players:
            tile = player.current_location
            r, c = HelpFunctions.get_location_of_tile(gamestate.board, tile)
            p.draw.circle(self.screen,
                          player.color,
                          (int((c + 0.5)*TILE_SIZE), int((r + 0.5)*TILE_SIZE)),
                          PAWN_RADIUS)


    def draw_current_player(self, gamestate):
        name = gamestate.current_player.name
        font = p.font.SysFont(None, 30)
        self.text = font.render('Current player: ' + name, True, p.Color('white'))
        self.screen.blit(self.text, (LEFT_MARGIN + 7 * TILE_SIZE + CURRENT_TILE_CONTAINER_LEFT_MARGIN,
                                     TOP_MARGIN + self.text.get_height() + TILE_SIZE + 2 * CURRENT_TILE_TEXT_BOTTOM_MARGIN + 40 + CURRENT_TILE_TEXT_BOTTOM_MARGIN))

    def draw_current_tile_text(self):
        font = p.font.SysFont(None, 30)
        self.text = font.render('Current tile', True, p.Color('white'))
        self.screen.blit(self.text, (LEFT_MARGIN + 7 * TILE_SIZE + CURRENT_TILE_CONTAINER_LEFT_MARGIN, TOP_MARGIN))

    def draw_turn_button(self, gamestate):

        button = Button(p.Color('grey'), CURRENT_TILE_CONTAINER_X,
                        TOP_MARGIN + self.text.get_height() + TILE_SIZE + 2 * CURRENT_TILE_TEXT_BOTTOM_MARGIN,
                        40, 20, 20, 'Turn')
        rect = button.draw(self.screen)
        if gamestate.last_mouse_click_location is not None and self.is_in_rect(gamestate.last_mouse_click_location,
                                                                               rect):
            gamestate.current_tile.turn_clock_wise()
            gamestate.last_mouse_click_location = None

    def draw_board(self, gamestate):
        action = gamestate.current_tile_action
        board = gamestate.board

        for r in range(7):
            for c in range(7):
                tile = board[r][c]
                img = p.image.load(tile.image_file_url)
                img = self.rotate_image(img, tile.type, tile.open_sides)
                img = p.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                x_location = LEFT_MARGIN + c * TILE_SIZE
                y_location = TOP_MARGIN + r * TILE_SIZE

                if action is not None:
                    x_location_current_tile = 0
                    y_location_current_tile = 0
                    if action.selected_index == r:
                        if action.selected_side == 'left':
                            x_location += action.distance_moved
                            x_location_current_tile += action.distance_moved
                        elif action.selected_side == 'right':
                            x_location -= action.distance_moved
                            x_location_current_tile -= action.distance_moved
                    if action.selected_index == c:
                        if action.selected_side == 'top':
                            y_location += action.distance_moved
                            y_location_current_tile += action.distance_moved
                        elif action.selected_side == 'bottom':
                            y_location -= action.distance_moved
                            y_location_current_tile -= action.distance_moved

                self.screen.blit(img, (x_location, y_location))

    def draw_current_tile(self, gamestate):
        current_tile = gamestate.current_tile
        img = p.image.load(current_tile.image_file_url)
        img = p.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        action = gamestate.current_tile_action
        x = LEFT_MARGIN + 7 * TILE_SIZE + CURRENT_TILE_CONTAINER_LEFT_MARGIN
        y = TOP_MARGIN + self.text.get_height() + CURRENT_TILE_TEXT_BOTTOM_MARGIN
        if action is not None:
            if action.selected_side == 'top':
                x = LEFT_MARGIN + action.selected_index * TILE_SIZE
                y = TOP_MARGIN - TILE_SIZE + action.distance_moved
            elif action.selected_side == 'bottom':
                x = LEFT_MARGIN + action.selected_index * TILE_SIZE
                y = TOP_MARGIN + BOARD_HEIGHT - action.distance_moved
            elif action.selected_side == 'left':
                x = LEFT_MARGIN - TILE_SIZE + action.distance_moved
                y = TOP_MARGIN + action.selected_index * TILE_SIZE
            elif action.selected_side == 'right':
                x = LEFT_MARGIN + BOARD_WIDTH - action.distance_moved
                y = TOP_MARGIN + action.selected_index * TILE_SIZE

        self.draw_tile(current_tile, (x, y), 255)

    def draw_tile_placeholders(self, gamestate):
        rects = []
        for r in [1, 3, 5]:
            rect_left = p.Rect(LEFT_MARGIN - TILE_SIZE - PLACEHOLDERS_MARGIN, TOP_MARGIN + r * TILE_SIZE, TILE_SIZE,
                               TILE_SIZE)
            rect_right = p.Rect(LEFT_MARGIN + BOARD_WIDTH + PLACEHOLDERS_MARGIN, TOP_MARGIN + r * TILE_SIZE, TILE_SIZE,
                                TILE_SIZE)
            rects.extend([(rect_left, r, 'left'), (rect_right, r, 'right')])

        for c in [1, 3, 5]:
            rect_top = p.Rect(LEFT_MARGIN + c * TILE_SIZE, TOP_MARGIN - TILE_SIZE - PLACEHOLDERS_MARGIN, TILE_SIZE,
                              TILE_SIZE)
            rect_bottom = p.Rect(LEFT_MARGIN + c * TILE_SIZE, TOP_MARGIN + BOARD_HEIGHT + PLACEHOLDERS_MARGIN,
                                 TILE_SIZE, TILE_SIZE)
            rects.extend([(rect_top, c, 'top'), (rect_bottom, c, 'bottom')])

        for (rect, index, side) in rects:
            rounded_rect = HelpFunctions.make_rounded_rect(self.screen, rect, p.Color('grey'), radius=0.4)
            if self.is_in_rect(p.mouse.get_pos(), rect):
                cur_tile = gamestate.current_tile
                self.draw_tile(cur_tile, (rect[0], rect[1]), 200)
            if gamestate.last_mouse_click_location is not None and self.is_in_rect(gamestate.last_mouse_click_location,
                                                                                   rect):
                action = TileAction(selected_side=side, selected_index=index,
                                    player=gamestate.current_player)
                gamestate.current_tile_action = action
                gamestate.last_mouse_click_location = None

    def draw_tile(self, tile, location, alpha=255):
        img = p.image.load(tile.image_file_url)
        img = self.rotate_image(img, tile.type, tile.open_sides)
        img = p.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img.set_alpha(alpha)
        self.screen.blit(img, location)

    def get_tile_size(self):
        return TILE_SIZE

    @staticmethod
    def is_in_rect(pos, rect):
        return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]

    @staticmethod
    def rotate_image(image, type, open_sides):
        if type == TileType.STRAIGHT:
            if not open_sides[0]:
                image = p.transform.rotate(image, 90)
        elif type == TileType.CURVED:
            if open_sides == [True, True, False, False]:
                image = p.transform.rotate(image, 270)
            elif open_sides == [False, True, True, False]:
                image = p.transform.rotate(image, 180)
            elif open_sides == [False, False, True, True]:
                image = p.transform.rotate(image, 90)
        elif type == TileType.THREE_WAY:
            if not open_sides[3]:
                image = p.transform.rotate(image, 270)
            elif not open_sides[0]:
                image = p.transform.rotate(image, 180)
            elif not open_sides[1]:
                image = p.transform.rotate(image, 90)
        return image
