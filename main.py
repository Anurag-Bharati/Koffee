# [1] Importing the Modules

import sys
import pygame
from pygame.locals import *     # Importing pygame classes into global namespace :V Lol what?

import hud_grid

from PlayerBluePrint import Player


# [2] Init the pygame modules:

pygame.mixer.init()
pygame.init()

pygame.display.set_caption("Koffee")
font_impact = pygame.font.SysFont("Impact", 18)
font_consolas = pygame.font.SysFont("consolas", 15)

# [3] Setting up a pause sys for main loop so that game match the given frame-rate:

gameClock = pygame.time.Clock()

#           >---------[CONSTANTS]---------<

Window_Width = 1280     # 40 Tiles Width 32
Window_Height = 720     # 24 Tiles Height 30

# COLORS

White = (255, 255, 255)
Black = (0, 0, 0)
Cyan = (70, 194, 166)

#           >---------[VARIABLES]---------<

FPS = 60  # FPS CA
fps_color = pygame.Color("White")  # Init fps_color
move_left = False
move_right = False

# Debug tools

flags = True  # Enable or disable full-screen mode
grid = True

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
    global move_right, move_left

    # Handling Animation
    if Knight.Alive:

        if Knight.above_ground:
            Player.change_action(Knight, new_action = 2)  # 2 = jump
        elif move_right or move_left:
            Player.change_action(Knight, new_action = 1)  # 1 = run
        else:
            Player.change_action(Knight, new_action = 0)  # 0 = idle

    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.mixer.quit()
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:  # Triggered when key is pressed down
            if event.key == K_a:
                move_left = True
            if event.key == K_d:
                move_right = True
            if event.key == K_SPACE:
                Knight.isJump = True

        if event.type == KEYUP:  # Released when key is released
            if event.key == K_a:
                move_left = False

            if event.key == K_d:
                move_right = False


def renderer():                 # All graphics here

    pygame.display.update()
    screen.fill(Cyan)

    Knight.draw(screen)
    Knight.mov(Window_Width, move_left, move_right)
    Knight.update()

    if grid:
        hud_grid.draw_grid()

    screen.blit(update_fps(), (5, 3))     # Must be at last :)


Knight = Player("player", 1, 100, 500, 1.25, 3)


def mains():                    # Main function

    mainloop = True
    while mainloop:

        gameClock.tick(FPS)

        event_handler()

        renderer()


if __name__ == '__main__':
    mains()
