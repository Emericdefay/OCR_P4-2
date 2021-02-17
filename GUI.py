import pygame
from pgu import gui

WIDTH = 1800
HEIGHT = 900

class Editor(gui.Dialog):
    def __init__(self):


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu")
    pygame.display.get_surface().fill((255, 255, 255))
    clock = pygame.time.Clock()

    # Text Editor :

    offset_X = 50
    offset_Y = 50
    textAreaWidth = 400
    textAreaHeight = 600

    run = True

    while run:
        clock.tick(60)
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                run = False
                pygame.quit()

        TX.display_editor()
        pygame.display.flip()

