from typing import Tuple, Sequence
import pymunk
import pygame
from . import GameObject
from ... import Game

class FixedPolyObject(GameObject):
    def __init__(
        self, 
        vertices: Sequence[Tuple[float, float]],
        pos: Tuple[float, float]
    ):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.friction = 0.5
        self.body.position = pos
        self.body.angle = 0

        Game.space.add(self.body, self.shape)

    def draw(self):
        ps = [
            p.rotated(self.shape.body.angle) + self.shape.body.position
            for p in self.shape.get_vertices()
        ]
        ps = [(round(p.x), round(Game.screen.get_height() - p.y)) for p in ps]
        ps += [ps[0]]
        pygame.draw.lines(Game.screen, pygame.Color("red"), False, ps, 1)
