import pygame
import pymunk

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils.enums import ButtonImgMap
from ..surface import PageSurface, ContainerSurface


class EditorPage(PageSurface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.staff_btn = Button(pos=(50, 50), img=ButtonImgMap.resume, on_click=self.open_staffs_panel)
        self.move_btn = Button(pos=(250, 50), img=ButtonImgMap.pause, init_scale=1)
        self.rotate_btn = Button(pos=(450, 50), img=ButtonImgMap.reset, init_scale=1)
        
        # staffs
        self.staffs_panel = ContainerSurface(size=(400, -200), pos=(50, 100), visible=False)
        self.staffs_bg = RectSurface(size=(0, 0), pos=(0, 0), color=pygame.Color(0, 0, 0, 100))

        self.staffs_panel.add_children([self.staffs_bg])
        
        self.add_children([self.staff_btn, self.move_btn, self.rotate_btn, self.staffs_panel])
    
    def open_staffs_panel(self, event: pygame.event.Event):
        self.staffs_panel.visible = True
    
    def draw(self):
        self.surface.fill("#13b974")
        return super().draw()
