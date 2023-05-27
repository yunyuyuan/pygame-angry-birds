from typing import Any, Callable, List, Optional
import pygame
import pymunk
from src import Game

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils import get_asset_path
from src.utils.animation import Animation
from src.utils.enums import ButtonImgMap, ObstacleTypes
from src.utils.surface import ContainerSurface, ElementSurface, PageSurface
from src.utils.types import ObstacleProp
from src.utils.vector import Vector


class EditorPage(PageSurface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 添加物料
        self.staff_btn = Button(pos=(5, 5), img=ButtonImgMap.my_materials, init_scale=0.6, on_click=self.toggle_staffs_panel)
        # 移动物料
        self.move_btn = Button(pos=(105, 5), img=ButtonImgMap.my_move, init_scale=0.6)
        # 旋转物料
        self.rotate_btn = Button(pos=(205, 5), img=ButtonImgMap.my_rotate, init_scale=0.6)
        # 切换预览模式
        self.preview_btn = Button(pos=(305, 5), img=ButtonImgMap.my_preview, init_scale=0.6)
        
        # staffs
        self.staffs_panel = StaffPanel(start_place=self.start_place)
        
        # game edit
        self.game_panel = GamePanel(end_place=self.end_place)
        
        self.add_children([self.game_panel, self.staff_btn, self.move_btn, self.rotate_btn, self.preview_btn, self.staffs_panel])
    
    def toggle_staffs_panel(self, event: pygame.event.Event):
        self.staffs_panel.visible = not self.staffs_panel.visible
    
    def start_place(self, item):
        self.game_panel.start_place(item)
        self.staff_btn.visible = False
        self.move_btn.visible = False
        self.rotate_btn.visible = False
        self.preview_btn.visible = False
        self.staffs_panel.visible = False

    def end_place(self):
        self.staff_btn.visible = True
        self.move_btn.visible = True
        self.rotate_btn.visible = True
        self.preview_btn.visible = True
        self.staffs_panel.visible = True
    
    def draw(self):
        self.surface.fill("#13b974")
        return super().draw()


class StaffItem(ElementSurface, Animation):
    def __init__(
            self, 
            obstacle_type: ObstacleTypes,
            onclick: Callable[[ObstacleTypes], Any],
            *args, **kwargs
        ):
        super().__init__((191, 100), (6, 6), *args, **kwargs)
        self.obstacle_type = obstacle_type
        self.img_surface = self.obstacle_type.value[0]
        self.img_size = Vector(self.img_surface.get_size())
        self.img_pos = self.size / 2 - self.img_size / 2
        self.onclick = onclick
        self.hover = False
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.is_mouse_inside(event)
        if event.type == pygame.MOUSEMOTION:
            if is_inside:
                # button 放大动画
                self.animation_state = 1
            else:
                # button 缩小动画
                self.animation_state = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if is_inside:
                self.onclick(self.obstacle_type)
        self.hover = is_inside
        return False
    
    def animation_step(self, progress):
        pass
    
    def draw(self):
        self.parent_surface.blit(self.img_surface, (self.img_pos, self.img_size))
        pygame.draw.rect(self.parent_surface, pygame.Color(255, 0, 0) if self.hover else pygame.Color(255, 255, 255), (self.pos, self.size), width=1, border_radius=10)


class StaffPanel(ContainerSurface):
    def __init__(self, start_place: Callable[[ObstacleTypes], Any]):
        super().__init__(size=(400, -120), pos=(5, 5), pos_bottom=True, visible=False)
        self.start_place = start_place
        self.bg = RectSurface(size=(0, 0), pos=(0, 0), color=pygame.Color(0, 0, 0, 100))
        self.items: List[StaffItem] = [StaffItem(obstacle_type=ObstacleTypes.g_w4_h1, onclick=self.item_click)]

        self.add_children([self.bg, *self.items])
    
    def change_page(self):
        pass
    
    def item_click(self, item: ObstacleTypes):
        self.start_place(item)
    
    def draw(self):
        return super().draw()



class GamePanel(ContainerSurface):
    def __init__(self, end_place: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placed_items: List[ObstacleProp] = []
        # 正在放置
        self.placing_item: Optional[ObstacleTypes] = None
        self.end_place = end_place
        
    def start_place(self, item: ObstacleTypes):
        self.placing_item = item
        pygame.mouse.set_visible(False)
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and self.placing_item:
            self.placed_items.append({
                "pos": Vector(pygame.mouse.get_pos()),
                "angle": 0.0,
                "type": self.placing_item
            })
            pygame.mouse.set_visible(True)
            self.placing_item = None
            self.end_place()
        return True

    def keyboard_event(self, event: pygame.event.Event) -> bool:
        if self.placing_item and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
            self.placing_item = None
            self.end_place()
        return False
    
    def draw(self):
        # place preview
        if self.placing_item:
            self.parent_surface.blit(self.placing_item.value[0], (pygame.mouse.get_pos(), self.placing_item.value[0].get_size()))
        # placed items
        for item in self.placed_items:
            self.parent_surface.blit(item['type'].value[0], (item['pos'], item['type'].value[0].get_size()))
        return super().draw()
    