import pygame
from typing import Tuple

from ..utils.surface import ElementSurface

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
        is_inside = self.check_mouse_inside(event)
        if event.type == pygame.MOUSEMOTION:
            if is_inside:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        return False
        
    def draw(self):
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.color, (self.pos, self.size), border_radius=10)
        super().draw()
