from typing import Any, Callable, List, Literal, Optional, Tuple, Union

import pygame
from src.utils.animation import Animation
from src.utils.enums import CollisionTypes, MaterialShape, ObstacleTypes, PigTypes
from src.utils.surface import ContainerSurface, ElementSurface

class StaffItem(ElementSurface):
    StaffSize = (190, 100)
    Gap = (6, 6)
    def __init__(self, index, onclick, *args, **kwargs):
        self.img_surface: pygame.Surface
        self.hover: bool = False
        self.img_size: pygame.Vector2
        self.img_pos: pygame.Vector2
        self.onclick = onclick
        (width, height) = self.StaffSize
        super().__init__(
            size=self.StaffSize, 
            pos=(
                self.Gap[0]*(index[0]+1)+index[0]*width, 
                self.Gap[1]*(index[1]+1)+index[1]*height
            ), 
            *args, **kwargs
        )
    
    def init_image(self):
        self.img_size = pygame.Vector2(self.img_surface.get_size())
        self.img_pos = self.size / 2 - self.img_size / 2
    
    def draw_hover_bg(self):
        self.surface.fill((255, 255, 255, 50) if self.hover else (0, 0, 0, 0))


class CollisionItem(StaffItem):
    def __init__(
            self, 
            collision_type: CollisionTypes,
            onclick: Callable[[CollisionTypes], Any],
            index: Tuple[float, float],
            *args, **kwargs
        ):
        super().__init__(index=index, onclick=onclick, *args, **kwargs)
        self.collision_type = collision_type
        self.img_surface = pygame.transform.scale_by(self.collision_type.surfaces[0], 0.75)
        self.init_image()
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.check_mouse_inside(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_inside:
                self.onclick(self.collision_type)
                return True
        self.hover = is_inside
        return False

    def draw(self):
        self.draw_hover_bg()
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
        super().__init__(index=index, onclick=onclick, *args, **kwargs)
        self.shape = shape
        self.img_surface = pygame.Surface(pygame.Vector2(self.StaffSize) * 0.75)
        self.init_image()
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        is_inside = self.check_mouse_inside(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_inside:
                self.onclick(self.shape)
                return True
        self.hover = is_inside
        return False
    
    def draw(self):
        self.draw_hover_bg()
        # self.surface.blit(self.img_surface, (self.img_pos, self.img_size))
        if self.shape == MaterialShape.box:
            pygame.draw.rect(self.surface, (255, 255, 255), (self.img_pos, self.img_size), width=1)
        elif self.shape == MaterialShape.triangle:
            pygame.draw.polygon(self.surface, (255, 255, 255), [self.img_pos, self.img_pos+self.img_size,self.img_pos+(0, self.img_size[1])], width=1)
        super().draw()



class StaffsPanel(ContainerSurface):
    Column = 5
    def __init__(self, start_place: Callable[[Union[CollisionTypes, MaterialShape]], Any]):
        super().__init__(size=(StaffItem.Gap[0]+self.Column*(StaffItem.Gap[0]+StaffItem.StaffSize[0]), -120), pos=(5, 5), pos_bottom=True, visible=False)
        self.start_place = start_place
        self.items: List[StaffItem] = []
        self.items.extend(list(map(
            lambda item: CollisionItem(collision_type=item[1][1], onclick=self.item_click, index=self.calc_index(item[0])), 
            enumerate(list(ObstacleTypes.__members__.items()))
        )))
        self.items.extend(list(map(
            lambda item: CollisionItem(collision_type=item[1][1], onclick=self.item_click, index=self.calc_index(item[0])), 
            enumerate(list(PigTypes.__members__.items()))
        )))
        self.items.extend(list(map(
            lambda item: FixedItem(item[1], onclick=self.item_click, index=self.calc_index(item[0])), 
            enumerate([MaterialShape.box, MaterialShape.triangle])
        )))

        self.add_children([*self.items])

    def calc_index(self, index: int = 0):
        index = len(self.items) + index
        return (index%StaffsPanel.Column, index//StaffsPanel.Column)
    
    def change_page(self):
        pass
    
    def item_click(self, item):
        self.start_place(item)
    
    def draw(self):
        self.surface.fill((0, 0, 0, 230))
        return super().draw()
