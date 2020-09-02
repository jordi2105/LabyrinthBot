import copy


class TileAction:

    def __init__(self, selected_side='top', selected_index=1, player=None, distance_moved=0):
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

    def copy(self):
        copy_obj = TileAction()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copy_obj.__dict__[name] = attr.copy()
            else:
                copy_obj.__dict__[name] = copy.deepcopy(attr)
        return copy_obj
