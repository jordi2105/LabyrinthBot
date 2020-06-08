from Player import Player
from TileAction import TileAction


class Bot(Player):
    def do_turn(self, gamestate):
        self.place_tile(gamestate)
        self.move_pawn(gamestate)

    def place_tile(self, gamestate):
        action = TileAction(selected_side='top', selected_index=1, player=gamestate.current_player)
        gamestate.current_tile_action = action

    def move_pawn(self, gamestate):
        reachable_neighbors = self.reachable_tiles(gamestate, self.current_location, [])
        for t in reachable_neighbors:
            t.reachability_mark = True
        a = 1
       # self.current_location = new_location








