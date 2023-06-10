import pymunk
import pygame

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject
    from src.utils.surface import PageSurface

fps = 60.0

# 单例静态class
class Game(object):
    running = True
    debug = True
    fps = fps
    fps_frame_sec = int(1000/fps)

    geometry = (1200, 720)
    screen: pygame.Surface
    active_page: "PageSurface"

    fps_event = pygame.USEREVENT + 1
    
    @staticmethod
    def pygame_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.running = False
            elif event.type == Game.fps_event:
                Game.active_page.animation_event()
            elif event.type == pygame.KEYDOWN:
                Game.active_page.keyboard_event(event)
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                Game.active_page.mouse_event(event)
