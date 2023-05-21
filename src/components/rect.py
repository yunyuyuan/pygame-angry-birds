import pygame
from typing import Tuple

from ..surface import ElementSurface
from .. import Game

class RectSurface(ElementSurface):
    def __init__(
        self, 
        size: Tuple[float, float],
        pos: Tuple[float, float],
        color: pygame.Color,
        *args, **kwargs
    ):
        super().__init__(size=size, pos=pos, *args, **kwargs)
        self.color = color
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.is_mouse_inside(event)
        if event.type == pygame.MOUSEMOTION:
            if is_inside:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        return False
        
    def draw(self):
        real_size = self.size
        real_pos = self.pos
        pygame.draw.rect(self.parent.surface, self.color, (self.pos, self.size))
