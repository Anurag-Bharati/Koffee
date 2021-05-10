# [1] Importing the Modules

import sys
import pygame
from pygame.locals import *     # Importing pygame classes into global namespace :V Lol what?

# [2] Init the pygame modules:

pygame.mixer.init()
pygame.init()


pygame.display.set_caption("Koffee")
font_impact = pygame.font.SysFont("Impact", 18)
font_consolas = pygame.font.SysFont("consolas", 15)

# [3] Setting up a pause sys for main loop so that game match the given frame-rate:

gameClock = pygame.time.Clock()

#           >---------[CONSTANTS]---------<

Window_Width = 1280
Window_Height = 720

# COLORS

White = (255, 255, 255)
Black = (0, 0, 0)

#           >---------[VARIABLES]---------<

FPS = 60  # FPS CA
fps_color = pygame.Color("White")  # Init fps_color

# Debug tools

flags = False  # Enable or disable full-screen mode

# Creates a display

if flags:
    flags = HWSURFACE | DOUBLEBUF | FULLSCREEN

screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync=True)   # Size, flags, Color, verticalSy

pygame.mouse.set_cursor(pygame.cursors.diamond)  # change cursor icon

print(pygame.display.get_window_size())  # used for debugging the actual size


def update_fps():  # Function for fps-overlay

    global fps_color

    fps = str(int(gameClock.get_fps()))     # Getting raw fps value and converting to string data type
    if gameClock.get_fps() >= 60:           # Basic logic for dynamic fps colors :P
        fps_color = pygame.Color("green")
    elif 50 <= gameClock.get_fps() < 60:
        fps_color = pygame.Color("gold")
    elif 40 <= gameClock.get_fps() < 50:
        fps_color = pygame.Color("orange")
    elif 30 <= gameClock.get_fps() < 40:
        fps_color = pygame.Color("red")
    elif gameClock.get_fps() <= 29:
        fps_color = pygame.Color("red2")

    fps_text = font_impact.render(fps, True, fps_color)     # Rendering as font

    return fps_text


def event_handler():            # All Event handling here

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.mixer.quit()
            pygame.quit()
            sys.exit()


def renderer():                 # All graphics here

    pygame.display.update()
    screen.fill(White)

    screen.blit(update_fps(), (10, 10))     # Must be at last :)


def mains():                    # Main function

    mainloop = True
    while mainloop:

        gameClock.tick(FPS)

        event_handler()

        renderer()


if __name__ == '__main__':
    mains()
