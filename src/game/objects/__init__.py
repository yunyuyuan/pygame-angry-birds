from typing import Tuple
import pygame
import pymunk
from src.utils.enums import CollisionTypes, ObstacleTypes

from src.utils.surface import BaseSurface
from src.utils.vector import Vector

__all__ = [
    "FixedLineObject",
    "FixedPolyObject",
    "ObstacleRectObject",
    "OrangeBirdObject"
]

class GameObject(BaseSurface):
    '''
    pymunk & pygame
    游戏对象，用于创建一个物理引擎内的物体，并可以画到屏幕上
    '''
    def __init__(self, angle: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body: pymunk.Body
        self.angle = angle
        self.shape = pymunk.Shape


class GameCollisionObject(GameObject):
    '''
    带碰撞的GameObject
    '''
    def __init__(self, collision_type: CollisionTypes, *args, **kwargs):
        super().__init__(size=collision_type.surfaces[0].get_size(),*args, **kwargs)
        self.collision_type = collision_type
        
        # 首次把状态设为 0
        self.collision_status = 0

    @property
    def current_surface(self):
        return self.collision_type.surfaces[self.collision_status]

    def collision(self, ke: float):
        pass


class GameObstacleObject(GameCollisionObject):
    def __init__(self, pos: Tuple[float, float], type: str, angle: float, *args, **kwargs):
        super().__init__(
            pos=pos,
            collision_type=ObstacleTypes[type],
            angle=angle,
            *args, **kwargs
        )

    def draw(self):
        # self.surface.fill((0, 0, 0, 0))
        self.parent_surface.blit(pygame.transform.rotate(self.current_surface, self.angle), (self.pos, self.size))
        # return super().draw()

class GameBirdObject(GameCollisionObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# from .fixed_line import FixedLineObject
# from .fixed_poly import FixedPolyObject
# from .obstacle_rect import ObstacleRectObject
# from .orange_bird import OrangeBirdObject