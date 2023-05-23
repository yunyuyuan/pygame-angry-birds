from src import Game
from src.utils.animation import Animatable
from src.utils.vector import Vector

import pygame

from typing import List, Tuple, Union


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
    def __init__(
            self,
            size: Tuple[float, float],
            pos: Tuple[float, float],
            parent: Union[pygame.Surface, "EventSurface", None] = None,
            visible = True,
            flags = 0,
            pos_bottom = False,
            pos_right = False,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.origin_size = size
        self._parent: Union[pygame.Surface, "EventSurface"]
        self.size: Vector
        self.parent = Game.screen if parent is None else parent
        self.surface = pygame.Surface(size=self.size, flags=flags)
        self._pos = pos
        self.pos_bottom = pos_bottom
        self.pos_right = pos_right
        self.visible = visible

    @property
    def parent(self) -> Union[pygame.Surface, "EventSurface"]:
        return self._parent

    @parent.setter
    def parent(self, parent: Union[pygame.Surface, "EventSurface"]):
        self._parent = parent
        # 子组件的 size 可能与父组件的 size 相关
        parent_size = parent.get_size() if isinstance(parent, pygame.Surface) else parent.size
        self.size = Vector((self.origin_size[0] if self.origin_size[0] > 0 else parent_size[0]+self.origin_size[0], self.origin_size[1] if self.origin_size[1] > 0 else parent_size[1]+self.origin_size[1]))

    @property
    def parent_surface(self) -> pygame.Surface:
        return self.parent if isinstance(self.parent, pygame.Surface) else self.parent.surface

    @property
    def pos(self) -> Vector:
        return Vector((
            self._pos[0] if not self.pos_right else Game.geometry[0]-self._pos[0]-self.size[0],
            self._pos[1] if not self.pos_bottom else Game.geometry[1]-self._pos[1]-self.size[1],
        ))

    @pos.setter
    def pos(self, pos):
        self._pos = pos

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
            event.pos = Vector(event.pos) - self.pos
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
        self.parent_surface.blit(self.surface, self.pos)
        return super().draw()


class PageSurface(ContainerSurface):
    '''
    大页面，目前有三个
    * home
    * level
    * game
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(parent=Game.screen, *args, **kwargs)

    def back(self):
        pass


class ElementSurface(EventSurface, Animatable):
    '''
    基本组件
    '''
    def __init__(self, size: Tuple[float, float], pos: Tuple[float, float], *args, **kwargs):
        super().__init__(size=size, pos=pos, *args, **kwargs)