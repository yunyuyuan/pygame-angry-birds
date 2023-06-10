

from typing import Any, Callable, List

import pygame
from src.components.rect import RectSurface
from src.utils.animation import Animation
from src.utils.enums import ObstacleTypes
from src.utils.surface import ContainerSurface, ElementSurface
from src.utils.vector import Vector


class StaffItem(ElementSurface, Animation):
    def __init__(
            self, 
            obstacle_type: ObstacleTypes,
            onclick: Callable[[ObstacleTypes], Any],
            *args, **kwargs
        ):
        super().__init__((191, 100), (6, 6), *args, **kwargs)
        self.obstacle_type = obstacle_type
        self.img_surface = self.obstacle_type.surfaces[0]
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
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, (255, 255, 255, 100) if self.hover else (0, 0, 0, 0), ((0, 0), self.size))
        self.surface.blit(self.img_surface, (self.img_pos, self.img_size))
        super().draw()


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
        self.surface.fill((0, 0, 0, 0))
        return super().draw()

