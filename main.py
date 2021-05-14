# [1] Importing the Modules

import sys, time
import pygame
from pygame.locals import *     # Importing pygame classes into global namespace :V Lol what?

import hud_grid
from PlayerBluePrint import Player
from level_generator import Earth

# [2] Init the pygame modules:

pygame.mixer.init()
pygame.init()

pygame.display.set_caption("Koffee")
font_impact = pygame.font.SysFont("Impact", 18)
font_consolas = pygame.font.SysFont("consolas", 15)

# [3] Setting up a pause sys for main loop so that game match the given frame-rate:

gameClock = pygame.time.Clock()

level_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,1,1],
    [1,1,1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1,1],
    [1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1],
    [1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1],
    [1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1],
    [1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

#           >---------[CONSTANTS]---------<

Window_Width = 1280     # 40 Tiles Width 32
Window_Height = 720     # 24 Tiles Height 30

# COLORS

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Cyan = (70, 194, 166)

#           >---------[VARIABLES]---------<

FPS = 60  # FPS CA
fps_color = pygame.Color("White")  # Init fps_color
move_left = False
move_right = False

# Debug tools

flags = True  # Enable or disable full-screen mode
grid = False
debug = False

# Creates a display

if flags:
    flags = HWSURFACE | DOUBLEBUF | FULLSCREEN

screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync=True)   # Size, flags, Color, verticalSy

pygame.mouse.set_cursor(pygame.cursors.diamond)  # change cursor icon


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

    global move_right, move_left, debug, grid

    # Handling Animation
    if Knight.Alive:

        if Knight.above_ground:
            Player.change_action(Knight, new_action = 2)  # 2 = jump
        elif move_right or move_left and not Knight.above_ground:
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

            if event.key == K_TAB:
                if not debug:
                    grid = False
                    debug = True
                else:
                    debug = False

            if event.key == K_LCTRL:

                if not grid:
                    debug = False
                    grid = True
                else:
                    grid = False

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

    level.draw(screen)

    if grid:
        hud_grid.draw_grid()
        pygame.draw.rect(screen, Red, Knight.rect, 1)
    if debug:
        debug_stats()
        pygame.draw.rect(screen, Red, Knight.rect, 1)

    screen.blit(update_fps(), (10, 3))     # Must be at last :)


Knight = Player("player", 1, 100, 500, 1.25, 3)

level = Earth(level_data)


def debug_stats():

    global rawTick, gameTime, gameRes, gameFps, activeFlags, playerMov, res, initial_time,\
        Knight_location, Knight_action, game_uptime, Knight_velocity, mouse_pos, Knight_animation_index, gameTick

    debug_update_timer = 50                                   # Timer for updating

    screen.blit(debug_title, (10, 40))
    screen.blit(game_info, (10, 60))
    screen.blit(gameFps, (10, 90))
    screen.blit(gameTime, (10, 110))
    screen.blit(rawTick, (150, 110))
    screen.blit(gameTick, (250, 110))
    screen.blit(activeFlags, (10, 130))
    screen.blit(gameRes, (10, 150))
    screen.blit(display_info, (10, 180))
    screen.blit(playerMov, (10, 210))
    screen.blit(Knight_location, (10, 230))
    screen.blit(Knight_velocity, (10, 250))
    screen.blit(Knight_action, (10, 270))
    screen.blit(Knight_animation_index, (10, 290))

    screen.blit(mouse_pos, (10, 320))

    screen.blit(game_uptime, (10, 350))

    if pygame.time.get_ticks() - initial_time > debug_update_timer:

        initial_time = pygame.time.get_ticks()

        res = (Window_Width, Window_Height)

        rawTick = font_consolas.render(str(f"praw_tick:{gameClock.get_rawtime()}"), True, White)
        gameTime = font_consolas.render(str(f"previous_tick:{gameClock.get_time()}"), True, White)
        gameTick = font_consolas.render(str(f"game_tick:{pygame.time.get_ticks()}"), True, White)
        gameFps = font_consolas.render(str(f"frame_per_sec:{gameClock.get_fps().__round__(5)}"), True, White)
        activeFlags = font_consolas.render(str(f"active_flags:{screen.get_flags()}"), True, White)

        playerMov = font_consolas.render(str(f"knight_moving:{move_left or move_right}"), True, White)
        Knight_location = font_consolas.render(str(f"knight_location:{Knight.rect.x, Knight.rect.y}"), True, White)
        Knight_velocity = font_consolas.render(str(f"knight_vel:{Knight.debug_vel}"), True, White)
        Knight_action = font_consolas.render(str(f"knight_action:{Knight.action}"), True, White)
        Knight_animation_index = font_consolas.render(str(f"knight_action_index:{Knight.animation_index}"), True, White)
        game_uptime = font_consolas.render(str(f"game_uptime: {Knight.update_time // 1000} (sec)"), True, White)
        mouse_pos = font_consolas.render(str(f"mouse_pos:{pygame.mouse.get_pos()}"), True, White)


initial_time = pygame.time.get_ticks()

debug_title = font_consolas.render(str("DEBUG_STAT"), True, White)
game_info = font_consolas.render("version 1.2 | Dev(fe/be):210030", True, White)

res = (Window_Width, Window_Height)
rawTick = font_consolas.render(str(f"praw_tick:{gameClock.get_rawtime()}"), True, White)
gameTime = font_consolas.render(str(f"previous_tick:{gameClock.get_time()}"), True, White)
gameTick = font_consolas.render(str(f"game_tick:{pygame.time.get_ticks()}"), True, White)
gameFps = font_consolas.render(str(f"frame_per_sec:{gameClock.get_fps()}"), True, White)
activeFlags = font_consolas.render(str(f"active_flags:{screen.get_flags()}"), True, White)
gameRes = font_consolas.render(str(f"current_res:{res}"), True, White)
display_info = font_consolas.render(str(f"display_driver:{pygame.display.get_driver()}"), True, White)

playerMov = font_consolas.render(str(f"knight_moving:{move_left or move_right}"), True, White)
Knight_location = font_consolas.render(str(f"knight_location:{Knight.rect.x, Knight.rect.y}"), True, White)
Knight_velocity = font_consolas.render(str(f"knight_vel:{Knight.debug_vel}"), True, White)
Knight_action = font_consolas.render(str(f"knight_action:{Knight.action}"), True, White)
Knight_animation_index = font_consolas.render(str(f"knight_action_index:{Knight.animation_index}"), True, White)

game_uptime = font_consolas.render(str(f"game_uptime: {Knight.update_time // 1000} (sec)"), True, White)
mouse_pos = font_consolas.render(str(f"mouse_pos:{pygame.mouse.get_pos()}"), True, White)


def mains():                    # Main function

    mainloop = True
    while mainloop:

        gameClock.tick(FPS)

        event_handler()

        renderer()


if __name__ == '__main__':
    print(pygame.display.get_window_size())  # used for debugging the actual size
    print("> starting the main loop..")
    mains()

