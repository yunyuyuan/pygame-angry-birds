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

        self.bgs = BgEnum['level_'+str(level)].value
        self.skin_surface = make_repeat_surface(self.max_width, pos_y, self.bgs["skin"], lambda h: -h-80)
        self.parallax_surface = make_repeat_surface(self.max_width, pos_y, self.bgs["parallax"], lambda h: -h-16)
        self.ground_surface_1 = make_repeat_surface(self.max_width, pos_y, self.bgs["ground1"], lambda h: -h)
        self.ground_surface_2 = make_repeat_surface(self.max_width, pos_y, self.bgs["ground2"], lambda _: 0)
        self.ground_surface_3 = make_repeat_surface(self.max_width, pos_y, self.bgs["ground3"], lambda h: -h)

    def before_game_draw(self, offset_x: float):
        # parent.fill(self.bgs['sky'], ((0, 0), (parent.get_width(), self.pos_y)))
        skin_offset = abs(offset_x) / 2
        skin_offset = 0 if skin_offset == self.skin_surface[0].get_width() else skin_offset
        parallax_offset = abs(offset_x) / 5
        parallax_offset = 0 if parallax_offset == self.parallax_surface[0].get_width() else parallax_offset

        # parent.blit(self.skin_surface[0], (skin_offset, self.skin_surface[1]))
        # parent.blit(self.parallax_surface[0], (parallax_offset, self.parallax_surface[1]))
        # parent.blit(self.ground_surface_1[0], (0, self.ground_surface_1[1]))
        # parent.fill(self.bgs['ground'], ((0, self.pos_y), (parent.get_width(), parent.get_height() - self.pos_y)))
        # parent.blit(self.ground_surface_2[0], (0, self.ground_surface_2[1]))
        return skin_offset == 0 and parallax_offset == 0
    
    def after_game_draw(self):
        # parent.blit(self.ground_surface_3[0], (0, self.ground_surface_3[1]))
        pass

    
def make_repeat_surface(max_width: float, pos_y: float, single: pygame.Surface, process: Callable[[int], int]):
    single = pygame.transform.scale_by(single, 1.6)
    (width, height) = single.get_size()
    count = math.ceil(max_width / width) + 1
    surface = pygame.Surface((width*count, height), flags=pygame.SRCALPHA)
    for i in range(count):
        surface.blit(single, (i * width, 0))
    return surface, pos_y+process(surface.get_height()), single


class BgEnum(Enum):
    level_4 = {
        "sky": "#90cded",
        "skin": clip_img("images/INGAME_SKIES_1.png", (490, 1), (492, 270)),
        "parallax": clip_img("images/INGAME_PARALLAX_4.png", (1, 1), (482, 117)),
        "ground1": clip_img("images/INGAME_PARALLAX_4.png", (0, 146), (483, 70)),
        "ground2": clip_img("images/INGAME_GROUNDS_1.png", (345, 3), (482, 202)),
        "ground3": clip_img("images/INGAME_PARALLAX_4.png", (1, 120), (482, 26)),
        "ground": "#1c120c"
    }