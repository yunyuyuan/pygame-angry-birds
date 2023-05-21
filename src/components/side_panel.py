
import pygame
from src import Game
from src.surface import Animation, ContainerSurface


class SidePanel(Animation, ContainerSurface):
    def __init__( 
            self,
            width: float,
            *args, **kwargs
        ):
        super().__init__(speed=150, size=(width, Game.geometry[1]), pos=(0, 0), *args, **kwargs)
        self.pos[0] = -self.size[0]
    
    def toggle(self):
        self.animation_state = -self.animation_state
        
    def animation_step(self, progress):
        self.pos[0] = (progress - 1) * self.size[0]
