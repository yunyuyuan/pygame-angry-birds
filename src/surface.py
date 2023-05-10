import pygame
from typing import List, Union
from . import Game

class EventSurface(pygame.Surface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def mouse_event(self, event: pygame.event.Event) -> bool:
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        return False


class PageSurface(EventSurface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children: List[ElementSurface] = []
    
    @property
    def visible_children(self):
        return [x for x in self.children if x.visible]
    
    @property
    def children_stack(self):
        return reversed(self.visible_children)
        
    def mouse_event(self, event: pygame.event.Event) -> bool:
        for child in self.children_stack:
            if child.mouse_event(event):
                return True
        return False
    
    def keyboard_event(self, event: pygame.event.Event) -> bool:
        return False
    
    def back(self):
        pass


class ElementSurface(EventSurface):
    def __init__(self, visible = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visible = visible