from typing import List, TYPE_CHECKING

from src import Game
from src.components.side_panel import SidePanel
from ..utils.surface import ContainerSurface
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject

import pygame
import pymunk

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils.enums import ButtonImgMap
from ..utils.surface import PageSurface

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
        
        self.pause_btn = Button(pos=(250, 150), img=ButtonImgMap.pause, on_click=self.pause_game)
        self.reset_btn = Button(pos=(450, 150), img=ButtonImgMap.reset)

        # 侧边栏
        self.left_board = SidePanel(width=300, right=True)
        self.left_board_bg = RectSurface(size=(0, 0), pos=(0, 0), color=pygame.Color(0, 0, 0))
        self.resume_btn = Button(pos=(50, 50), img=ButtonImgMap.resume)
        self.left_board.add_children([self.left_board_bg, self.resume_btn])
        
        self.add_children([self.pause_btn, self.reset_btn, self.left_board])
    
    def pause_game(self, event: pygame.event.Event):
        self.left_board.toggle()
    
    def draw(self):
        self.surface.fill("#13b3b9")
        return super().draw()
