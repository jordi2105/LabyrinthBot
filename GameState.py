from TileAction import TileAction
from Phase import Phase

import copy


class GameState:
    def __init__(self, players=None, board=None, current_tile=None, current_player=None, current_tile_action=None,
                 last_mouse_click_location=None, current_move_action=None, current_phase=Phase.CHOOSING_TILE,
                 recalculate_state_variables=True):
        self.board = board  # 2d array of Tiles [rows][columns]
        self.current_tile = current_tile
        self.players = players
        self.current_player = current_player
        self._current_tile_action = current_tile_action
        self.last_mouse_click_location = last_mouse_click_location
        self._current_move_action = current_move_action
        self._current_phase = current_phase
        self.player_won = None

        if recalculate_state_variables:
            self.recalculate_state_variables()

    def recalculate_state_variables(self):

        # Setting the row and column variable for each tile
        for i, row in enumerate(self.board):
            for j, t in enumerate(row):
                t.row = i
                t.column = j
                # t.reachability_mark = False

        self.current_tile.row = 0
        self.current_tile.column = 0

        # Setting the reachability tiles for each player
        for p in self.players:
            p.update_properties(self)

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

        self.recalculate_state_variables()

    def next_player(self):
        index = self.players.index(self.current_player)
        self.current_player = self.players[(index + 1) % len(self.players)]

    def copy(self):
        board = [[0 for x in range(7)] for y in range(7)]
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                board[i][j] = tile.copy()
        players = []
        for player in self.players:
            players.append(player.copy())

        copyobj = GameState(players=players, board=board, recalculate_state_variables=False)
        for name, attr in self.__dict__.items():
            if name in ['board', 'players'] or attr is None:
                continue
            if (hasattr(attr, 'copy') and callable(getattr(attr, 'copy'))) or name in ['_current_tile_action',
                                                                                       '_current_move_action']:
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)

        copyobj.set_references_after_copy()
        copyobj.copy_check()
        return copyobj

    def set_references_after_copy(self):
        # Setting the right reference to player.current_location
        # Setting the right reference of the player's cards
        for player in self.players:
            player.current_location = self.get_tile_by_url(player.current_location.image_file_url)
            if player.current_card is not None:
                player.current_card = next((c for c in player.cards if c.objective == player.current_card.objective),
                                           None)

        # Setting the right reference to current_player
        current_player = next((p for p in self.players if p.name == self.current_player.name), None)
        self.current_player = current_player

        # Setting the right references of current_move_action
        if self.current_move_action is not None:
            new_route = []
            for t in self.current_move_action.route:
                tile = self.get_tile_by_url(t.url)
                new_route.append(tile)
            self.current_move_action.route = new_route
            current_tile = self.get_tile_by_url(self.current_move_action.current_tile.image_file_url)
            self.current_tile = current_tile

        # Setting the right references of current_tile_action
        if self.current_tile_action is not None:
            player = next((p for p in self.players if p.name == self.current_tile_action.player.name), None)
            self.current_tile_action.player = player

    # def copy(self):
    #     gs = GameState(recalculate_state_variables=False)
    #     for name, attr in self.__dict__.items():
    #         if name == 'board':
    #             gs.board = attr
    #             for i, row in enumerate(attr):
    #                 for j, tile in enumerate(row):
    #                     gs.board[i][j] = attr[i][j].copy()
    #         elif hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
    #             gs.__dict__[name] = attr.copy()
    #         else:
    #             gs.__dict__[name] = copy.deepcopy(attr)
    #
    #     gs.recalculate_state_variables()
    #
    #     # # Setting the right reference to player.current_location
    #     # for player in gs.players:
    #     #     url = player.current_location.image_file_url
    #     #     tile = gs.get_tile_by_url(url)
    #     #     player.current_location = tile
    #     #
    #     # # Setting the right reference to current_player
    #     # current_player = next((p for p in gs.players if p.name == gs.current_player.name), None)
    #     # gs.current_player = current_player
    #     #
    #     # # Setting the right references of current_move_action
    #     # if gs.current_move_action is not None:
    #     #     new_route = []
    #     #     for t in gs.current_move_action.route:
    #     #         tile = gs.get_tile_by_url(t.url)
    #     #         new_route.append(tile)
    #     #     gs.current_move_action.route = new_route
    #     #     current_tile = gs.get_tile_by_url(gs.current_move_action.current_tile.image_file_url)
    #     #     gs.current_tile = current_tile
    #     #
    #     # # Setting the right references of current_tile_action
    #     # if gs.current_tile_action is not None:
    #     #     player = next((p for p in gs.players if p.name == gs.current_tile_action.player.name), None)
    #     #     gs.current_tile_action.player = player
    #     # gs.copy_check()
    #
    #     return gs

    def get_tile_by_url(self, url):
        return next((t for t in self.all_tiles_on_board() if t.image_file_url == url), None)

    def copy_check(self):
        assert self.current_player in self.players
        all_tiles = self.all_tiles_on_board()
        for player in self.players:
            assert player.current_location in all_tiles
            if player.current_card is not None:
                assert player.current_card in player.cards
        if self.current_move_action is not None:
            assert self.current_move_action.current_tile in all_tiles
            for tile in self.current_move_action.route:
                assert tile in all_tiles
        if self.current_tile_action is not None:
            assert self.current_tile_action.player in self.players

    def all_tiles_on_board(self):
        return [i for sub in self.board for i in sub]
