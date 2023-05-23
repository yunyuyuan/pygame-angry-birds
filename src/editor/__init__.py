import pygame
import pymunk

from src.components.button import Button
from src.components.rect import RectSurface
from src.utils.enums import ButtonImgMap
from src.utils.surface import ContainerSurface, PageSurface


class EditorPage(PageSurface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 添加物料
        self.staff_btn = Button(pos=(5, 5), img=ButtonImgMap.my_materials, init_scale=0.6, on_click=self.open_staffs_panel)
        # 移动物料
        self.move_btn = Button(pos=(105, 5), img=ButtonImgMap.my_move, init_scale=0.6)
        # 旋转物料
        self.rotate_btn = Button(pos=(205, 5), img=ButtonImgMap.my_rotate, init_scale=0.6)
        # 切换预览模式
        self.preview_btn = Button(pos=(305, 5), img=ButtonImgMap.my_preview, init_scale=0.6)
        
        # staffs
        self.staffs_panel = ContainerSurface(size=(400, -120), pos=(5, 5), pos_bottom=True, visible=False)
        self.staffs_bg = RectSurface(size=(0, 0), pos=(0, 0), color=pygame.Color(0, 0, 0, 100))

        self.staffs_panel.add_children([self.staffs_bg])
        
        self.add_children([self.staff_btn, self.move_btn, self.rotate_btn, self.preview_btn, self.staffs_panel])
    
    def open_staffs_panel(self, event: pygame.event.Event):
        self.staffs_panel.visible = True
    
    def draw(self):
        self.surface.fill("#13b974")
        return super().draw()
