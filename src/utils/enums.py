from enum import Enum
from typing import Generator, Tuple

import pygame

from src.utils import get_asset_path, load_subsurfaces, clip_img


class ButtonTypes(Enum):
    setting = clip_img("images/BUTTONS_SHEET_1.png", (10, 10), (10, 10))
    pause = clip_img("images/BUTTONS_SHEET_1.png", (254, 739), (99, 108))
    resume = clip_img("images/BUTTONS_SHEET_1.png", (902, 294), (71, 80))
    reset = clip_img("images/BUTTONS_SHEET_1.png", (254, 852), (99, 108))

    # my buttons
    my_materials = clip_img("images/MY_BUTTONS.png", (13,26), (148, 166))
    my_preview = clip_img("images/MY_BUTTONS.png", (516,26), (148, 166))
    my_delete = clip_img("images/MY_BUTTONS.png", (688,26), (148, 166))


class MaterialType(Enum):
    glass = 1
    wood = 2
    stone = 3
    bird = 4
    pig = 5

MaterialCollisionScore = {
    MaterialType.wood: 10000000,
    MaterialType.stone: 10000000,
    MaterialType.bird: 10000000,
    MaterialType.pig: 10000000,
    MaterialType.glass: 10000000
}

class MaterialShape(Enum):
    box = 1
    hollow_box = 2
    circle = 3
    triangle = 4


class CollisionTypes(Enum):
    @property
    def surfaces(self) -> Tuple[pygame.Surface, pygame.Surface, pygame.Surface, pygame.Surface]:
        return super().value[0]

    @property
    def size(self):
        return self.surfaces[0].get_size()

    @property
    def material_type(self) -> MaterialType:
        return super().value[1]

    @property
    def material_shape(self) -> MaterialShape:
        return super().value[2]


class BirdTypes(CollisionTypes):
    red = (tuple(load_subsurfaces("INGAME_BIRDS_1", (46, 46), (903, 797), (903, 797), (903, 797), (903, 797))), MaterialType.bird, MaterialShape.circle)
    orange = 2
    blue = 3

class ObstacleTypes(CollisionTypes):
    w4_h1_wood_box = (tuple(load_subsurfaces("INGAME_BLOCKS_1", (85, 22), (309, 1017), (394, 1105), (394, 1105), (394, 1105))), MaterialType.wood, MaterialShape.box)
    w4_h1_glass_box = (tuple(load_subsurfaces("INGAME_BLOCKS_1", (85, 22), (394, 1017), (309, 1061), (394, 1105), (309, 1127))), MaterialType.wood, MaterialShape.box)
    w4_h1_stone_box = (tuple(load_subsurfaces("INGAME_BLOCKS_1", (85, 22), (394, 1127), (394, 1105), (309, 1105), (309, 1105))), MaterialType.stone, MaterialShape.box)

    w10_h1_wood_box = (tuple(load_subsurfaces("INGAME_BLOCKS_1", (206, 22), (309, 643), (516, 643), (723, 643), (309, 665))), MaterialType.wood, MaterialShape.box)
    w10_h1_glass_box = (tuple(load_subsurfaces("INGAME_BLOCKS_1", (206, 22), (516, 665), (723, 665), (309, 687), (516, 687))), MaterialType.glass, MaterialShape.box)
    w10_h1_stone_box = (tuple(load_subsurfaces("INGAME_BLOCKS_1", (206, 22), (723, 709), (723, 687), (309, 709), (516, 709))), MaterialType.stone, MaterialShape.box)

    w4_h4_wood_hollow_box =(tuple(load_subsurfaces("INGAME_BLOCKS_1", (84, 84), (761, 0) , (761, 84), (845, 0), (845, 84))), MaterialType.wood, MaterialShape.hollow_box)

    w1_h1_stone_circle =(tuple(load_subsurfaces("INGAME_BLOCKS_2", (41, 41), (620, 416), (661, 416), (702, 416), (743, 416))), MaterialType.stone, MaterialShape.circle)

class PigTypes(CollisionTypes):
    normal_pig = (tuple(load_subsurfaces("INGAME_BIRDS_1", (99, 99), (297, 355), (297, 454), (297, 553), (297, 652))), MaterialType.pig, MaterialShape.circle)

class SpecialItems(Enum):
    SlingShotBack = clip_img("images/INGAME_BIRDS_1.png", (0, 0), (40, 201))
    SlingShotFront = clip_img("images/INGAME_BIRDS_1.png", (832, 0), (45, 126))
