from typing import List, Tuple
import pygame
import pymunk
from os.path import dirname, join

from .. import Game
import math

# pygame 和 pymunk坐标转化
def pymunk_to_pygame(v: pymunk.Vec2d):
   return (v.x, Game.screen.get_height() - v.y)

def pygame_to_pymunk(v: pygame.Vector2, height: float):
   return (v[0], height - v[1])

def get_asset_path(*path: str):
    return join(dirname(__file__), '..', '..', 'assets', *path)

def clip_img(path: str, pos: Tuple[float, float], size: Tuple[float, float]):
    return pygame.image.load(get_asset_path(path)).subsurface(pygame.Rect(pos, size))

def load_subsurfaces(img: str, size: Tuple[int, int], *pos: Tuple[int, int]):
    surface = pygame.image.load(get_asset_path(f"images/{img}.png"))
    for p in pos:
        yield surface.subsurface(pygame.Rect(p, size))

def calculate_intersection(p1, p2, r):
    a, b = p1
    c, d = p2
    if a == c and b == d:
        return None  # Points are the same, intersection is the point itself
    
    # Calculate the slope and intercept of the line passing through (a, b) and (c, d)
    if c == a:
        return pygame.Vector2((a, b+(r if d > b else -r))) if abs(b - d) > r else None 
    m = (d - b) / (c - a)
    c_line = b - m * a
    
    # Solve the quadratic equation to find x coordinates of intersection points
    A = 1 + m**2
    B = 2 * (m * c_line - a - b * m)
    C = a**2 + c_line**2 - 2 * b * c_line + b**2 - r**2
    
    discriminant = B**2 - 4 * A * C
    
    if discriminant < 0:
        return None  # No real intersection points
    
    x1 = (-B + math.sqrt(discriminant)) / (2 * A)
    x2 = (-B - math.sqrt(discriminant)) / (2 * A)
    
    # Calculate corresponding y coordinates
    y1 = m * x1 + c_line if m != math.inf else d
    y2 = m * x2 + c_line if m != math.inf else d
    if a <= x1 <= c or a >= x1 >= c:
        return pygame.Vector2((x1, y1))
    if a <= x2 <= c or a >= x2 >= c:
        return pygame.Vector2((x2, y2))

def calculate_distance(p1: pygame.Vector2, p2: pygame.Vector2):
    subtract = p1 - p2
    return subtract[0]**2 + subtract[1]**2