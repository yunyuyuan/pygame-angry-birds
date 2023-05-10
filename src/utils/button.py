import pygame
from typing import Tuple

from src.utils.enums import ButtonImgMap

from ..surface import ElementSurface
from .img import clip_img
from .. import Game

class Button(ElementSurface):
    def __init__(
        self, 
        size: Tuple[float, float],
        pos: Tuple[float, float],
        img: ButtonImgMap,
        max_scale = 1.3
    ):
        super().__init__()
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
        Game.screen.blit(self.img, pygame.Rect(real_pos, real_size))
