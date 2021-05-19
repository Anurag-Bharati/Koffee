# [1] Importing the Modules

import sys, time
import pygame
from pygame.locals import *     # Importing pygame classes into global namespace :V Lol what?

import hud_grid
from PlayerBluePrint import Player
from level_generator import Earth, slime_group
import enemy


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
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,0,0,0,0,7,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,5,5,5,5,5,5,5,5,5,5,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,5,5,5,5,5,0,0,5,4,4,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,5,5,5,5,5,0,0,0,0,0,0,0,0,0,4,3,4,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,5,5,0,0,0,5,4,3,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,4,4,0,0,5,4,4,3,3,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,7,0,7,0,0,5,4,4,0,0,4,4,4,3,3,4,4,4,0,0,0,0,0,7,0,0,0,7,0,0,0,0,1,1,1],
    [1,1,1,5,5,5,5,5,5,5,4,4,4,5,5,4,4,3,3,3,3,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,1,1],
    [1,1,1,4,4,4,4,4,4,4,4,3,4,4,4,4,4,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1,1],
    [1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1],
    [1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1],
    [1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

#           >---------[CONSTANTS]---------<

Window_Width = 1280     # 40 Tiles Width of 32
Window_Height = 720     # 24 Tiles Height of 30

# COLORS

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Cyan = (70, 194, 166)
Deep_blue = (24, 20, 37)

#           >---------[VARIABLES]---------<

FPS = 60  # FPS CA
fps_color = pygame.Color("White")  # Init fps_color
move_left = False
move_right = False

# Debug tools

flags = False  # Enable or disable full-screen mode
grid = False
debug = False


# Creates a display

if flags:
    flags = HWSURFACE | DOUBLEBUF | FULLSCREEN

screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync=True)   # Size, flags, Color, verticalSy

pygame.mouse.set_cursor(pygame.cursors.diamond)  # change cursor icon

mainloop = True


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


X_ani = 1


def event_handler():            # All Event handling here

    global move_right, move_left, debug, grid, flags

    # Handling Animation
    if Knight.Alive:

        if Knight.above_ground:
            Player.change_action(Knight, new_action = 2)  # 2 = jump
        elif (move_right or move_left) and not Knight.above_ground and Knight.current_vel[0] != 0:
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
            elif event.key == K_d:
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

            elif event.key == K_d:
                move_right = False


debug_Animation_Timer = pygame.time.get_ticks()


def renderer():                 # All graphics here

    global X_ani

    screen.fill(Cyan)

    Knight.draw(screen)
    Knight.mov(move_left, move_right, level)
    Knight.update()

    level.draw(screen)

    slime_group.draw(screen)
    slime_group.update()

    if debug:

        screen.fill(pygame.Color(Deep_blue), (0, 0, X_ani, Window_Height))
        X_ani += 10
        X_ani *= 1.1

        if X_ani > Window_Width*0.3:
            X_ani = Window_Width*0.3
            debug_stats()
        pygame.draw.rect(screen, Red, Knight.rect, 1)
    if not debug:
        screen.fill(pygame.Color(Deep_blue), (0, 0, X_ani, Window_Height))
        X_ani *= 0.9

        if X_ani < -1:
            X_ani = -1

    if grid and not debug:
        hud_grid.draw_grid(screen, White, Window_Width, Window_Height, font_consolas)
        pygame.draw.rect(screen, Red, Knight.rect, 1)

    screen.blit(update_fps(), (10, 3))     # Must be at last :)
    pygame.display.update()


Knight = Player("player", 1, 150, 300, .9, 3)

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

    screen.blit(mouse_pos, (10, 330))

    screen.blit(game_uptime, (10, 350))

    screen.blit(debugNote, (10, 380))
    screen.blit(debugNote0, (10, 400))
    screen.blit(debugNote1, (10, 420))
    screen.blit(debugNote2, (10, 440))

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
        Knight_velocity = font_consolas.render(str(f"knight_vel:{Knight.current_vel}"), True, White)
        Knight_action = font_consolas.render(str(f"knight_action:{Knight.action}"), True, White)
        Knight_animation_index = font_consolas.render(str(f"knight_action_index:{Knight.animation_index}"), True, White)

        game_uptime = font_consolas.render(str(f"game_uptime: {Knight.update_time // 1000} (sec)"), True, White)
        mouse_pos = font_consolas.render(str(f"mouse_pos:{pygame.mouse.get_pos()}"), True, White)


initial_time = pygame.time.get_ticks()

debug_title = font_consolas.render(str("DEBUG_STAT"), True, White)

game_info = font_consolas.render("version 1.3 | Dev(fe/be):210030", True, White)

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
Knight_velocity = font_consolas.render(str(f"knight_vel:{Knight.current_vel}"), True, White)
Knight_action = font_consolas.render(str(f"knight_action:{Knight.action}"), True, White)
Knight_animation_index = font_consolas.render(str(f"knight_action_index:{Knight.animation_index}"), True, White)

game_uptime = font_consolas.render(str(f"game_uptime: {Knight.update_time // 1000} (sec)"), True, White)
mouse_pos = font_consolas.render(str(f"mouse_pos:{pygame.mouse.get_pos()}"), True, White)

debugNote = font_consolas.render(str("NOTES:"), True, White)
debugNote0 = font_consolas.render(str("     Press \"TAB\" to collapse Debug Window."), True, White)
debugNote1 = font_consolas.render(str("     Press \"LCTRL\" to toggle Grid View."), True, White)
debugNote2 = font_consolas.render(str("     Press \"Esc\" to Exit the game."), True, White)


if __name__ == "__main__":

    icon = pygame.image.load("assets/images/Koffee.png").convert_alpha()

    pygame.display.set_icon(icon)

    while mainloop:

        gameClock.tick(FPS)

        event_handler()

        renderer()
    pygame.mixer.quit()
    pygame.quit()

else:
    mainloop = False
