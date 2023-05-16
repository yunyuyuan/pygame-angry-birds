import pygame
from typing import List, Union, Tuple
from . import Game

class Drawable():
    def draw(self):
        '''
        每个元素都有draw方法
        '''
        pass

class EventSurface(Drawable, pygame.Surface):
    '''
    带有鼠标和键盘事件的Surface
    '''
    def __init__(self, *args, **kwargs):
        super(pygame.Surface).__init__(*args, **kwargs)
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False
    
class ContainerSurface(EventSurface):
    def __init__(
        self, 
        size: Tuple[float, float],
        pos: Tuple[float, float],
    ):
        super().__init__()
        self.children: List[ElementSurface] = []
    
    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]
    
    @property
    def children_stack(self):
        ''' 所有的子surface，事件将从右往左依次处理 '''
        return reversed(self.visible_children)
        
    def draw(self):
        ''' 按顺序画出每一个子组件 '''
        for child in self.children_stack:
            child.draw()
        return super().draw()

class PageSurface(EventSurface):
    '''
    大页面，目前有三个
    * home
    * level
    * game
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children: List[ElementSurface] = []
    
    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]
    
    @property
    def children_stack(self):
        ''' 所有的子surface，事件将从右往左依次处理 '''
        return reversed(self.visible_children)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True说明被子组件拦截 '''
        for child in self.children_stack:
            if child.mouse_event(event):
                return True
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        return False
    
    def draw(self):
        ''' 按顺序画出每一个子组件 '''
        for child in self.children_stack:
            child.draw()
        return super().draw()
    
    def back(self):
        pass

class AnimationSurface(EventSurface):
    def __init__(self, speed = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 0代表静止，1代表向前，2代表向后
        self.status = 0
        self.speed = speed
    
    def start_animation(self, status: int):
        if self.status == status:
            return

class ElementSurface(EventSurface):
    def __init__(self, visible = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visible = visible
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        return super().mouse_event(event)