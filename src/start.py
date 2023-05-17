import pygame

from .game import GamePage
from . import Game


fps = 60.0

def start_game():
    # pygame setup
    pygame.init()
    Game.screen = pygame.display.set_mode(Game.geometry)
    clock = pygame.time.Clock()
    Game.active_page = GamePage()

    while Game.running:
        # fill the screen with a color to wipe away anything from last frame
        Game.pygame_event()

        Game.active_page.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()