
import pygame
from src import Game
from src.utils.surface import ContainerSurface
from src.utils.animation import Animation


class SidePanel(Animation, ContainerSurface):
    def __init__( 
            self,
            width: float,
            right = False,
            *args, **kwargs
        ):
        super().__init__(speed=1500, size=(width, Game.geometry[1]), pos=(0, 0), pos_right=right, *args, **kwargs)
        self.pos = [-self.size[0], self.pos[1]]
    
    def toggle(self):
        self.animation_state = -self.animation_state
        
    def animation_step(self, progress):
        self.pos = [(progress - 1) * self.size[0], self.pos[1]]
