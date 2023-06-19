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


def _load_obstacle(i: str, *pos: Tuple[int, int, int, int]):
    img = pygame.image.load(get_asset_path(f"images/INGAME_BLOCKS_{i}.png"))
    for p in pos:
        yield img.subsurface(pygame.Rect(p))


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
    w4_h1_wood_box = (tuple(_load_obstacle("1", (309, 1017, 85, 22), (394, 1105, 85, 22), (394, 1105, 85, 22), (394, 1105, 85, 22))), MaterialType.wood, MaterialShape.box)

    w4_h4_wood_hollow_box =(tuple(_load_obstacle("1", (761, 0, 84, 84), (761, 84, 84, 84), (845, 0, 84, 84), (845, 84, 84, 84))), MaterialType.wood, MaterialShape.hollow_box)

    w1_h1_stone_circle =(tuple(_load_obstacle("2", (620, 416, 41, 41), (661, 416, 41, 41), (702, 416, 41, 41), (743, 416, 41, 41))), MaterialType.stone, MaterialShape.circle)
