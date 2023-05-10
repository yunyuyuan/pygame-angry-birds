from enum import Enum

from src.utils.button import Button
from src.utils.enums import ButtonImgMap
from ..surface import PageSurface

# 加载游戏level的json配置
def load_json_config():
    pass

collision_types = {
    "bird": 1,
    "pig": 2,
    "obstacle": 3
}

bird_types = {
    "red": 1,
    "orange": 2,
    "blue": 3,
}

obstacle_rect_types = {
    "4x1": 1,
}

class GamePage(PageSurface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.pause_btn = Button(size=(100, 50), pos=(50, 50), img=ButtonImgMap.pause)
        
        self.children.extend([self.pause_btn])
