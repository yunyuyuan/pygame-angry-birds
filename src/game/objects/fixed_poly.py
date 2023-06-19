from typing import Tuple, Sequence
import pymunk
import pygame
from . import GameObject
from ... import Game

class FixedPolyObject(GameObject):
    def __init__(
        self,
        space: pymunk.Space,
        vertices: Sequence[Tuple[float, float]],
        pos: Tuple[float, float]
    ):
        super().__init__()
        self.space = space

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shapes = pymunk.Poly(self.body, vertices)
        self.shapes.friction = 0.5
        self.body.position = pos
        self.body.angle = 0

        self.space.add(self.body, self.shapes)

    def draw(self):
        ps = [
            p.rotated(self.shapes.body.angle) + self.shapes.body.position
            for p in self.shapes.get_vertices()
        ]
        ps = [(round(p.x), round(Game.screen.get_height() - p.y)) for p in ps]
        ps += [ps[0]]
        pygame.draw.lines(Game.screen, pygame.Color("red"), False, ps, 1)
