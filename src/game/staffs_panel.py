from typing import Any, Callable, List, Literal, Optional, Tuple, Union

import pygame
from src.utils.animation import Animation
from src.utils.enums import MaterialShape, ObstacleTypes
from src.utils.surface import ContainerSurface, ElementSurface
from src.utils.vector import Vector


class StaffItem(ElementSurface):
    StaffSize = (190, 100)
    Gap = (6, 6)
    def __init__(self, index, *args, **kwargs):
        (width, height) = self.StaffSize
        super().__init__(size=self.StaffSize, pos=(self.Gap[0]*(index[0]+1)+index[0]*width, self.Gap[1]*(index[1]+1)+index[1]*height), *args, **kwargs)


class ObstacleItem(StaffItem):
    def __init__(
            self, 
            obstacle_type: ObstacleTypes,
            onclick: Callable[[ObstacleTypes], Any],
            index: Tuple[float, float],
            *args, **kwargs
        ):
        super().__init__(index=index, *args, **kwargs)
        self.obstacle_type = obstacle_type
        self.img_surface = pygame.transform.scale_by(self.obstacle_type.surfaces[0], 0.75)
        self.img_size = Vector(self.img_surface.get_size())
        self.img_pos = self.size / 2 - self.img_size / 2
        self.onclick = onclick
        self.hover = False
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.check_mouse_inside(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_inside:
                self.onclick(self.obstacle_type)
                return True
        self.hover = is_inside
        return False

    def draw(self):
        self.surface.fill((255, 255, 255, 100) if self.hover else (0, 0, 0, 0))
        self.surface.blit(self.img_surface, (self.img_pos, self.img_size))
        super().draw()


class FixedItem(StaffItem):
    def __init__(
            self,
            shape: MaterialShape,
            onclick: Callable[[MaterialShape], Any],
            index: Tuple[float, float],
            *args, **kwargs
        ):
        super().__init__(index=index, *args, **kwargs)
        self.shape = shape
        self.img_surface = pygame.Surface(Vector(self.StaffSize) * 0.75)
        self.img_size = Vector(self.img_surface.get_size())
        self.img_pos = self.size / 2 - self.img_size / 2
        self.onclick = onclick
        self.hover = False
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.check_mouse_inside(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_inside:
                self.onclick(self.shape)
                return True
        self.hover = is_inside
        return False
    
    def draw(self):
        self.surface.fill((255, 255, 255, 100) if self.hover else (0, 0, 0, 0))
        # self.surface.blit(self.img_surface, (self.img_pos, self.img_size))
        if self.shape == MaterialShape.box:
            pygame.draw.rect(self.surface, (0, 0, 0), (self.img_pos, self.img_size), width=1)
        elif self.shape == MaterialShape.triangle:
            pygame.draw.polygon(self.surface, (0, 0, 0), [self.img_pos, self.img_pos+self.img_size,self.img_pos+(0, self.img_size[1])], width=1)
        super().draw()



class StaffsPanel(ContainerSurface):
    Column = 5
    def __init__(self, start_place: Callable[[Union[ObstacleTypes, MaterialShape]], Any]):
        super().__init__(size=(StaffItem.Gap[0]+self.Column*(StaffItem.Gap[0]+StaffItem.StaffSize[0]), -120), pos=(5, 5), pos_bottom=True, visible=False)
        self.start_place = start_place
        self.items: List[StaffItem] = list(map(
            lambda item: ObstacleItem(obstacle_type=item[1][1], onclick=self.item_click, index=StaffsPanel.calc_index(item[0])), 
            enumerate(list(ObstacleTypes.__members__.items()))
        ))
        self.items.extend([
            FixedItem(MaterialShape.box, onclick=self.item_click, index=StaffsPanel.calc_index(len(self.items))),
            FixedItem(MaterialShape.triangle, onclick=self.item_click, index=StaffsPanel.calc_index(len(self.items)+1)),
        ])

        self.add_children([*self.items])
    
    @staticmethod
    def calc_index(index: int):
        return (index%StaffsPanel.Column, index//StaffsPanel.Column)
    
    def change_page(self):
        pass
    
    def item_click(self, item):
        self.start_place(item)
    
    def draw(self):
        self.surface.fill((0, 0, 0, 100))
        return super().draw()
