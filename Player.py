import Card
from abc import ABC, abstractmethod
from Tile import Tile

class Player(ABC):

    def __init__(self, name, current_location: Tile, color: str):
        self.name = name
        self.current_location = current_location
        self.color = color


    @abstractmethod
    def do_turn(self, gamestate):
        pass
