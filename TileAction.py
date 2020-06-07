class TileAction:

    def __init__(self, selected_side, selected_index, player, distance_moved=0):
        """
        :param selected_side: top, bottom, left or right
        :param distance_moved: how far the new tile has moved, by default 0 in the beginning
        :param player:
        """
        if selected_index not in [1, 3, 5]:
            raise ValueError('The selected index is not a valid value')
        self.selected_side = selected_side
        self.selected_index = selected_index
        self.distance_moved = distance_moved
        self.player = player

