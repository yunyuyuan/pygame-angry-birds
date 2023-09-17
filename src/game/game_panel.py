from copy import deepcopy
import json
import math
from typing import Callable, List, Optional, Tuple, Union, TYPE_CHECKING

import pygame
import pymunk
from src import Game
from src.game.bg_panel import BgPanel
from src.game.objects import GameBirdObject, GameFixedObject, GameObstacleObject
from src.utils import calculate_distance, calculate_intersection, get_asset_path, pygame_to_pymunk
from src.utils.enums import BirdTypes, MaterialShape, MaterialType, ObstacleTypes, SpecialItems
from src.utils.surface import BaseSurface, ContainerSurface

if TYPE_CHECKING:
    from src.game import GamePage

class GamePanel(ContainerSurface['GamePage']):
    PlayingBottom = 100
    SlingshotRadius = 120
    MaxLaunchDistance = SlingshotRadius**2
    MinLaunchDistance = MaxLaunchDistance/4
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
        self.birds: List[str] = self.config['resources']['birds']
        self.min_scale = Game.geometry[0]/self.config['geometry']['width']
        self.bottom = self.config['geometry']['bottom']
        super().__init__(
            size=(self.config['geometry']['width'], Game.geometry[1]/self.min_scale), 
            *args, **kwargs
        )
        '''
        物理引擎
        '''
        # 地面
        ground_line = pymunk.Poly(self.space.static_body, [(0,self.bottom), (self.config['geometry']['width'],self.bottom), (0,0), (self.config['geometry']['width'],0)], None, 0.0)
        ground_line.friction = 0.5
        self.space.add(ground_line)
        # 初始化放置obstacles
        for obstacle in self.config["obstacles"]:
            self.add_obstacle(type=obstacle['type'], angle=obstacle['angle'], pos=obstacle['pos'])
        # 初始化放置fixed
        for fixed in self.config["fixed"]:
            self.add_fixed(type=fixed['type'], size=fixed['size'], angle=fixed['angle'], pos=fixed['pos'])
        '''
        UI
        '''
        # 弹弓位置
        self.slingshot = pygame.Vector2(self.config['resources']['slingshot'])
        self.bird_launch_pos: pygame.Vector2 = pygame.Vector2([0, 0])
        # 背景
        self.bg_panel = BgPanel(max_width=self.config['geometry']['width'], level=4, pos_y=self.surface.get_height()-self.bottom)
        '''
        gaming
        '''
        self.current_fly_bird: Optional[GameBirdObject] = None

        '''
        editing
        '''
        # 正在放置
        self.placing_item: Union[ObstacleTypes, MaterialShape, None] = None
        self.placing_angle: float
        self.placing_size: List[int] # fixed的大小
        self.end_place = end_place
        # 正在移除
        self.deleting = False
        self.end_delete = end_delete
        
        '''
        common
        '''
        self.moving_start: pygame.Vector2
        # 正在移动屏幕
        self.screen_moving = False
        # 正在拖拽小鸟
        self.slingshot_moving = False

        self.paused = True
        self.scale = self.config['geometry']['initial-scale']
        # scale动画的方向
        self.scale_target = 0
        
    @property
    def editing(self):
        return self.parent.editing
    
    @property
    def playing(self):
        return not self.editing

    @property
    def candidate_bird(self):
        return BirdTypes[self.birds[0]]
    
    def add_obstacle(self, pos, angle, type):
        self.add_children([GameObstacleObject(
            space=self.space,
            pos=pos,
            type=type,
            angle=angle
        )])
    
    def del_obstacle(self, obstacle: GameObstacleObject):
        obstacle.remove_from_space()
        self.remove_child(obstacle)

    def add_fixed(self, pos, angle, type, size):
        self.add_children([GameFixedObject(
            space=self.space,
            size=size,
            type=type,
            angle=angle,
            pos=pos,
        )])

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
            pass
        else:
            self.space.step(1.0/Game.fps)
    
    def animation_event(self):
        old_scale = self.scale
        if self.scale_target != 0:
            interval = self.scale_target / 5
            step = interval / 10
            if self.scale_target > 0:
                self.scale_target = max(self.scale_target - interval, 0)
                self.scale = max(self.min_scale, self.scale - step)
            elif self.scale_target < 0:
                self.scale_target = min(self.scale_target - interval, 0)
                self.scale = min(self.scale - step, self.config['geometry']['max-scale'])
            if self.scale != old_scale:
                # 中心缩放，理论上应该封装在BaseSurface里的 @scale.setter
                half_geometry = pygame.Vector2((Game.geometry[0], Game.geometry[1]-self.bottom))/2
                new_pos = half_geometry - (half_geometry - self.pos)*self.scale/old_scale
                self.set_valid_pos(new_pos)
        super().animation_event()
    
    # 处理pos的边界情况
    def set_valid_pos(self, new_pos: pygame.Vector2):
        min_x = Game.geometry.x-self.size.x*self.scale
        min_y = Game.geometry.y-self.size.y*self.scale
        self.pos = (
            0 if new_pos.x >= 0 else (min_x if new_pos.x <= min_x else new_pos.x),
            (0 if new_pos.y >= 0 else (min_y if new_pos.y <= min_y else new_pos.y)) 
                if self.editing 
                else min(0, min_y+self.bottom*self.scale-self.PlayingBottom),
        )
    
    @property
    def obstacles(self):
        return [x for x in self.children if isinstance(x, GameObstacleObject)]

    @property
    def fixed(self):
        return [x for x in self.children if isinstance(x, GameFixedObject)]
    
    
    '''
    gaming methods
    --------------
    '''   
    def collision_handler(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data):
        # if material == MaterialType.stone:
        for shape in [x for x in arbiter.shapes if x.collision_type == MaterialType.bird.value]:
            print(shape)

    '''
    editing methods
    --------------
    '''   
    def start_place(self, item: Union[ObstacleTypes, MaterialShape]):
        self.placing_item = item
        self.placing_angle = 0
        self.placing_size = [50, 50]
        pygame.mouse.set_visible(False)

    def start_delete(self):
        self.deleting = not self.deleting
    
    def after_draw_children(self):
        # preview
        if self.placing_item:
            angle = math.degrees(self.placing_angle)
            if isinstance(self.placing_item, ObstacleTypes):
                surface = self.placing_item.surfaces[0]
            else:
                img_size = self.placing_size
                surface = pygame.Surface(img_size, flags=pygame.SRCALPHA)
                if self.placing_item == MaterialShape.box:
                    pygame.draw.rect(surface, (0, 0, 0), ((0, 0), img_size), width=1)
                else:
                    pygame.draw.polygon(surface, (0, 0, 0), [(0,0),(0, img_size[1]-1), (img_size[0],img_size[1]-1),(0,0)], width=1)

            rotated_surface = pygame.transform.rotate(surface, angle)
            offset = pymunk.Vec2d(*rotated_surface.get_size()) / 2
            self.surface.blit(rotated_surface, self.relative_mouse - offset)
        # slingshot
        slingshot = self.relative_mouse if (self.editing and self.slingshot_moving) else self.slingshot
        # back
        self.surface.blit(SpecialItems.SlingShotBack.value, slingshot+(-8, -30))
        if self.playing:
            # backline
            # bird
            self.surface.blit(self.candidate_bird.surfaces[0], slingshot+self.bird_launch_pos-pygame.Vector2(self.candidate_bird.size)/2)
            # frontlint
            # 垫圈
            # front
        self.surface.blit(SpecialItems.SlingShotFront.value, slingshot+(-36, -32))
        if Game.debug:
            pygame.draw.circle(self.surface, (255, 0, 0), slingshot, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), slingshot, self.SlingshotRadius, width=1)
        # 背景
        self.bg_panel.after_game_draw(self.surface)

    '''
    --------------
    '''

    def mouse_event(self, event: pygame.event.Event) -> bool:
        pos = (self.relative_mouse[0], self.size[1] - self.relative_mouse[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.placing_item:
                if event.button == pygame.BUTTON_LEFT:
                    # 放置
                    if isinstance(self.placing_item, ObstacleTypes):
                        # 放置障碍物
                        self.add_obstacle(
                            pos=pos,
                            angle=self.placing_angle,
                            type=self.placing_item.name
                        )
                    else:
                        # 放置fixed
                        self.add_fixed(
                            size=tuple(self.placing_size),
                            angle=self.placing_angle,
                            type=self.placing_item,
                            pos=pos
                        )
                    pygame.mouse.set_visible(True)
                    self.placing_item = None
                    self.end_place()
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    if isinstance(self.placing_item, MaterialShape) and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # 调整fixed长宽
                        self.placing_size[0 if pygame.key.get_mods() & pygame.KMOD_LCTRL else 1] -= 10
                    else:
                        # 旋转
                        self.placing_angle += 0.03
                elif event.button == pygame.BUTTON_WHEELUP:
                    if isinstance(self.placing_item, MaterialShape) and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # 调整fixed长宽
                        self.placing_size[0 if pygame.key.get_mods() & pygame.KMOD_LCTRL else 1] += 10
                    else:
                        # 旋转
                        self.placing_angle -= 0.03
            elif self.deleting:
                # 删除
                if event.button == pygame.BUTTON_LEFT:
                    for item in [*self.obstacles, *self.fixed]:
                        if item.check_mouse_inside(pos):
                            self.del_obstacle(item)
                            self.deleting = False
                            self.end_delete()
                            break
            else:
            # 编辑/游戏模式下通用
                if event.button == pygame.BUTTON_LEFT:
                    if calculate_distance(self.relative_mouse, self.slingshot) <= self.MaxLaunchDistance:
                        # 拖拽弹弓
                        self.slingshot_moving = True
                        if self.playing:
                            self.bird_launch_pos = self.relative_mouse - self.slingshot
                    # 释放技能
                    else:
                        # 移动屏幕
                        self.screen_moving = True
                # 放大/缩小
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    if self.scale_target < 0:
                        self.scale_target = 0
                    self.scale_target = min(3, self.scale_target + 0.5)
                elif event.button == pygame.BUTTON_WHEELUP:
                    if self.scale_target > 0:
                        self.scale_target = 0
                    self.scale_target = max(-3, self.scale_target - 0.5)
        elif event.type == pygame.MOUSEMOTION:
            if self.deleting:
                # 删除
                for item in [*self.obstacles, *self.fixed]:
                    if item.check_mouse_inside(pos):
                        break
            elif self.screen_moving:
                # 拖动屏幕
                new_pos = self.pos + (event.rel[0], event.rel[1] if self.editing else 0)
                self.set_valid_pos(new_pos)
            elif self.slingshot_moving:
                intersection = calculate_intersection(self.slingshot, self.relative_mouse, self.SlingshotRadius)
                # 弹弓移动
                self.bird_launch_pos = (intersection if intersection else self.relative_mouse) - self.slingshot
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.slingshot_moving:
                self.slingshot_moving = False
                if self.editing:
                    # 弹弓移动松开
                    self.slingshot = self.relative_mouse
                else:
                    # 发射鸟
                    distance = calculate_distance(self.bird_launch_pos, pygame.Vector2((0, 0)))
                    if distance >= self.MinLaunchDistance:
                        self.current_fly_bird = GameBirdObject(
                            space=self.space,
                            pos=pos,
                            bird_type=self.candidate_bird.name
                        )
                        self.add_children([self.current_fly_bird])
                        self.current_fly_bird.launch(pygame_to_pymunk(self.slingshot+self.bird_launch_pos, self.size[1]), self.bird_launch_pos)
            elif self.screen_moving:
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
                "pos": tuple(obstacle.pos)
            }, self.obstacles))
            new_config['fixed'] = list(map(lambda fixed: {
                "type": fixed.type.name,
                "angle": fixed.angle,
                "size": tuple(fixed.size),
                "pos": tuple(fixed.pos)
            }, self.fixed))
            new_config["resources"]["slingshot"] = list(self.slingshot)
            json.dump(new_config, fp, indent=2)

    def draw(self):
        self.surface.fill((180, 120, 160))
        self.bg_panel.before_game_draw(self.surface, self.pos.x)
        self.pymunk_step()
        return super().draw(after_draw_children=self.after_draw_children)
