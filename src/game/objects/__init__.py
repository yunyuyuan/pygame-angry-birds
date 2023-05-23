import pygame
import pymunk

from src.utils.surface import Drawable

__all__ = [
    "FixedLineObject",
    "FixedPolyObject",
    "ObstacleRectObject",
    "OrangeBirdObject"
]

class GameObject(Drawable):
    '''
    pymunk & pygame
    游戏对象，用于创建一个物理引擎内的物体
    '''
    def __init__(self):
        self.body: pymunk.Body
        self.shape = pymunk.Shape


class GameCollisionObject(GameObject):
    '''
    带碰撞的GameObject
    '''
    def __init__(self):
        self._collision_status: int
        self.image: pygame.Surface
        
        # 首次把状态设为 0
        self.collision_status = 0

    @property
    def collision_status(self):
        return self._collision_status
    
    @collision_status.setter
    def collision_status(self, v: int):
        self._collision_status = v
        self.image = self.load_img()

    def load_img(self) -> pygame.Surface:
        raise NotImplementedError("You need define the load_img() method")

    def collision(self, ke: float):
        pass

class GameObstacleObject(GameCollisionObject):
    def __init__(self):
        super().__init__()

class GameBirdObject(GameCollisionObject):
    def __init__(self):
        super().__init__()

from .fixed_line import FixedLineObject
from .fixed_poly import FixedPolyObject
from .obstacle_rect import ObstacleRectObject
from .orange_bird import OrangeBirdObject