from copy import deepcopy
import json
from typing import Callable, List, Optional, Tuple, Union

import pygame
from src import Game
from src.components.rect import RectSurface
from src.game.objects import GameObstacleObject
from src.utils import get_asset_path
from src.utils.enums import ObstacleTypes
from src.utils.surface import ContainerSurface
from src.utils.vector import Vector


class GamePanel(ContainerSurface):
    Bottom = 100
    '''
    编辑/游戏界面通用
    '''
    def __init__(self, end_place: Callable, *args, **kwargs):
        # 读取level
        self.config_path = get_asset_path("levels", '1.json')
        with open(self.config_path) as fp:
            self.config = json.load(fp)
        super().__init__(
            size=(self.config['geometry']['width'], (Game.geometry[1]-GamePanel.Bottom)*(self.config['geometry']['width']/Game.geometry[0])), 
            *args, **kwargs
        )
        # 背景
        self.bg = RectSurface(size=(0, 0), pos=(0, 0), color=pygame.Color(180, 120, 160))
        self.add_children([self.bg])
        # 放置obstacles
        for obstacle in self.config["obstacles"]:
            self.add_obstacle(obstacle['type'], obstacle['angle'], obstacle['pos'])
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
        self.moving_start: Vector
        # 正在移动屏幕
        self.screen_moving = False
        # 正在拖拽小鸟
        self.bird_moving = False

        self.paused = False
        self.translate_x = 0
        self.translate_y = 0
        self.scale = self.config['geometry']['initial-scale']
        
    
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, v: float):
        self._scale = v
        # 重新计算pos_y
        self.pos = [self.pos[0], (Game.geometry[1]-GamePanel.Bottom)-self.scale*self.size[1]]
    
    def add_obstacle(self, type, angle, pos):
        self.add_children([GameObstacleObject(
            type=type,
            angle=angle,
            pos=pos,
        )])
    
    def del_obstacle(self):
        pass

    def add_fixed(self):
        pass

    def add_enemy(self):
        pass

    '''
    editing methods
    --------------
    '''   
    def start_place(self, item: ObstacleTypes):
        self.placing_item = item
        pygame.mouse.set_visible(False)
    
    def draw_preview(self):
        if self.placing_item:
            self.surface.blit(pygame.transform.rotate(self.placing_item.surfaces[0], self.placing_angle), (self.relative_mouse, self.placing_item.surfaces[0].get_size()))

    '''
    --------------
    '''

    def mouse_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 放置
            if self.placing_item:
                if event.button == pygame.BUTTON_LEFT:
                    self.add_obstacle(
                        type=self.placing_item.name,
                        angle=self.placing_angle,
                        pos=(self.relative_mouse[0], self.size[1] - self.relative_mouse[1])
                    )
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
                    self.scale = max(self.config['geometry']['min-scale'], self.scale - 0.1)
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.scale = min(self.scale + 0.1, 1)
        elif event.type == pygame.MOUSEMOTION:
            if self.screen_moving:
                new_pos = self.pos + event.rel
                self.pos = [0 if new_pos[0] >= 0 else (Game.geometry[0]-self.size[0]*self.scale if new_pos[0] <= Game.geometry[0]-self.size[0]*self.scale else new_pos[0]), self.pos[1]]
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
            with open(self.config_path, 'w') as fp:
                new_config = deepcopy(self.config)
                new_config['obstacles'] = list(map(lambda child: {
                    "type": child.collision_type.name,
                    "angle": child.angle,
                    "pos": child.pos
                }, [x for x in self.children if isinstance(x, GameObstacleObject)]))
                json.dump(new_config, fp, indent=2)
        return False

    def draw(self):
        self.surface.fill((0, 0, 0, 0))
        return super().draw(after_draw_children=self.draw_preview)
