
from typing import Callable, List, Optional, Tuple
import pygame
from src import Game
from src.utils.surface import ChildType, ContainerSurface, ElementSurface
from src.utils.animation import Animation


class SidePanel(Animation, ContainerSurface):
    def __init__(self, width: float, bg_width: float, *args, **kwargs):
        super().__init__(speed=150, size=(width, Game.geometry.y), pos=(0, 0), *args, **kwargs)
        self.bg_width = bg_width
        self.visible = False
        self.mask_surface = pygame.Surface(Game.geometry, pygame.SRCALPHA)
        self.mask_surface.fill((0, 0, 0, 125))
    
    def toggle(self):
        self.animation_state = -self.animation_state
        if self.animation_state == 1:
            self.visible = True
        
    def animation_step(self, progress):
        self.pos = ((progress - 1) * self.size.x, self.pos[1])
    
    def animate_down(self):
        if self.animation_state == -1:
            self.visible = False

    def draw(self):
        Game.screen.blit(self.mask_surface, (0, 0))
        self.surface.fill('#00000000', ((self.size.x-self.bg_width, 0), (self.bg_width, self.surface.get_height())))
        self.surface.fill('#298772', ((0, 0), (self.bg_width, self.surface.get_height())))
        return super().draw()
