from . import get_asset_path
from typing import Tuple
import pygame

def clip_img(path: str, pos: Tuple[float, float], size: Tuple[float, float]):
    return pygame.image.load(get_asset_path(path)).subsurface(pygame.Rect(pos, size))
