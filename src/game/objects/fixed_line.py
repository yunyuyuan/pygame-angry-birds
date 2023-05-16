from typing import Tuple
import pymunk
import pygame
from . import GameObject
from ... import Game

class FixedLineObject(GameObject):
    def __init__(
        self, 
        pos_a: Tuple[float, float], 
        pos_b: Tuple[float, float],
    ):
        self.line = pymunk.Segment(Game.space.static_body, pos_a, pos_b, 0.0)
        self.line.friction = 0.5
        Game.space.add(self.line)
        
    def draw(self):
        body = self.line.body

        pv1 = body.position + self.line.a.rotated(body.angle)
        pv2 = body.position + self.line.b.rotated(body.angle)
        p1 = round(pv1.x), Game.screen.get_height() - round(pv1.y)
        p2 = round(pv2.x), Game.screen.get_height() - round(pv2.y)
        pygame.draw.lines(Game.screen, pygame.Color("black"), False, [p1, p2], 2)
