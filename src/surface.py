import pygame
from typing import List, Union, Tuple

from src.utils.smart_arr import arr_sub
from . import Game

class Drawable():
    def draw(self):
        '''
        每个元素都有draw方法
        '''
        pass

class Animatable():
    def animation_event(self):
        if isinstance(self, Animation):
            self.animate()
'''
----------------------------------------------------------------------
'''
class EventSurface(Drawable):
    '''
    带有鼠标和键盘事件的Drawable
    '''
    def __init__(self, size: Tuple[float, float], pos: Tuple[float, float], parent: Union[None, "ContainerSurface"] = None, visible = True, flags=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surface = pygame.Surface(size=size, flags=flags)
        self.size = list(size)
        self.pos = list(pos)
        self.visible = visible
        self.parent = parent
    

    def is_mouse_inside(self, event: pygame.event.Event) -> bool:
        return 0 <= event.pos[0]-self.pos[0] <= self.size[0] and \
               1 <= event.pos[1]-self.pos[1] <= self.size[1]
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False


ChildrenType = List[Union["ContainerSurface", "ElementSurface"]]
class ContainerSurface(EventSurface, Animatable):
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
        super().__init__(size=size if size else Game.geometry, pos=pos, flags=pygame.SRCALPHA, *args, **kwargs)
        self.children: ChildrenType = []
    
    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]
    
    @property
    def children_stack(self):
        ''' 所有的子组件，事件将从右往左依次处理 '''
        return reversed(self.visible_children)
    
    def add_children(self, children: ChildrenType):
        for child in children:
            child.parent = self
        self.children.extend(children)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        # 鼠标在container内部, 拦截
        if self.is_mouse_inside(event=event):
            # 修改为相对坐标
            event.pos = arr_sub(event.pos, self.pos)
            for child in self.children_stack:
                if child.mouse_event(event):
                    break
            return True
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        # 键盘事件永远被第一个拦截
        for child in self.children_stack:
            if child.keyboard_event(event):
                break
        return True
    
    def animation_event(self):
        super().animation_event()
        for child in self.children_stack:
            child.animation_event()
    
    def draw(self):
        ''' 按顺序画出每一个子组件 '''
        for child in self.visible_children:
            child.draw()
        parent_surface = self.parent.surface if self.parent else Game.screen
        parent_surface.blit(self.surface, self.pos)
        return super().draw()


class Animation():
    '''
    特性：
    * 不可中断
    '''
    def __init__(self, speed = 150, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animation_state = -1
        # 0.01~1.00
        self.animation_progress: float = 0
        self.animation_speed = Game.fps_frame_sec/speed
    
    def animation_step(self, progress: float):
        raise NotImplementedError("you must define the animation step!")
    
    def animate(self):
        new_progress = self.animation_progress + self.animation_speed*self.animation_state
        if 0 <= new_progress < 1:
            self.animation_progress = new_progress
            self.animation_step(self.animation_progress)

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


class ElementSurface(EventSurface, Animatable):
    '''
    基本组件
    '''
    def __init__(self, size: Tuple[float, float], pos: Tuple[float, float], *args, **kwargs):
        super().__init__(size=size, pos=pos, *args, **kwargs)
