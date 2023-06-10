from typing import Callable, List, TYPE_CHECKING, Optional

from src import Game
from src.components.side_panel import SidePanel
from src.game.editor_panel import StaffPanel
from src.utils.types import ObstacleProp
from src.utils.vector import Vector
from ..utils.surface import ContainerSurface
if TYPE_CHECKING:
    from src.game.objects import GameBirdObject, GameObstacleObject

import pygame
import pymunk

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils.enums import ButtonImgMap, ObstacleTypes
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
        self.preview_btn = Button(pos=(305, 5), img=ButtonImgMap.my_preview, init_scale=0.6, visible=self.editing)        
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
    def toggle_staffs_panel(self, event: pygame.event.Event):
        self.staffs_panel.visible = not self.staffs_panel.visible
    
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
        self.surface.fill("#13b974")
        return super().draw()


class GamePanel(ContainerSurface):
    '''
    编辑/游戏界面通用
    '''
    def __init__(self, end_place: Callable, *args, **kwargs):
        super().__init__(size=(2400, 720), *args, **kwargs)
        '''
        gaming
        '''

        '''
        editing
        '''
        # 正在放置
        self.placing_item: Optional[ObstacleTypes] = None
        self.placing_angle: float = 0
        self.end_place = end_place
        
        '''
        common
        '''
        self.bg = RectSurface(size=(0, -100), pos=(0, 0), color=pygame.Color(180, 120, 160))

        self.obstacle_items: List[ObstacleProp] = []

        self.moving_start: Vector
        # 正在移动屏幕
        self.screen_moving = False
        # 正在拖拽小鸟
        self.bird_moving = False

        self.paused = False
        self.translate_x = 0
        self.translate_y = 0
        self.scale = 1
        
        self.add_children([self.bg])
    
    def common_toggle_pause(self):
        self.paused = not self.paused

    '''
    editing methods
    --------------
    '''   
    def start_place(self, item: ObstacleTypes):
        self.placing_item = item
        pygame.mouse.set_visible(False)
    
    def draw_preview(self):
        # place preview
        if self.placing_item:
            self.surface.blit(pygame.transform.rotate(self.placing_item.surfaces[0], self.placing_angle), (pygame.mouse.get_pos(), self.placing_item.surfaces[0].get_size()))

    '''
    --------------
    '''  

    def mouse_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 放置
            if self.placing_item:
                if event.button == pygame.BUTTON_LEFT:
                    self.obstacle_items.append({
                        "pos": Vector(pygame.mouse.get_pos()),
                        "angle": self.placing_angle,
                        "type": self.placing_item
                    })
                    pygame.mouse.set_visible(True)
                    self.placing_angle = 0
                    self.placing_item = None
                    self.end_place()
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.placing_angle += 1
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.placing_angle -= 1
            else:
                if event.button == pygame.BUTTON_LEFT:
                    # 拖拽小鸟
                    # 释放技能
                    # 移动屏幕
                    self.screen_moving = True
                # 放大/缩小
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.scale = max(0.1, self.scale - 0.1)
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.scale += 0.1
        elif event.type == pygame.MOUSEMOTION:
            if self.screen_moving:
                new_pos = self.pos + event.rel
                self.pos = [new_pos[0], self.pos[1]]
        elif event.type == pygame.MOUSEBUTTONUP:
            # 发射!
            # 取消移动屏幕
            self.screen_moving = False
        return True

    def keyboard_event(self, event: pygame.event.Event) -> bool:
        if self.placing_item and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
            self.placing_item = None
            self.end_place()
        return False

    def draw(self):
        self.surface.fill((0, 0, 0, 0))
        # placed items
        for item in self.obstacle_items:
            self.surface.blit(pygame.transform.rotate(item['type'].surfaces[0], item["angle"]), (item['pos']*self.scale, item['type'].surfaces[0].get_size()))
        return super().draw(afterChildrenDraw=self.draw_preview)
