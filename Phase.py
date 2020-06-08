from enum import Enum


class Phase(Enum):
    CHOOSING_TILE = 1
    TILE_MOVING = 2
    CHOOSING_PAWN = 3
    PAWN_MOVING = 4
