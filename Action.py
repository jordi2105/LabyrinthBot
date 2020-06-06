class Action:

    def __init__(self, selected_side, selected_index, distance_moved, player):
        """
        :param selected_side: top, bottom, left or right
        :param distance_moved:
        :param player:
        """
        self.selected_side = selected_side
        self.selected_index = selected_index
        self.distance_moved = distance_moved
        self.player = player

