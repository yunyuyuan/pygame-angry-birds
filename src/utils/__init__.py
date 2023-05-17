import pymunk
from os.path import dirname, join
from .. import Game

# pygame 和 pymunk坐标转化
def pymunk_to_pygame(v: pymunk.Vec2d):
   return (v.x, Game.screen.get_height() - v.y)

def pygame_to_pymunk(v: pymunk.Vec2d):
   return (v.x, Game.screen.get_height() - v.y)

def get_asset_path(path: str):
    return join(dirname(__file__), '../../assets/'+path)