import pygame
from typing import Tuple, Union

from src.utils.enums import ButtonImgMap

from ..surface import ElementSurface, AnimationSurface
from ..utils.img import clip_img
from .. import Game

class Button(ElementSurface, AnimationSurface):
    def __init__(
        self, 
        size: Tuple[float, float],
        pos: Tuple[float, float],
        img: ButtonImgMap,
        max_scale = 1.3,
        *args, **kwargs
    ):
        super().__init__(size = size, *args, **kwargs)
        self.size = size
        self.pos = pos
        self.scale = 1
        self.img = clip_img("images/BUTTONS_SHEET_1.png", *img.value)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        return False
        
    def draw(self):
        real_size = self.size
        real_pos = self.pos
        self.parent.surface.blit(self.img, pygame.Rect(real_pos, real_size))
