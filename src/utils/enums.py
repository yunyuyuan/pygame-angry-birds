from enum import Enum

class ButtonImgMap(Enum):
    setting = ((10, 10), (10, 10))
    pause = ((254, 739), (99, 108))
    resume = ((902, 294), (71, 80))
    reset = ((254, 852), (99, 108))

    # my buttons
    my_materials = ((38,26), (148, 166))
    my_move = ((206,26), (148, 166))
    my_rotate = ((375,26), (148, 166))
    my_preview = ((543,26), (148, 166))


class CollisionTypes(Enum):
    bird = 1
    pig = 2
    obstacle = 3


class BirdTypes(Enum):
    red = 1,
    orange = 2,
    blue = 3,


class ObstacleRectTypes(Enum):
    w4_h1 = 1

