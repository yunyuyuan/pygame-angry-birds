import pygame
from typing import List, Union
from . import Game

class EventSurface(pygame.Surface):
    mouse_triggered = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscription = Game.event_bus.subscribe(self.mouse_event)
        self.items: List[EventSurface] = []
    
    def mouse_event(self, event: int):
        raise NotImplementedError("Mouse Event")
    
    def add_item(self, item: "EventSurface"):
        self.items.append(item)
    
    def dispose(self):
        self.subscription.dispose()
        for item in self.items:
            item.dispose()

