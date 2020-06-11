import Objective

import pygame as p


class Card:

    def __init__(self, objective: Objective, image_file_url: str):
        self.objective = objective
        image = p.image.load(image_file_url)
        self.image = p.transform.scale(image, (100, 150))
