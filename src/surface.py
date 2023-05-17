import pygame
from typing import List, Union, Tuple
from . import Game

class Drawable():
    def draw(self):
        '''
        每个元素都有draw方法
        '''
        pass

class EventSurface(Drawable):
    '''
    带有鼠标和键盘事件的Drawable
    '''
    def __init__(self, size: Tuple[float, float], parent: Union[None, "ContainerSurface"] = None, visible = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surface = pygame.Surface(size=size)
        self.visible = visible
        self.parent = parent
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False
    
class ContainerSurface(EventSurface):
    '''
    * Container没有实体
    * Container拦截鼠标和键盘事件, 依次传给child处理
    '''
    def __init__(
        self, 
        size: Union[Tuple[float, float], None] = None,
        pos: Tuple[float, float] = (0, 0),
        *args, **kwargs
    ):
        self.size = size if size else Game.geometry
        super().__init__(size=self.size, *args, **kwargs)
        self.pos = pos
        self.children: List[EventSurface] = []
    
    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]
    
    @property
    def children_stack(self):
        ''' 所有的子组件，事件将从右往左依次处理 '''
        return reversed(self.visible_children)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        if True:
            # 鼠标在container内部, 拦截
            for child in self.children_stack:
                if child.mouse_event(event):
                    break
            return True
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        # 键盘事件永远被拦截
        for child in self.children_stack:
            if child.keyboard_event(event):
                break
        return True
    
    def draw(self):
        ''' 按顺序画出每一个子组件 '''
        for child in self.children_stack:
            child.draw()
        parent_surface = self.parent.surface if self.parent else Game.screen
        parent_surface.blit(self.surface, self.pos)
        return super().draw()

class PageSurface(ContainerSurface):
    '''
    特殊的Container：大页面，目前有三个
    * home
    * level
    * game
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def back(self):
        pass

class AnimationSurface():
    '''
    * 有两种状态
    * 逐帧判断，并改变
    '''
    def __init__(self, speed = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 0代表静止，1代表向前
        self.status = 0
        # 0~100步
        self.progress = 0
        self.speed = speed
    
    def start_animation(self, status: int):
        if self.status == status:
            return
    
    def animation_step(self):
        pass

class ElementSurface(EventSurface):
    '''
    基本组件
    '''
    def __init__(self, size: Tuple[float, float], *args, **kwargs):
        super().__init__(size=size, *args, **kwargs)