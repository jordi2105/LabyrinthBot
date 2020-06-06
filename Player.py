import Card
from abc import ABC, abstractmethod

class Player(ABC):


    @abstractmethod
    def do_turn(self):
        pass
