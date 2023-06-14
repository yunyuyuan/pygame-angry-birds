from typing import Callable, List, TYPE_CHECKING, Optional

from src import Game
from src.components.side_panel import SidePanel
from src.game.editor_panel import StaffPanel
from src.game.game_panel import GamePanel
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject

import pygame
import pymunk

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils.enums import ButtonImgMap
from ..utils.surface import PageSurface


class GamePage(PageSurface):
    def __init__(self, editing=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editing = editing
        
        '''
        gaming
        '''
        self.pause_btn = Button(pos=(250, 150), img=ButtonImgMap.pause, visible=not self.editing, on_click=self.pause_game)
        self.reset_btn = Button(pos=(450, 150), img=ButtonImgMap.reset, visible=not self.editing)

        # 侧边栏
        self.left_board = SidePanel(width=300, right=True, visible=not self.editing)
        self.left_board_bg = RectSurface(size=(0, 0), pos=(0, 0), color=pygame.Color(0, 0, 0))
        self.resume_btn = Button(pos=(50, 50), img=ButtonImgMap.resume)
        self.left_board.add_children([self.left_board_bg, self.resume_btn])
        
        '''
        editing
        '''
        # 添加物料
        self.staff_btn = Button(pos=(5, 5), img=ButtonImgMap.my_materials, init_scale=0.6, visible=self.editing, on_click=self.toggle_staffs_panel)
        # 切换预览模式
        self.preview_btn = Button(pos=(305, 5), img=ButtonImgMap.my_preview, init_scale=0.6, visible=self.editing, on_click=self.toggle_preview)        
        # 物品栏
        self.staffs_panel = StaffPanel(start_place=self.start_place)
        
        '''
        common
        '''
        self.game_panel = GamePanel(end_place=self.end_place)

        self.add_children([self.game_panel, 
                           self.staff_btn, self.preview_btn, self.staffs_panel,
                           self.pause_btn, self.reset_btn, self.left_board])

    def common_pause_resume(self):
        '''
        通用。暂停/继续
        '''
        pass

    def common_move_camera(self):
        '''
        通用。移动视角
        '''
        pass

    def common_scale_camera(self):
        '''
        通用。放大缩小
        '''
        pass
    
    '''
    gaming methods
    --------------
    '''
    
    def pause_game(self, event: pygame.event.Event):
        self.left_board.toggle()    
    '''
    --------------
    '''
    
    '''
    editing methods
    --------------
    '''   
    def toggle_staffs_panel(self, _):
        self.staffs_panel.visible = not self.staffs_panel.visible
    
    def toggle_preview(self, _):
        self.game_panel.toggle_pause(True)
    
    def start_place(self, item):
        self.game_panel.start_place(item)
        self.staff_btn.visible = False
        self.preview_btn.visible = False
        self.staffs_panel.visible = False

    def end_place(self):
        self.staff_btn.visible = True
        self.preview_btn.visible = True
        self.staffs_panel.visible = True
    
    '''
    --------------
    '''
    
    def draw(self):
        self.game_panel.pymunk_step()
        self.surface.fill("#13b974")
        return super().draw()
