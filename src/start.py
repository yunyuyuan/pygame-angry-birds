import pymunk
import pygame

from .game import collision_types, bird_types, obstacle_rect_types
from .game.objects import FixedLineObject, FixedPolyObject, ObstacleRectObject, OrangeBirdObject
from . import Game


fps = 60.0

def start_game():
    # pygame setup
    pygame.init()
    Game.screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    Game.space = pymunk.Space()
    Game.space.gravity = pymunk.Vec2d(0.0, -900.0)
    # space.gravity = pymunk.Vec2d(0.0, 0.0)
    
    # pygame 和 pymunk坐标转化
    pymunk_to_pygame = lambda v: (v.x, Game.screen.get_height() - v.y)
    pygame_to_pymunk = lambda pos: pymunk.Vec2d(pos[0], Game.screen.get_height() - pos[1])
    real_size = lambda x: x * 33.3
    
    fixed_line = FixedLineObject((0, 100), (1280, 100))
    fixed_poly1 = FixedPolyObject(vertices=((0, 0), (real_size(3), 0), (real_size(2.5), real_size(0.7)), (real_size(0.4), real_size(0.7))), 
                    pos=(100, 100)
                )
    fixed_poly2 = FixedPolyObject(vertices=((0, 0), (real_size(6.7), 0), (real_size(7.7), real_size(1.1)), (real_size(0.9), real_size(1.1))), 
                    pos=(700, 100)
                )
    fixed_poly3 = FixedPolyObject(vertices=((0, 0), (real_size(5.5), 0), (real_size(2.45), real_size(2.8))), 
                    pos=(923, 100)
                )
    fixed_poly4 = FixedPolyObject(vertices=((0, 0), (real_size(1.4), real_size(-1.3)), (real_size(3.62), real_size(1.12)), (real_size(2.2), real_size(2.5))), 
                    pos=(1005, 193)
                )
    
    Game.obstacles.append(ObstacleRectObject(rect_type=obstacle_rect_types["4x1"], size=(real_size(0.2), real_size(1)), 
                    pos=(740, 155)
                ))
    Game.obstacles.append(ObstacleRectObject(rect_type=obstacle_rect_types["4x1"], size=(real_size(0.9), real_size(0.2)), 
                    pos=(740, 175)
                ))
    
    bird_launching = False
    
    slingshot_pos = pymunk.Vec2d(300, 500)
    launch_pos = pymunk.Vec2d(*slingshot_pos)

    bird_radius = 24
    moment = pymunk.moment_for_circle(10, 0, bird_radius)
    bird_body = pymunk.Body(10, moment, body_type=pymunk.Body.DYNAMIC)
    bird_shape = pymunk.Circle(bird_body, bird_radius)
    bird_shape.friction = 0.5
    # bird_body.position = (500, 500)
    
    # 碰撞检测
    obstacle_collision_handler = Game.space.add_wildcard_collision_handler(collision_types["obstacle"])
    def obstacle_collision_fn(arbiter: pymunk.Arbiter, space: pymunk.Space, data):
        if arbiter.total_ke > 100000:            
            for obstacle in [x for x in Game.obstacles if x.collision_status != 1]:
                if obstacle.shape in [x for x in arbiter.shapes if x.collision_type == collision_types["obstacle"]]:
                    obstacle.collision(arbiter.total_ke)
                    break
    obstacle_collision_handler.post_solve = obstacle_collision_fn

    bird_collision_handler = Game.space.add_wildcard_collision_handler(collision_types["bird"])
    def bird_collision_fn(arbiter: pymunk.Arbiter, space: pymunk.Space, data):
        if arbiter.total_ke > 0:
            for bird in [x for x in Game.launched_birds if x.collision_status != 1]:
                if bird.shape in arbiter.shapes:
                    bird.collision(arbiter.total_ke)
                    break
    bird_collision_handler.post_solve = bird_collision_fn

    while running:
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if not bird_launching:
            #         mouse_pos = pygame_to_pymunk(event.pos)
            #         distance = mouse_pos.get_distance(slingshot_pos)
            #         if distance <= bird_radius:
            #             bird_launching = True
            # elif event.type == pygame.MOUSEMOTION:
            #     if bird_launching:
            #         launch_pos = pygame_to_pymunk(event.pos)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if bird_launching:
            #         bird_launching = False

            #         bird = OrangeBirdObject(bird_types["orange"], launch_pos, slingshot_pos)
            #         Game.launched_birds.append(bird)

            #         # 还原弹弓位置
            #         launch_pos = pymunk.Vec2d(*slingshot_pos)
        Game.pygame_event()

        # fill the screen with a color to wipe away anything from last frame
        Game.screen.fill("#13b3b9")

        fixed_line.draw()
        fixed_poly1.draw()
        fixed_poly2.draw()
        fixed_poly3.draw()
        fixed_poly4.draw()
        for obstacle in Game.obstacles:
            obstacle.draw()

        # 发射后
        for bird in Game.launched_birds:
            bird.draw()
        # 发射前
        pygame.draw.circle(Game.screen, pygame.Color("red"), center=pymunk_to_pygame(launch_pos), radius=bird_radius)

        # RENDER YOUR GAME HERE
        Game.space.step(1.0/fps)

        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()