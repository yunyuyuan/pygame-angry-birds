import pygame
from typing import Tuple, Callable, Any
from ..utils.animation import Animation

from src.utils.enums import ButtonTypes
from src.utils.vector import Vector

from ..utils.surface import ElementSurface
from .. import Game

class Button(Animation, ElementSurface):
    def __init__(
        self, 
        pos: Tuple[float, float],
        button_type: ButtonTypes,
        on_click: Callable[[pygame.event.Event], Any] = lambda _: None,
        init_scale = 1.0,
        max_scale = 0.05,
        *args, **kwargs
    ):
        self.img = button_type.value
        self.img_size = Vector(self.img.get_size())
        max_size = self.img_size * (init_scale+max_scale)
        super().__init__(size=max_size, pos=pos, *args, **kwargs)
        self.center_pos = self.size / 2
        self.init_scale = init_scale
        self.max_scale = max_scale
        self.scale = init_scale
        self.on_click = on_click
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.check_mouse_inside(event)
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
                return True
        return False
    
    def animation_step(self, progress):
        self.scale = self.init_scale + progress * self.max_scale
    
    def draw(self):
        self.surface.fill((0, 0, 0, 0))
        new_size = self.img_size * self.scale
        target_rect = pygame.Rect(self.center_pos - new_size / 2, new_size)
        self.surface.blit(pygame.transform.scale(self.img, target_rect.size), target_rect)
        if Game.debug:
            pygame.draw.rect(self.surface, (255, 0, 0), target_rect, width=1)
        super().draw()
