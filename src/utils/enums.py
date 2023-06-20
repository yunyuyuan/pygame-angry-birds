from enum import Enum
from typing import Generator, Tuple

import pygame

from src.utils import get_asset_path

class ButtonTypes(Enum):
    setting = ((10, 10), (10, 10))
    pause = ((254, 739), (99, 108))
    resume = ((902, 294), (71, 80))
    reset = ((254, 852), (99, 108))

    # my buttons
    my_materials = ((13,26), (148, 166))
    my_preview = ((516,26), (148, 166))
    my_delete = ((688,26), (148, 166))


class BirdTypes(Enum):
    red = 1,
    orange = 2,
    blue = 3,


class MaterialType(Enum):
    glass = 1
    wood = 2
    bird = 3
    stone = 4
    

class MaterialShape(Enum):
    box = 1
    hollow_box = 2
    circle = 3
    triangle = 4


def _load_obstacle(i: str, size: Tuple[int, int], *pos: Tuple[int, int]):
    img = pygame.image.load(get_asset_path(f"images/INGAME_BLOCKS_{i}.png"))
    for p in pos:
        yield img.subsurface(pygame.Rect(p, size))


class CollisionTypes(Enum):
    @property
    def surfaces(self) -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]:
        return super().value[0]

    @property
    def size(self) -> Tuple[int, int]:
        return self.surfaces[0].get_size()

    @property
    def material_type(self) -> MaterialType:
        return super().value[1]

    @property
    def material_shape(self) -> MaterialType:
        return super().value[2]


class ObstacleTypes(CollisionTypes):
    w4_h1_wood_box = (tuple(_load_obstacle("1", (85, 22), (309, 1017), (394, 1105), (394, 1105), (394, 1105))), MaterialType.wood, MaterialShape.box)
    w10_h1_wood_box = (tuple(_load_obstacle("1", (206, 22), (309, 643), (516, 643), (723, 643), (309, 665))), MaterialType.wood, MaterialShape.box)

    w4_h4_wood_hollow_box =(tuple(_load_obstacle("1", (84, 84), (761, 0) , (761, 84), (845, 0), (845, 84))), MaterialType.wood, MaterialShape.hollow_box)

    w1_h1_stone_circle =(tuple(_load_obstacle("2", (41, 41), (620, 416), (661, 416), (702, 416), (743, 416))), MaterialType.stone, MaterialShape.circle)
