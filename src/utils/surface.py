from src import Game
from src.utils.animation import Animation

import pygame

from typing import Callable, Generic, List, Optional, Tuple, TypeVar, Union


class Drawable():
    def draw(self):
        '''
        每个元素都有draw方法
        '''
        pass


ParentType = TypeVar('ParentType', pygame.Surface, "BaseSurface")
class BaseSurface(Drawable, Generic[ParentType]):
    '''
    带有鼠标和键盘事件的Drawable
    '''
    def __init__(
            self,
            size: Tuple[float, float],
            pos: Tuple[float, float],
            parent: Optional[ParentType] = None,
            visible = True,
            flags = pygame.SRCALPHA,
            pos_bottom = False,
            pos_right = False,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.origin_size = size
        self._parent: ParentType
        self.size: pygame.Vector2
        self.parent = Game.screen if parent is None else parent # type: ignore
        self.surface = pygame.Surface(size=self.size, flags=flags)
        self._pos = pos
        self.pos_bottom = pos_bottom
        self.pos_right = pos_right
        self.visible = visible
        self.scale: float = 1
        ''' 只会在GamePanel里用 '''

    @property
    def parent(self) -> ParentType:
        return self._parent

    @parent.setter
    def parent(self, parent: ParentType):
        self._parent = parent
        # 子组件的 size 可能与父组件的 size 相关
        parent_size = parent.get_size() if isinstance(parent, pygame.Surface) else parent.size
        self.size = pygame.Vector2((self.origin_size[0] if self.origin_size[0] > 0 else parent_size[0]+self.origin_size[0], self.origin_size[1] if self.origin_size[1] > 0 else parent_size[1]+self.origin_size[1]))
        if getattr(self, 'surface', None):
            self.surface = pygame.transform.scale(self.surface, self.size)

    @property
    def parent_surface(self) -> pygame.Surface:
        return self.parent if isinstance(self.parent, pygame.Surface) else self.parent.surface

    @property
    def pos(self) -> pygame.Vector2:
        return pygame.Vector2((
            self._pos[0] if not self.pos_right else Game.geometry[0]-self._pos[0]-self.size[0],
            self._pos[1] if not self.pos_bottom else Game.geometry[1]-self._pos[1]-self.size[1],
        ))

    @pos.setter
    def pos(self, pos):
        self._pos = pos
     
    @property
    def relative_mouse(self):
        return (pygame.Vector2(pygame.mouse.get_pos()) - self.pos)/self.scale

    def check_mouse_inside(self, event: pygame.event.Event) -> bool:
        return 0 <= event.pos[0]-self.pos[0] <= self.size[0]*self.scale and \
               1 <= event.pos[1]-self.pos[1] <= self.size[1]*self.scale

    def mouse_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False

    def keyboard_event(self, event: pygame.event.Event) -> bool:
        ''' 返回True则说明被拦截，不再继续往下处理 '''
        return False
    
    def animation_event(self):
        ''' 如果没有继承Animation，则不会执行该函数 '''
        if isinstance(self, Animation):
            self.animate()

    def draw(self):
        # 只画出在parent_surface内的部分
        if 'GamePanel' in str(self.__class__):
            clipped = self.surface.subsurface(-self.pos / self.scale, Game.geometry / self.scale)
            scaled = pygame.transform.scale_by(clipped, self.scale)
            self.parent_surface.blit(scaled, ((0, 0), Game.geometry))
        else:
            scaled = pygame.transform.scale_by(self.surface, self.scale)
            pos = (self.pos, self.size)
            self.parent_surface.blit(scaled, pos)


ChildType = Union["ContainerSurface", "BaseSurface"]
T = TypeVar('T')
class ContainerSurface(Generic[T], BaseSurface[T]): # type: ignore
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
        super().__init__(size=size if size else (Game.geometry.x, Game.geometry.y), pos=pos, *args, **kwargs)
        self.children: List[ChildType] = []

    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]

    @property
    def children_stack(self):
        ''' 所有的子组件，事件将从右往左依次处理 '''
        return reversed(self.visible_children)

    def add_children(self, children: List[ChildType]):
        for child in children:
            child.parent = self
        self.children.extend(children)

    def remove_child(self, child: ChildType):
        self.children.remove(child)

    def mouse_event(self, event: pygame.event.Event) -> bool:
        # 鼠标在container内部, 拦截
        if self.check_mouse_inside(event=event):
            # 修改为相对坐标
            event.pos = self.relative_mouse
            for child in self.children_stack:
                if child.mouse_event(event):
                    break
            return True
        return False

    def keyboard_event(self, event: pygame.event.Event) -> bool:
        for child in self.children_stack:
            if child.keyboard_event(event):
                return True
        return False

    def animation_event(self):
        super().animation_event()
        for child in self.children_stack:
            child.animation_event()

    def draw(self, after_draw_children: Optional[Callable] = None):
        ''' 按顺序画出每一个子组件 '''
        for child in self.visible_children:
            child.draw()
        if after_draw_children:
            after_draw_children()
        if Game.debug:
            pygame.draw.rect(self.parent_surface, (50, 50, 50), (self.pos, pygame.Vector2(self.surface.get_size())*self.scale), width=1)
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
        self.surface = Game.screen

    def back(self):
        pass


class ElementSurface(BaseSurface):
    '''
    基本组件
    '''
    def __init__(self, size: Tuple[float, float], pos: Tuple[float, float], *args, **kwargs):
        super().__init__(size=size, pos=pos, *args, **kwargs)
