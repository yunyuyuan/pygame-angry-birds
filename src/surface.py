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
    def __init__(self, size: Tuple[float, float], pos: Tuple[float, float], parent: Union[None, "ContainerSurface"] = None, visible = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.surface = pygame.Surface(size=size)
        self.size = size
        self.pos = pos
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
        super().__init__(size=size if size else Game.geometry, pos=pos, *args, **kwargs)
        self.children: List[EventSurface] = []
    
    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]
    
    @property
    def children_stack(self):
        ''' 所有的子组件，事件将从右往左依次处理 '''
        return reversed(self.visible_children)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        # 鼠标在container内部, 拦截
        if self.is_mouse_inside(event=event):
            # 修改为相对坐标
            event.pos = (event.pos[0]-self.pos[0], event.pos[1]-self.pos[1])
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
    
    def draw(self):
        ''' 按顺序画出每一个子组件 '''
        for child in self.visible_children:
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
        # 0~100步
        self.progress = 0
        self.speed = speed
    
    def next_step(self, status: int):
        pass
    
    def animation_step(self):
        pass

class ElementSurface(EventSurface):
    '''
    基本组件
    '''
    def __init__(self, size: Tuple[float, float], pos: Tuple[float, float], *args, **kwargs):
        super().__init__(size=size, pos=pos, *args, **kwargs)
