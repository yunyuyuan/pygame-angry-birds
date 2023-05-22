import pygame
from typing import Tuple, Callable, Any

from src.utils.enums import ButtonImgMap
from src.utils.vector import Vector

from ..surface import ElementSurface, Animation
from ..utils.img import clip_img
from .. import Game

class Button(Animation, ElementSurface):
    def __init__(
        self, 
        pos: Tuple[float, float],
        img: ButtonImgMap,
        on_click: Callable[[pygame.event.Event], Any] = lambda _: None,
        init_scale = 1.0,
        max_scale = 0.2,
        *args, **kwargs
    ):
        self.img_size = Vector(img.value[1])
        max_size = self.img_size * (init_scale+max_scale)
        super().__init__(size=max_size, pos=pos, *args, **kwargs)
        self.center_pos = self.pos + self.size / 2
        self.init_scale = init_scale
        self.max_scale = max_scale
        self.scale = init_scale
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
        self.scale = self.init_scale + progress * self.max_scale
    
    def draw(self):
        new_size = self.img_size * self.scale
        target_rect = pygame.Rect(self.center_pos - new_size / 2, new_size)
        self.parent.surface.blit(pygame.transform.scale(self.img, target_rect.size), target_rect)
        if Game.debug:
            pygame.draw.rect(self.parent.surface, pygame.Color(255, 0, 0), target_rect, width=1)
            pygame.draw.rect(self.parent.surface, pygame.Color(255, 0, 0), (self.pos, self.surface.get_size()), width=1)
