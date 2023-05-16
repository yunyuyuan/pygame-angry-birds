from enum import Enum

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject

import pygame
import pymunk

from src.utils.button import Button
from src.utils.rect import RectSurface
from src.utils.enums import ButtonImgMap
from ..surface import PageSurface

# 加载游戏level的json配置
def load_json_config():
    pass


class GameEngine():
    '''
    物理引擎相关
    '''
    def __init__(self) -> None:
        self.space: pymunk.Space
        self.launched_birds: List[GameBirdObject] = []
        self.obstacles: List[GameObstacleObject] = []


class GamePage(PageSurface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.pause_btn = Button(size=(100, 50), pos=(50, 50), img=ButtonImgMap.pause)
        self.reset_btn = Button(size=(100, 50), pos=(300, 50), img=ButtonImgMap.reset)
        self.left_board = RectSurface(size=(300, 720), pos=(0, 0), color=pygame.Color(255, 255, 255))
        self.left_board.visible = False
        
        self.children.extend([self.left_board, self.pause_btn, self.reset_btn])
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        if not super().mouse_event(event):
            pass
        return True
