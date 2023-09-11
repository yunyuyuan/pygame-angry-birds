
from typing import Callable, List, Optional, Tuple
import pygame
from src import Game
from src.utils.surface import ChildType, ContainerSurface, ElementSurface
from src.utils.animation import Animation


class SidePanel(Animation, ContainerSurface):
    def __init__(self, width: float, *args, **kwargs):
        super().__init__(speed=150, size=(Game.geometry.x, Game.geometry.y), pos=(0, 0), *args, **kwargs)
        self.container_surface = SidePanelContainer(width=width)
        super().add_children([self.container_surface])
        self.bg_color: pygame.Color = pygame.Color(0, 0, 0, 0)
        self.visible = False
    
    def add_children(self, children: List[ChildType]):
        self.container_surface.add_children(children)
    
    def toggle(self):
        self.animation_state = -self.animation_state
        if self.animation_state == 1:
            self.visible = True
        
    def animation_step(self, progress):
        self.container_surface.pos = ((progress - 1) * self.container_surface.size.x, self.container_surface.pos[1])
        self.bg_color.a = int(125 * progress)
    
    def animate_down(self):
        if self.animation_state == -1:
            self.visible = False

    def draw(self):
        self.surface.fill(self.bg_color)
        return super().draw()

class SidePanelContainer(ContainerSurface):
    def __init__(self, width: float, *args, **kwargs):
        super().__init__(size=(width, Game.geometry.y), pos=(-width, 0), *args, **kwargs)
    
    def draw(self):
        self.surface.fill('#298772')
        return super().draw()
