from enum import Enum
from typing import Generator, Tuple

import pygame

from src.utils import get_asset_path

class ButtonImgMap(Enum):
    setting = ((10, 10), (10, 10))
    pause = ((254, 739), (99, 108))
    resume = ((902, 294), (71, 80))
    reset = ((254, 852), (99, 108))

    # my buttons
    my_materials = ((38,26), (148, 166))
    my_move = ((206,26), (148, 166))
    my_rotate = ((375,26), (148, 166))
    my_preview = ((543,26), (148, 166))


class CollisionTypes(Enum):
    bird = 1
    pig = 2
    obstacle = 3


class BirdTypes(Enum):
    red = 1,
    orange = 2,
    blue = 3,


class MaterialType(Enum):
    glass = ()
    wood = ()
    stone = ()

def _load_obstacle(i: str, *pos: Tuple[int, int, int, int]):
    img = pygame.image.load(get_asset_path(f"images/INGAME_BLOCKS_{i}.png"))
    for p in pos:
        yield img.subsurface(pygame.Rect(p))

class ObstacleTypes(Enum):
    # (status0, status1, status2, status3, img, material)
    g_w4_h1 = (*_load_obstacle("1", (309, 1017, 85, 22), (394, 1105, 85, 22), (394, 1105, 85, 22), (394, 1105, 85, 22)), MaterialType.glass)

