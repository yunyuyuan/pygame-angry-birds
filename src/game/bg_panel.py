import math
from typing import Callable
import pygame
from enum import Enum

from src.utils import clip_img

class BgPanel():
    def __init__(self, max_width: float, level: int, pos_y: float) -> None:
        self.max_width = max_width
        self.level = level
        self.pos_y = pos_y

        bgs = BgEnum['level_'+str(level)].value
        self.skin_surface = self.make_repeat_surface(bgs["skin"], lambda h: -h-50)
        self.parallax_surface = self.make_repeat_surface(bgs["parallax"], lambda h: -h-10)
        self.ground_surface_1 = self.make_repeat_surface(bgs["ground1"], lambda h: -h)
        self.ground_surface_2 = self.make_repeat_surface(bgs["ground2"], lambda _: 0)
        self.ground_surface_3 = self.make_repeat_surface(bgs["ground3"], lambda h: -h)
    
    def make_repeat_surface(self, single: pygame.Surface, process: Callable[[int], int]):
        (width, height) = single.get_size()
        count = math.ceil(self.max_width / width)
        surface = pygame.Surface((width*count, height), flags=pygame.SRCALPHA)
        for i in range(count):
            surface.blit(single, (i * width, 0))
        return surface, (0, self.pos_y+process(surface.get_height()))

    def before_game_draw(self, parent: pygame.Surface):
        parent.blit(*self.skin_surface)
        parent.blit(*self.parallax_surface)
        parent.blit(*self.ground_surface_1)
        parent.blit(*self.ground_surface_2)
    
    def after_game_draw(self, parent: pygame.Surface):
        parent.blit(*self.ground_surface_3)


class BgEnum(Enum):
    level_4 = {
        "skin": clip_img("images/INGAME_SKIES_1.png", (490, 1), (492, 270)),
        "parallax": clip_img("images/INGAME_PARALLAX_4.png", (1, 1), (482, 117)),
        "ground1": clip_img("images/INGAME_PARALLAX_4.png", (0, 146), (483, 70)),
        "ground2": clip_img("images/INGAME_GROUNDS_1.png", (345, 3), (482, 202)),
        "ground3": clip_img("images/INGAME_PARALLAX_4.png", (1, 120), (482, 26)),
    }