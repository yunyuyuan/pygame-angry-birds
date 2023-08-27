from typing import Any, Callable, List, TYPE_CHECKING, Optional, Union

from src import Game
from src.components.side_panel import SidePanel
from src.game.staffs_panel import StaffsPanel
from src.game.game_panel import GamePanel
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject

import pygame
import pymunk

from src.components.button import Button
from src.utils.enums import ButtonTypes, MaterialShape, ObstacleTypes
from ..utils.surface import ChildType, PageSurface


class GamePage(PageSurface):
    def __init__(self, editing=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editing = editing
        
        '''
        gaming
        '''
        self.pause_btn = Button(pos=(5, 5), button_type=ButtonTypes.pause, init_scale=0.75, visible=not self.editing, on_click=self.pause_game)
        self.reset_btn = Button(pos=(95, 5), button_type=ButtonTypes.reset, init_scale=0.75, visible=not self.editing)

        # 侧边栏
        self.left_board = SidePanel(width=300, right=True, visible=not self.editing)
        self.resume_btn = Button(pos=(50, 50), button_type=ButtonTypes.resume)
        self.left_board.add_children([self.resume_btn])
        
        '''
        editing
        '''
        self.previewing = False
        # 添加物料
        self.staff_btn = Button(pos=(5, 5), button_type=ButtonTypes.my_materials, init_scale=0.6, visible=self.editing, on_click=self.toggle_staffs_panel)
        # 删除物料
        self.delete_btn = Button(pos=(125, 5), button_type=ButtonTypes.my_delete, init_scale=0.6, visible=self.editing, on_click=self.start_delete)        
        # 切换预览模式
        self.preview_btn = Button(pos=(245, 5), button_type=ButtonTypes.my_preview, init_scale=0.6, visible=self.editing, on_click=self.toggle_preview)        
        # 物品栏
        self.staffs_panel = StaffsPanel(start_place=self.start_place)
        
        '''
        common
        '''
        self.game_panel = GamePanel(end_place=self.end_place, end_delete=self.end_delete)

        self.add_children([self.game_panel, 
                           self.staff_btn, self.delete_btn, self.preview_btn, self.staffs_panel,
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
    def toggle_operating(self, b: bool, exclude: List[ChildType] = []):
        for item in [x for x in [
            self.staff_btn,
            self.staffs_panel,
            self.delete_btn,
            self.preview_btn,
        ] if x not in exclude]:
            item.visible = b

    def toggle_staffs_panel(self, _):
        self.staffs_panel.visible = not self.staffs_panel.visible

    def toggle_preview(self, _):
        self.game_panel.toggle_pause(True)
        self.previewing = not self.previewing
        self.toggle_operating(not self.previewing, [self.preview_btn])
    
    def start_place(self, item):
        self.game_panel.start_place(item)
        self.toggle_operating(False)

    def end_place(self):
        self.toggle_operating(True)

    def start_delete(self, _):
        self.game_panel.start_delete()
        self.toggle_operating(False)
    
    def end_delete(self):
        self.toggle_operating(True)
    '''
    --------------
    '''
    
    def draw(self):
        self.surface.fill("#13b974")
        return super().draw()
