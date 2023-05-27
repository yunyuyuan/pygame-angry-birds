from typing import Tuple, TypedDict
from src.utils.enums import ObstacleTypes

from src.utils.vector import Vector

class ObstacleProp(TypedDict):
    pos: Vector
    type: ObstacleTypes
    angle: float