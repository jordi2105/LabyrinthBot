from abc import ABC, abstractmethod
from Players.Player import Player
import random

class Bot(Player):

    @abstractmethod
    def place_tile(self, gamestate):
        pass

    @abstractmethod
    def move_pawn(self, gamestate):
        pass

    # def choose_random_route(self, gamestate, routes):
    #     random_route = random.choice(routes)
    #     return random_route
