import Objective

import pygame as p

import copy

class Card:

    def __init__(self, objective: Objective=None, image_file_url: str=None):
        self.objective = objective
        if image_file_url is not None:
            image = p.image.load(image_file_url)
            self.image = p.transform.scale(image, (100, 150))

    def copy(self):
        copy_obj = Card()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copy_obj.__dict__[name] = attr.copy()
            else:
                copy_obj.__dict__[name] = copy.deepcopy(attr)
        return copy_obj
