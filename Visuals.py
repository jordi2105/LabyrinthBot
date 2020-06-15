import pygame as p
from TileAction import TileAction
from MoveAction import MoveAction
from Players.Human import Human

from Button import Button

from Phase import Phase

from HelpFunctions import HelpFunctions



LEFT_MARGIN = 100
RIGHT_MARGIN = 200
TOP_MARGIN = 100
BOTTOM_MARGIN = 100

TILE_SIZE = 80

PAWN_RADIUS = int(TILE_SIZE/4)

BOARD_WIDTH = BOARD_HEIGHT = 7 * TILE_SIZE

CURRENT_TILE_CONTAINER_LEFT_MARGIN = 100
CURRENT_TILE_CONTAINER_WIDTH = 100
CURRENT_TILE_TEXT_BOTTOM_MARGIN = 10
CURRENT_TILE_CONTAINER_X = LEFT_MARGIN + BOARD_WIDTH + CURRENT_TILE_CONTAINER_LEFT_MARGIN

RIGHT_CONTAINER_MARGIN = CURRENT_TILE_CONTAINER_LEFT_MARGIN
RIGHT_CONTAINER_X = LEFT_MARGIN + BOARD_WIDTH + RIGHT_CONTAINER_MARGIN

PLACEHOLDERS_MARGIN = 10

MARGIN = 30

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
        self.draw_current_pawns(gamestate)
        self.draw_current_card(gamestate)
        self.draw_player_has_won(gamestate)

    def draw_player_has_won(self, gamestate):
        player = gamestate.player_won
        if player is not None:
            font = p.font.SysFont(None, 80)
            text = font.render(player.name + ' has won!', True, p.Color('red'))
            x = LEFT_MARGIN + 100
            y = TOP_MARGIN + 100
            self.screen.blit(text, (x, y))

    def draw_current_card(self, gamestate):
        player = gamestate.current_player
        y = TOP_MARGIN + 200
        font = p.font.SysFont(None, 30)
        self.text = font.render('Current card: ', True, p.Color('white'))
        self.screen.blit(self.text, (RIGHT_CONTAINER_X, y))

        if player.going_back_to_starting_point():
            text = font.render('Go back to your starting point!', True, p.Color('red'))
            x = RIGHT_CONTAINER_X
            y = y + MARGIN
            self.screen.blit(text, (x, y))

        elif isinstance(player, Human):
            card = player.current_card
            x = RIGHT_CONTAINER_X
            y = y + MARGIN

            self.screen.blit(card.image, (x, y))

    def draw_current_pawns(self, gamestate):
        for player in gamestate.players:
            tile = player.current_location
            self.draw_pawn(tile, player, gamestate)

    def draw_pawn(self, tile, player, gamestate):
        r = tile.row
        c = tile.column

        x = LEFT_MARGIN + int((c + 0.5) * TILE_SIZE) - int(PAWN_RADIUS)
        y = TOP_MARGIN + int((r + 0.5) * TILE_SIZE) - int(PAWN_RADIUS)

        x, y = self.get_new_position_by_tile_action(gamestate.current_tile_action, x, y, r, c)

        circle = p.Surface((PAWN_RADIUS * 2, PAWN_RADIUS * 2), p.SRCALPHA)
        p.draw.circle(circle, player.color, (PAWN_RADIUS, PAWN_RADIUS), PAWN_RADIUS)
        self.screen.blit(circle, (x, y))



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
            gamestate.current_tile.turn_clock_wise(1)
            gamestate.last_mouse_click_location = None

    def draw_board(self, gamestate):
        action = gamestate.current_tile_action
        board = gamestate.board

        for r in range(7):
            for c in range(7):
                tile = board[r][c]
                x = LEFT_MARGIN + c * TILE_SIZE
                y = TOP_MARGIN + r * TILE_SIZE

                x, y = self.get_new_position_by_tile_action(action, x, y, r ,c)

                self.draw_tile(gamestate, tile, (x, y))

    @staticmethod
    def get_new_position_by_tile_action(action, x, y, r, c) -> (int, int):
        if action is not None:
            if action.selected_index == r:
                if action.selected_side == 'left':
                    x += action.distance_moved
                elif action.selected_side == 'right':
                    x -= action.distance_moved
            if action.selected_index == c:
                if action.selected_side == 'top':
                    y += action.distance_moved
                elif action.selected_side == 'bottom':
                    y -= action.distance_moved
        return x, y

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

        self.draw_tile(gamestate, current_tile, (x, y), 255)



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
            phase = gamestate.current_phase
            if phase == Phase.CHOOSING_TILE and self.is_in_rect(p.mouse.get_pos(), rect):
                cur_tile = gamestate.current_tile
                self.draw_tile(gamestate, cur_tile, (rect[0], rect[1]), 200)
            if phase == Phase.CHOOSING_TILE and gamestate.last_mouse_click_location is not None and self.is_in_rect(gamestate.last_mouse_click_location,
                                                                                   rect):
                action = TileAction(selected_side=side, selected_index=index,
                                    player=gamestate.current_player)
                gamestate.current_tile_action = action
                gamestate.last_mouse_click_location = None

    def draw_tile(self, gamestate, tile, location, alpha=255):
        rect = self.screen.blit(tile.image, location)

        # Marks a tile with the color of the player if it is reachable
        if tile.reachability_mark:
            p.draw.rect(self.screen, gamestate.previous_player().color, (location[0], location[1], TILE_SIZE, TILE_SIZE), 4)

        # Makes it possible to hover over the tile and click on it)
        player = gamestate.current_player
        reachable_tiles = player.reachable_tiles
        phase = gamestate.current_phase
        if phase == Phase.CHOOSING_PAWN and tile in reachable_tiles and self.is_in_rect(p.mouse.get_pos(), rect):
            self.draw_pawn(tile, player, gamestate)
        if phase == Phase.CHOOSING_PAWN and tile in reachable_tiles and gamestate.last_mouse_click_location is not None and self.is_in_rect(gamestate.last_mouse_click_location, rect):
            route = player.route_to_tile(tile, gamestate)
            move_action = MoveAction(player, route)
            gamestate.current_move_action = move_action



    def get_tile_size(self):
        return TILE_SIZE

    @staticmethod
    def is_in_rect(pos, rect):
        return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]

