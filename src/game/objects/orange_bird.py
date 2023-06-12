# import pymunk
# import pygame
# import math

# from src.utils import pymunk_to_pygame
# from src.utils.img import load_bird
# from . import GameBirdObject
# from src import Game
# from .. import collision_types

# class OrangeBirdObject(GameBirdObject):
#     def __init__(
#         self, 
#         bird_type: int,
#         launch_pos: pymunk.Vec2d,
#         slingshot_pos: pymunk.Vec2d,
#     ):
#         self.bird_type = bird_type
#         super().__init__()

#         self.bird_radius = 24
#         moment = pymunk.moment_for_circle(10, 0, self.bird_radius)
#         self.body = pymunk.Body(10, moment)
#         self.body.position = launch_pos
#         self.shape = pymunk.Circle(self.body, self.bird_radius)
#         self.shape.collision_type = collision_types["bird"]
#         self.shape.friction = 1
        
#         Game.space.add(self.body, self.shape)
#         # 初始速度
#         impulse = launch_pos.get_distance(slingshot_pos) * 100
#         angle = pymunk.Vec2d(abs(slingshot_pos.x - launch_pos.x), 0).get_angle_between(slingshot_pos - launch_pos)
#         impulse = impulse * pymunk.Vec2d(1, 0)
#         impulse = impulse.rotated(angle)
#         self.body.apply_impulse_at_world_point(impulse, self.body.position)
        
#     def draw(self):
#         pygame.draw.circle(Game.screen, pygame.Color("blue"), center=pymunk_to_pygame(self.body.position), radius=self.bird_radius)
#         p = pymunk_to_pygame(self.body.position)

#         angle_degrees = math.degrees(self.body.angle)
#         rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)

#         offset = pymunk.Vec2d(*rotated_logo_img.get_size()) / 2
#         p = p - offset

#         Game.screen.blit(rotated_logo_img, (round(p.x), round(p.y)))
#         return super().draw()
    
#     def load_img(self) -> pygame.Surface:
#         return load_bird(self.bird_type, self.collision_status)
    
#     def collision(self, ke: float):
#         self.collision_status = 1
#         return super().collision(ke)
