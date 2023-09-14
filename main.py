import pygame
from src import Game

pygame.init()
Game.screen = pygame.display.set_mode(Game.geometry)

if __name__ == '__main__':
    from src.start import start_game
    start_game()