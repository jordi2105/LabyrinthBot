import pygame as p
import Tile
from Objective import Objective

class HelpFunctions:

    @staticmethod
    def make_rounded_rect(surface, rect, color, radius=0.4):
        rect = p.Rect(rect)
        color = p.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = p.Surface(rect.size, p.SRCALPHA)

        circle = p.Surface([min(rect.size) * 3] * 2, p.SRCALPHA)
        p.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = p.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=p.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=p.BLEND_RGBA_MIN)

        return surface.blit(rectangle, pos)

    @staticmethod
    def color_to_str(color):
        if color.r == 255 and color.g == 255:
            return 'YELLOW'
        elif color.r == 255:
            return 'RED'
        elif color.g == 255:
            return 'GREEN'
        elif color.b == 255:
            return 'BLUE'



