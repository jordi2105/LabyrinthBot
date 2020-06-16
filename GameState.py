from TileAction import TileAction
from Phase import Phase


class GameState:
    def __init__(self, players, board=None, current_tile=None, current_player=None, current_tile_action=None,
                 last_mouse_click_location=None, current_move_action=None, current_phase=Phase.CHOOSING_TILE):
        self.board = board  # 2d array of Tiles [rows][columns]
        self.current_tile = current_tile
        self.players = players
        self.current_player = current_player
        self._current_tile_action = current_tile_action
        self.last_mouse_click_location = last_mouse_click_location
        self._current_move_action = current_move_action
        self._current_phase = current_phase
        self.player_won = None

        self.re_calculate_state_variables()

    def re_calculate_state_variables(self):

        # Setting the row and column variable for each tile
        for i, row in enumerate(self.board):
            for j, t in enumerate(row):
                t.row = i
                t.column = j
                #t.reachability_mark = False

        # Setting the reachability tiles for each player
        for p in self.players:
            p.re_calculate_reachable_tiles(self)

            # if self.current_player == p:
            #     for t in p.reachable_tiles:
            #         t.reachability_mark = True

    def previous_player(self):
        index = self.players.index(self.current_player)
        return self.players[(index + len(self.players) - 1) % len(self.players)]

    @property
    def current_tile_action(self):
        return self._current_tile_action

    @current_tile_action.setter
    def current_tile_action(self, current_tile_action):
        self._current_tile_action = current_tile_action
        if self._current_tile_action is not None:
            self.next_phase()

    @property
    def current_move_action(self):
        return self._current_move_action

    @current_move_action.setter
    def current_move_action(self, current_move_action):
        self._current_move_action = current_move_action
        if self._current_move_action is not None:
            self.next_phase()

    @property
    def current_phase(self):
        return self._current_phase

    @current_phase.setter
    def current_phase(self, current_phase):
        self._current_phase = current_phase

    def next_phase(self):
        self.re_calculate_state_variables()
        if self.current_phase == Phase.CHOOSING_TILE:
            self.current_phase = Phase.TILE_MOVING
        elif self.current_phase == Phase.TILE_MOVING:
            self.current_tile_action = None
            self.current_phase = Phase.CHOOSING_PAWN
        elif self.current_phase == Phase.CHOOSING_PAWN:
            self.current_phase = Phase.PAWN_MOVING
        elif self.current_phase == Phase.PAWN_MOVING:
            self.current_move_action = None
            self.current_phase = Phase.CHOOSING_TILE
            self.next_player()

    def next_player(self):
        index = self.players.index(self.current_player)
        self.current_player = self.players[(index + 1) % len(self.players)]


