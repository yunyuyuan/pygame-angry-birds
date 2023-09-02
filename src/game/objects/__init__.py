import math
from typing import List, Sequence, Tuple
import pygame
import pymunk
from src import Game, game
from src.utils.enums import BirdTypes, CollisionTypes, MaterialShape, ObstacleTypes

from src.utils.surface import BaseSurface
from src.utils.vector import Vector

def poly_box(body: pymunk.Body, pos: Tuple[float, float], size: Tuple[float, float]):
    left_top = pos
    right_top = (pos[0]+size[0], pos[1])
    right_bottom = (pos[0]+size[0], pos[1]+size[1])
    left_bottom = (pos[0], pos[1]+size[1])
    return pymunk.Poly(body, [left_top, right_top, right_bottom, left_bottom])

class GameObject(BaseSurface):
    '''
    pymunk & pygame
    游戏对象，用于创建一个物理引擎内的物体，并可以画到屏幕上
    '''
    def __init__(self, space: pymunk.Space, angle = 0.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.space = space
        self.body: pymunk.Body
        self.parent: BaseSurface
        self.shapes: List[pymunk.Shape]
        self.angle = angle

        # 正在删除，并且鼠标悬停在该物体上，用于高亮
        self.deleting_focus = False
    
    def add_to_space(self):
        self.space.add(self.body, *self.shapes)

    def remove_from_space(self):
        self.space.remove(self.body, *self.shapes)

    def reload(self):
        pass

    def check_mouse_inside(self, pos: Tuple[float, float]):
        for shape in self.shapes:
            self.deleting_focus = shape.point_query(pos).distance <= 0
            # 只要有一个shape在鼠标内，则可以return
            if self.deleting_focus:
                return True
        return False

    def draw(self):
        if Game.debug or self.deleting_focus:
            color = pygame.Color("red") if self.deleting_focus else pygame.Color("black")
            for shape in self.shapes:
                if isinstance(shape, pymunk.Poly):
                    ps = [p.rotated(shape.body.angle) + shape.body.position for p in shape.get_vertices()]
                    ps = [(round(p.x), round(self.parent.size[1] - p.y)) for p in ps]
                    ps += [ps[0]]
                    pygame.draw.lines(self.parent_surface, color, False, ps, 2)
                elif isinstance(shape, pymunk.Circle):
                    p = shape.body.position
                    pygame.draw.circle(self.parent_surface, color, (round(p.x), round(self.parent.size[1] - p.y)), shape.radius, width=2)


class GameCollisionObject(GameObject):
    '''
    带碰撞的GameObject
    '''
    def __init__(self, collision_type: CollisionTypes, *args, **kwargs):
        super().__init__(size=collision_type.size, *args, **kwargs)
        self.collision_type = collision_type
        
        # 首次把状态设为 0
        self.collision_status = 0

    @property
    def current_surface(self):
        return self.collision_type.surfaces[self.collision_status]

    def collision(self, ke: float):
        pass


    def draw(self):
        pos = (self.body.position.x, self.parent.size[1] - self.body.position.y)

        angle_degrees = math.degrees(self.body.angle)
        rotated_surface = pygame.transform.rotate(self.current_surface, angle_degrees)

        offset = pymunk.Vec2d(*rotated_surface.get_size()) / 2
        pos = pos - offset

        self.parent_surface.blit(rotated_surface, (pos.x, pos.y))
        super().draw()


class GameObstacleObject(GameCollisionObject):
    def __init__(self, pos: Tuple[float, float], type: str, angle: float, *args, **kwargs):
        super().__init__(
            pos=pos,
            collision_type=ObstacleTypes[type],
            angle=angle,
            *args, **kwargs
        )
        if self.collision_type.material_shape == MaterialShape.box:
            # 实心box
            self.body = pymunk.Body(10, moment=pymunk.moment_for_box(10, self.collision_type.size), body_type=pymunk.Body.DYNAMIC)
            self.shapes = [pymunk.Poly.create_box(self.body, size=self.collision_type.size)]
            self.body.position = self.pos
            self.body.angle = self.angle
        elif self.collision_type.material_shape == MaterialShape.hollow_box:
            # 空心box
            self.body = pymunk.Body(10, moment=pymunk.moment_for_box(10, self.collision_type.size), body_type=pymunk.Body.DYNAMIC)
            square_size = self.collision_type.size[0]
            small_size = square_size / 4.5
            half = square_size / 2
            self.shapes = [
                poly_box(self.body, pos=(0-half, 0-half), size=(square_size, small_size)),
                poly_box(self.body, pos=(square_size-small_size-half, small_size-half), size=(small_size, square_size-2*small_size)),
                poly_box(self.body, pos=(0-half, square_size-small_size-half), size=(square_size, small_size)),
                poly_box(self.body, pos=(0-half, small_size-half), size=(small_size, square_size-2*small_size)),
            ]
            self.body.position = self.pos
            self.body.angle = self.angle
        elif self.collision_type.material_shape == MaterialShape.circle:
            # 实心圆
            radius = self.collision_type.size[0]/2
            self.body = pymunk.Body(10, pymunk.moment_for_circle(10, radius, radius), body_type=pymunk.Body.DYNAMIC)
            self.shapes = [pymunk.Circle(self.body, radius)]
            self.body.position = self.pos
            self.body.angle = self.angle
        else:
            raise BaseException("You should handle material: "+self.collision_type.material_shape.name)
        
        for shape in self.shapes:
            shape.friction = 0.5
            shape.collision_type = self.collision_type.material_type.value

        self.add_to_space()

    def reload(self):
        self.body.position = self.pos
        self.body.angle = self.angle
        self.body.velocity = (0,0)
        self.body.angular_velocity = 0
        return super().reload()


class GameFixedObject(GameObject):
    def __init__(self, pos: Tuple[float, float], size: Tuple[float, float], type: MaterialShape, angle: float, *args, **kwargs):
        super().__init__(pos=pos, angle=angle, size=size, *args, **kwargs)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        if type == MaterialShape.box:
            self.shapes = [pymunk.Poly.create_box(self.body, size=size)]
        else:
            half_size = self.size / 2
            self.shapes = [pymunk.Poly(self.body, [(-half_size[0], -half_size[1]), (-half_size[0], half_size[1]),(half_size[0], -half_size[1])])]
        self.body.position = self.pos
        self.body.angle = self.angle

        self.add_to_space()

    def draw(self):
        # pos = (self.body.position.x, self.parent.size[1] - self.body.position.y)

        # angle_degrees = math.degrees(self.body.angle)
        # rotated_surface = pygame.transform.rotate(self.current_surface, angle_degrees)

        # offset = pymunk.Vec2d(*rotated_surface.get_size()) / 2
        # pos = pos - offset

        # self.parent_surface.blit(rotated_surface, (pos.x, pos.y))
        return super().draw()
    

class GameBirdObject(GameCollisionObject):
    def __init__(self, bird_type: str, *args, **kwargs):
        super().__init__(collision_type=BirdTypes[bird_type], *args, **kwargs)

        self.bird_radius = self.collision_type.size[0] / 2
        self.body = pymunk.Body(10, pymunk.moment_for_circle(10, self.bird_radius, self.bird_radius), body_type=pymunk.Body.DYNAMIC)
        self.shapes = [pymunk.Circle(self.body, self.bird_radius)]
        self.shapes[0].friction = 1
        
        self.add_to_space()
    
    def launch(self, position: Tuple[float, float], relative_pos: Vector):
        self.body.position = position
        self.body.apply_impulse_at_world_point(pymunk.Vec2d(-relative_pos[0], relative_pos[1]) * 100, self.body.position)


# from .fixed_line import FixedLineObject
# from .fixed_poly import FixedPolyObject
# from .obstacle_rect import ObstacleRectObject
# from .orange_bird import OrangeBirdObject