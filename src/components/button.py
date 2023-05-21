import pygame
from typing import Tuple, Callable, Any

from src.utils.enums import ButtonImgMap

from ..surface import ElementSurface, Animation
from ..utils.img import clip_img
from .. import Game

class Button(Animation, ElementSurface):
    def __init__(
        self, 
        pos: Tuple[float, float],
        img: ButtonImgMap,
        on_click: Callable[[pygame.event.Event], Any] = lambda _: None,
        max_scale = 1.1,
        *args, **kwargs
    ):
        super().__init__(size=img.value[1], pos=pos, *args, **kwargs)
        self.scale = 1
        self.max_scale = max_scale - 1
        self.img_type = img
        self.on_click = on_click
        self.img = clip_img("images/BUTTONS_SHEET_1.png", *img.value)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.is_mouse_inside(event)
        if event.type == pygame.MOUSEMOTION:
            if is_inside:
                # button 放大动画
                self.animation_state = 1
            else:
                # button 缩小动画
                self.animation_state = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_inside:
                self.on_click(event)
        return False
    
    def animation_step(self, progress):
        self.scale = 1 + progress * self.max_scale
    
    def draw(self):
        real_width = self.size[0] * self.scale
        real_height = self.size[1] * self.scale
        target_rect = pygame.Rect((self.pos[0]-(real_width-self.size[0])/2, self.pos[1]-(real_height-self.size[1])/2), (real_width, real_height))
        self.parent.surface.blit(pygame.transform.scale(self.img, target_rect.size), target_rect)
        if Game.debug:
            pygame.draw.rect(self.parent.surface, pygame.Color(255, 0, 0), target_rect, width=1)
