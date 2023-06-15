from copy import deepcopy
import json
import math
from typing import Callable, List, Optional, Tuple, Union

import pygame
import pymunk
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
    def __init__(self, end_place: Callable, end_delete: Callable, *args, **kwargs):
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0.0, -900.0)
        # 读取level
        self.config_path = get_asset_path("levels", '1.json')
        with open(self.config_path) as fp:
            self.config = json.load(fp)
        super().__init__(
            size=(self.config['geometry']['width'], (Game.geometry[1]-GamePanel.Bottom)*(self.config['geometry']['width']/Game.geometry[0])), 
            *args, **kwargs
        )
        # 地面
        ground_line = pymunk.Segment(self.space.static_body, (0,0), (self.config['geometry']['width'],0), 0.0)
        ground_line.friction = 0.5
        self.space.add(ground_line)
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
        # 正在移除
        self.deleting = False
        self.end_delete = end_delete
        
        '''
        common
        '''
        self.moving_start: Vector
        # 正在移动屏幕
        self.screen_moving = False
        # 正在拖拽小鸟
        self.bird_moving = False

        self.paused = True
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
            space=self.space,
            type=type,
            angle=angle,
            pos=pos,
        )])
    
    def del_obstacle(self, obstacle: GameObstacleObject):
        obstacle.remove_from_space()
        self.remove_child(obstacle)

    def add_fixed(self):
        pass

    def add_enemy(self):
        pass

    def toggle_pause(self, reset = False):
        self.paused = not self.paused
        if reset:
            # 重置
            for obstacle in self.obstacles:
                obstacle.reload()
                self.space.reindex_shapes_for_body(obstacle.body)
    
    def pymunk_step(self):
        if self.paused:
            self.space.step(0)
        else:
            self.space.step(1.0/Game.fps)
    
    @property
    def obstacles(self):
        return [x for x in self.children if isinstance(x, GameObstacleObject)]

    '''
    editing methods
    --------------
    '''   
    def start_place(self, item: ObstacleTypes):
        self.placing_item = item
        pygame.mouse.set_visible(False)

    def start_delete(self):
        self.deleting = not self.deleting
    
    def draw_preview(self):
        if self.placing_item:
            rotated_surface = pygame.transform.rotate(self.placing_item.surfaces[0], math.degrees(self.placing_angle))
            offset = pymunk.Vec2d(*rotated_surface.get_size()) / 2
            self.surface.blit(rotated_surface, self.relative_mouse - offset)

    '''
    --------------
    '''

    def mouse_event(self, event: pygame.event.Event) -> bool:
        pos = (self.relative_mouse[0], self.size[1] - self.relative_mouse[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.placing_item:
                # 放置
                if event.button == pygame.BUTTON_LEFT:
                    self.add_obstacle(
                        type=self.placing_item.name,
                        angle=self.placing_angle,
                        pos=pos
                    )
                    pygame.mouse.set_visible(True)
                    self.placing_angle = 0
                    self.placing_item = None
                    self.end_place()
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.placing_angle += 0.03
                elif event.button == pygame.BUTTON_WHEELUP:
                    self.placing_angle -= 0.03
            elif self.deleting:
                # 删除
                if event.button == pygame.BUTTON_LEFT:
                    for obstacle in self.obstacles:
                        if obstacle.check_mouse_inside(pos):
                            self.del_obstacle(obstacle)
                            self.deleting = False
                            self.end_delete()
                            break
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
            elif self.deleting:
                for obstacle in self.obstacles:
                    if obstacle.check_mouse_inside(pos):
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            # 发射!
            # 取消移动屏幕
            self.screen_moving = False
        return True

    def keyboard_event(self, event: pygame.event.Event) -> bool:
        if event.key == pygame.K_ESCAPE:
            if self.placing_item:
                pygame.mouse.set_visible(True)
                self.placing_item = None
                self.end_place()
                self.write_config()
            elif self.deleting:
                self.deleting = False
                self.end_delete()
                self.write_config()
        return False
    
    def write_config(self):
        with open(self.config_path, 'w') as fp:
            new_config = deepcopy(self.config)
            new_config['obstacles'] = list(map(lambda obstacle: {
                "type": obstacle.collision_type.name,
                "angle": obstacle.angle,
                "pos": obstacle.pos
            }, self.obstacles))
            json.dump(new_config, fp, indent=2)

    def draw(self):
        self.surface.fill((0, 0, 0, 0))
        return super().draw(after_draw_children=self.draw_preview)
