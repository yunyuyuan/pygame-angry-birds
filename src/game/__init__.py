from typing import List, TYPE_CHECKING

from src import Game
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject

import pygame
import pymunk

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils.enums import ButtonImgMap
from ..surface import PageSurface, ContainerSurface

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
        
        self.pause_btn = Button(size=(100, 50), pos=(50, 50), img=ButtonImgMap.pause, parent=self)
        self.reset_btn = Button(size=(100, 50), pos=(300, 50), img=ButtonImgMap.reset, parent=self)

        self.left_board = ContainerSurface(size=(300, 600), pos=(500, 20), visible=True, parent=self)
        self.left_board_bg = RectSurface(size=(250, 600), pos=(0, 0), color=pygame.Color(255, 255, 255), parent=self.left_board)
        self.resume_btn = Button(size=(100, 50), pos=(50, 50), img=ButtonImgMap.resume, parent=self.left_board)
        self.left_board.children.extend([self.resume_btn, self.left_board_bg])
        
        self.children.extend([self.left_board, self.pause_btn, self.reset_btn])
    
    def draw(self):
        self.surface.fill("#13b3b9")
        return super().draw()
