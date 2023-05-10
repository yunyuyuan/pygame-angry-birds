import pymunk
import pygame

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject
    from src.surface import PageSurface


fps = 60.0

# 单例静态class
class Game(object):
    running = True

    screen: pygame.Surface
    active_page: PageSurface

    space: pymunk.Space

    launched_birds: List[GameBirdObject] = []
    obstacles: List[GameObstacleObject] = []
    
    @staticmethod
    def pygame_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.running = False
            elif event.type == pygame.KEYDOWN:
                Game.active_page.keyboard_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                Game.active_page.mouse_event(event)
