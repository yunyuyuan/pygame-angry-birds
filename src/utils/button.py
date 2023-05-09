import pygame
from typing import Tuple

from ..surface import EventSurface
from .img import clip_img
from .. import Game

ImgMap = {
    "setting": ((10, 10), (10, 10))
}

class Button(EventSurface):
    def __init__(
        self, 
        parent: pygame.Surface,
        size: Tuple[float, float],
        pos: Tuple[float, float],
        img: str,
        max_scale = 1.3
    ):
        super().__init__(size)
        self.size = size
        self.pos = pos
        self.parent = parent
        self.scale = 1
        self.img = clip_img("images/BUTTONS_SHEET_1.png", *ImgMap[img])
        
    def mouse_event(self, event: int):
        if event == pygame.MOUSEMOTION:
            pass
        
    def draw(self):
        real_size = self.size
        real_pos = self.pos
        self.parent.blit(self.img, pygame.Rect(real_pos, real_size))
