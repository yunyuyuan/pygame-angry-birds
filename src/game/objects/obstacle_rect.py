# import math
# from typing import Tuple
# import pymunk
# import pygame

# from src.utils import pymunk_to_pygame
# from . import GameObstacleObject
# from .. import collision_types
# from src.utils.img import load_obstacle_rect
# from ... import Game

# class ObstacleRectObject(GameObstacleObject):
#     def __init__(
#         self, 
#         rect_type: int,
#         pos: Tuple[float, float],
#         size: Tuple[float, float],
#     ):
#         self.rect_type = rect_type
#         super().__init__()
#         moment = pymunk.moment_for_box(10, size)
#         self.body = pymunk.Body(10, moment, body_type=pymunk.Body.DYNAMIC)
#         self.shape = pymunk.Poly.create_box(self.body, size=size)
#         self.shape.friction = 0.5
#         self.shape.collision_type = collision_types["obstacle"]
#         self.body.position = pos
#         self.body.angle = 0

#         Game.space.add(self.body, self.shape)

#     def draw(self):
#         ps = [
#             p.rotated(self.shape.body.angle) + self.shape.body.position
#             for p in self.shape.get_vertices()
#         ]
#         ps = [(round(p.x), round(Game.screen.get_height() - p.y)) for p in ps]
#         ps += [ps[0]]
#         pygame.draw.lines(Game.screen, pygame.Color("red"), False, ps, 1)
        
#         p = pymunk_to_pygame(self.body.position)

#         angle_degrees = math.degrees(self.body.angle)
#         rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)

#         offset = pymunk.Vec2d(*rotated_logo_img.get_size()) / 2
#         p = p - offset

#         Game.screen.blit(rotated_logo_img, (round(p.x), round(p.y)))
#         return super().draw()
    
#     def load_img(self) -> pygame.Surface:
#         return load_obstacle_rect(self.rect_type, self.collision_status)
    
#     def collision(self, kc: float):
#         self.collision_status = 1
#         return super().collision(kc)
