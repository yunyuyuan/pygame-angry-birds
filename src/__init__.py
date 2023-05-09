import pymunk
import pygame
import reactivex as rx

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject


fps = 60.0

# 单例静态class
class Game(object):
    event_bus: rx.Subject[int] = rx.Subject()
    running = True

    screen: pygame.Surface
    space: pymunk.Space

    launched_birds: List["GameBirdObject"] = []
    obstacles: List["GameObstacleObject"] = []
    
    @staticmethod
    def pygame_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.running = False
            else:
                Game.event_bus.on_next(event.type)