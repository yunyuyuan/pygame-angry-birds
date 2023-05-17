import pygame
from typing import Tuple, Union

from src.utils.enums import ButtonImgMap

from ..surface import ElementSurface, AnimationSurface
from ..utils.img import clip_img
from .. import Game

class Button(ElementSurface, AnimationSurface):
    def __init__(
        self, 
        pos: Tuple[float, float],
        img: ButtonImgMap,
        max_scale = 1.3,
        *args, **kwargs
    ):
        super().__init__(size=img.value[1], pos=pos, *args, **kwargs)
        self.scale = 1
        self.img_type = img
        self.img = clip_img("images/BUTTONS_SHEET_1.png", *img.value)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.is_mouse_inside(event)
        if event.type == pygame.MOUSEMOTION:
            if is_inside:
                # button 放大动画
                print(self.img_type)
            else:
                # button 缩小动画
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        return False
    
    def draw(self):
        real_size = self.size
        real_pos = self.pos
        target_rect = pygame.Rect(real_pos, real_size)
        self.parent.surface.blit(self.img, target_rect)
        if Game.debug:
            pygame.draw.rect(self.parent.surface, pygame.Color(255, 0, 0), target_rect, width=1)
