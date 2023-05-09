# load clipped image resources from png file

from ..game import bird_types, obstacle_rect_types
from . import get_asset_path
from typing import Tuple
import pygame


def clip_img(path: str, pos: Tuple[float, float], size: Tuple[float, float]):
    return pygame.image.load(get_asset_path(path)).subsurface(pygame.Rect(pos, size))

def load_bird(bird_type: int, status: int):
    bird_img = pygame.image.load(get_asset_path("images/INGAME_BIRDS_1.png"))
    if bird_type == bird_types["orange"]:
        if status == 0:
            return bird_img.subsurface(pygame.Rect(667, 878, 61, 56))
        elif status == 1:
            return bird_img.subsurface(pygame.Rect(792, 743, 60, 55))
    return bird_img


def load_obstacle_rect(rect_type: int, status: int):
    rect_img = pygame.image.load(get_asset_path("images/INGAME_BLOCKS_1.png"))
    if rect_type == obstacle_rect_types["4x1"]:
        if status == 0:
            return rect_img.subsurface(pygame.Rect(309, 1017, 85, 22))
        elif status == 1:
            return rect_img.subsurface(pygame.Rect(394, 1105, 85, 22))
    return rect_img