import pygame

from src.home import HomePage
from src.game import GamePage
from . import Game

def start_game():
    clock = pygame.time.Clock()

    pygame.time.set_timer(Game.fps_event, Game.fps_frame_sec)
    Game.active_page = GamePage(editing=True)
    # Game.active_page = HomePage(level=4)

    while Game.running:
        # fill the screen with a color to wipe away anything from last frame
        Game.pygame_event()

        Game.active_page.draw()

        fps = int(clock.get_fps())
        pygame.display.set_caption(str(fps))
        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(Game.fps)

    pygame.quit()