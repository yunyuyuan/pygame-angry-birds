from typing import List, TYPE_CHECKING

from src import Game
from src.components.side_panel import SidePanel
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
        
        self.pause_btn = Button(pos=(550, 150), img=ButtonImgMap.pause, parent=self, on_click=self.pause_game)
        self.reset_btn = Button(pos=(750, 150), img=ButtonImgMap.reset, parent=self)

        # 侧边栏
        self.left_board = SidePanel(width=300, visible=True, parent=self)
        self.left_board_bg = RectSurface(size=(250, 600), pos=(0, 0), color=pygame.Color(0, 0, 0), parent=self.left_board)
        self.resume_btn = Button(pos=(50, 50), img=ButtonImgMap.resume, parent=self.left_board)
        self.left_board.children.extend([self.left_board_bg, self.resume_btn])
        
        self.children.extend([self.pause_btn, self.reset_btn, self.left_board])
    
    def pause_game(self, event: pygame.event.Event):
        self.left_board.toggle()
    
    def draw(self):
        self.surface.fill("#13b3b9")
        return super().draw()
