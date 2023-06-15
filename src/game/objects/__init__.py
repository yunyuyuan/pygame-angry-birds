import math
from typing import Tuple
import pygame
import pymunk
from src import Game
from src.utils.enums import CollisionTypes, MaterialShape, ObstacleTypes

from src.utils.surface import BaseSurface
from src.utils.vector import Vector


class GameObject(BaseSurface):
    '''
    pymunk & pygame
    游戏对象，用于创建一个物理引擎内的物体，并可以画到屏幕上
    '''
    def __init__(self, angle = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body: pymunk.Body
        self.shape: pymunk.Poly | pymunk.Circle
        self.angle = angle

    def reload(self):
        pass

    def draw(self):
        raise NotImplementedError("You should create draw() of GameObject")

class GameCollisionObject(GameObject):
    '''
    带碰撞的GameObject
    '''
    def __init__(self, space: pymunk.Space, collision_type: CollisionTypes, *args, **kwargs):
        super().__init__(size=collision_type.size,*args, **kwargs)
        self.space = space
        self.collision_type = collision_type
        
        # 首次把状态设为 0
        self.collision_status = 0
    
    def add_to_space(self):
        self.space.add(self.body, self.shape)

    def remove_from_space(self):
        self.space.remove(self.body, self.shape)

    @property
    def current_surface(self):
        return self.collision_type.surfaces[self.collision_status]

    def collision(self, ke: float):
        pass

    def draw(self):
        real_pos = (self.pos[0], self.parent.size[1] - self.pos[1])
        self.parent_surface.blit(pygame.transform.rotate(self.current_surface, self.angle), (real_pos, self.size))


class GameObstacleObject(GameCollisionObject):
    def __init__(self, pos: Tuple[float, float], type: str, angle: float, *args, **kwargs):
        super().__init__(
            pos=pos,
            collision_type=ObstacleTypes[type],
            angle=angle,
            *args, **kwargs
        )
        if self.collision_type.material_shape == MaterialShape.box:
            moment = pymunk.moment_for_box(10, self.collision_type.size)
            self.body = pymunk.Body(10, moment, body_type=pymunk.Body.DYNAMIC)
            self.shape = pymunk.Poly.create_box(self.body, size=self.collision_type.size)
            self.shape.friction = 0.5
            self.shape.collision_type = self.collision_type.material_type.value
            self.body.position = self.pos
            self.body.angle = self.angle
        else:
            pass
        self.deleting_focus = False
        self.add_to_space()

    def reload(self):
        self.body.position = self.pos
        self.body.angle = self.angle
        self.body.velocity = (0,0)
        self.body.angular_velocity = 0
        return super().reload()
    
    def check_mouse_inside(self, pos: Tuple[float, float]):
        if isinstance(self.shape, pymunk.Poly):
            self.deleting_focus = self.shape.point_query(pos).distance <= 0
        elif isinstance(self.shape, pymunk.Circle):
            pass
        return self.deleting_focus
    
    def draw(self):
        pos = (self.body.position.x, self.parent.size[1] - self.body.position.y)

        angle_degrees = math.degrees(self.body.angle)
        rotated_surface = pygame.transform.rotate(self.current_surface, angle_degrees)

        offset = pymunk.Vec2d(*rotated_surface.get_size()) / 2
        pos = pos - offset

        self.parent_surface.blit(rotated_surface, (pos.x, pos.y))
        if Game.debug or self.deleting_focus:
            if isinstance(self.shape, pymunk.Poly):
                ps = [
                    p.rotated(self.shape.body.angle) + self.shape.body.position
                    for p in self.shape.get_vertices()
                ]
                ps = [(round(p.x), round(self.parent.size[1] - p.y)) for p in ps]
                ps += [ps[0]]
                pygame.draw.lines(self.parent_surface, pygame.Color("red") if self.deleting_focus else pygame.Color("black"), False, ps, 1)


class GameBirdObject(GameCollisionObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# from .fixed_line import FixedLineObject
# from .fixed_poly import FixedPolyObject
# from .obstacle_rect import ObstacleRectObject
# from .orange_bird import OrangeBirdObject