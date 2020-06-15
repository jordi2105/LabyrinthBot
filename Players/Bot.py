from abc import ABC, abstractmethod
from Players.Player import Player


class Bot(Player):

    @abstractmethod
    def place_tile(self, gamestate):
        pass

    @abstractmethod
    def move_pawn(self, gamestate):
        pass
