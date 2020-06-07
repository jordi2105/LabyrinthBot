from Player import Player
from TileAction import TileAction


class Bot(Player):
    def do_turn(self, gamestate):
        action = TileAction(selected_side='top', selected_index=1, player=gamestate.current_player)
        gamestate.current_tile_action = action

