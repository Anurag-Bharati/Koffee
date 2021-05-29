# [1] Importing the Modules

import sys, math, time, os
import pygame
from pygame.locals import *     # Importing pygame classes into global namespace :V Lol what?
import pickle

import PlayerBluePrint
import hud_grid
from PlayerBluePrint import Player

from level_generator import Earth, slime_group, killable_blocks_group, gate_group, coin_group, koffee_group
from buttons import Button


# [2] Init the pygame modules:
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

pygame.display.set_caption("Koffee")


font_impact = pygame.font.SysFont("Impact", 18)
font_consolas = pygame.font.SysFont("consolas", 15)


# [3] Setting up a pause sys for main loop so that game match the given frame-rate:

WIN = PlayerBluePrint.WIN
gameClock = pygame.time.Clock()
current_level = 0

level_dat = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,0,0,0,0,7,0,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,1,5,5,5,5,5,5,5,5,5,5,0,0,0,0,0,0,5,5,5,11,11,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,0,0,11,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,5,5,5,5,5,0,0,5,4,4,0,0,0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,5,5,5,5,5,0,0,0,0,0,0,0,0,0,4,3,4,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,12,12,12,12,12,0,0,0,5,5,0,0,0,5,4,3,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,4,4,0,0,5,4,4,3,3,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,5,4,4,11,11,4,4,4,3,3,4,4,4,0,0,0,7,0,7,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,5,14,14,14,14,5,5,4,4,4,5,5,4,4,3,3,3,3,4,4,5,5,5,5,5,5,5,5,9,9,9,9,9,5,1,1,1],
    [1,1,1,4,15,15,15,15,4,4,4,3,4,4,4,4,4,3,3,3,3,4,4,4,4,4,4,4,4,4,4,10,10,10,10,10,4,4,1,1],
    [1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
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

fs = False  # Enable or disable full-screen mode
grid = False
debug = False
MainMenu = True
sChange = False     # used for Transitions
audiomute = True   # mute's audio.. used for toggle
reset = False   # Resets player with the key 'R'
portal_fx = True
death_fx = True

play_ambiance = False
stop_ambiance = False


volume = 0.1

# Creates a display
flags = 0
if fs:
    flags = HWSURFACE | DOUBLEBUF | FULLSCREEN

screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 32, vsync=True)  # Size, flags, Color, verticalSy

pygame.mouse.set_cursor(pygame.cursors.diamond)  # change cursor icon

icon = pygame.image.load("assets/images/Koffee.png").convert_alpha()

pygame.display.set_icon(icon)

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


debugWindow_X = 1


def event_handler():            # All Event handling here

    global move_right, move_left, debug, grid, flags, reset, WIN

    WIN = PlayerBluePrint.WIN

    # Handling Animation
    if Knight.Alive:

        if Knight.above_ground:
            Player.change_action(Knight, new_action = 2)  # 2 = jump
        elif (move_right or move_left) and not Knight.above_ground and Knight.current_vel[0] != 0:
            Player.change_action(Knight, new_action = 1)  # 1 = run
        else:
            Player.change_action(Knight, new_action = 0)  # 0 = idle
    if not Knight.Alive:
        Player.change_action(Knight, new_action = 3)
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
                if not Knight.above_ground:
                    jump_sfx.play()
                Knight.isJump = True
            if event.key == K_r:
                reset = True

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
Transition = 0
blackout_Timer = pygame.time.get_ticks()


def renderer():                 # All graphics here

    global debugWindow_X, Transition, blackout_Timer, MainMenu, audiomute, reset, current_level, WIN, portal_fx,\
        death_fx, volume, play_ambiance, stop_ambiance

    screen.fill(Cyan)

    coin_group.draw(screen)
    coin_group.update()

    koffee_group.draw(screen)
    koffee_group.update()

    gate_group.draw(screen)
    gate_group.update()

    Knight.draw(screen)
    if Knight.Alive and not MainMenu:

        Knight.mov(move_left, move_right, level)

    Knight.update()
    level.draw(screen)

    slime_group.draw(screen)
    slime_group.update()

    killable_blocks_group.draw(screen)
    killable_blocks_group.update()

    pygame.mixer.music.set_volume(volume)

    if Knight.Alive:

        death_fx = True

        if reset:
            if pygame.time.get_ticks() - blackout_Timer > 10:
                blackout_Timer = pygame.time.get_ticks()
                Transition += 1
                Transition *= 1.35
                if Transition >= 150:
                    Transition = 150
            main_bg1.set_alpha(Transition)
            screen.blit(main_bg1, (0, 0))
            if Transition == 150:
                Transition = 0
                Knight.Alive = False
                reset = False
        if WIN:
            if portal_fx:
                portal_fx = False
                portal_sfx.play()
            if pygame.time.get_ticks() - blackout_Timer > 10:
                blackout_Timer = pygame.time.get_ticks()
                Transition += 1
                Transition *= 1.35
                if Transition >= 150:
                    Transition = 150
            main_bg1.set_alpha(Transition)
            screen.blit(main_bg1, (0, 0))
            if Transition == 150:
                Knight.reset("player", 3, 150, 300, .9, 3)
                cleanup()
                portal_fx = True
        else:
            if pygame.time.get_ticks() - blackout_Timer > 10:
                blackout_Timer = pygame.time.get_ticks()

                Transition *= 0.96
                if Transition <= 0:
                    Transition = 0

                volume += 0.0001
                volume *= 1.01
                if volume >= 0.1:
                    volume = 0.1

            main_bg1.set_alpha(Transition)
            screen.blit(main_bg1, (0, 0))

    elif not Knight.Alive and not MainMenu:
        if death_fx:
            death_fx = False
            death_sfx.play()
        if pygame.time.get_ticks() - blackout_Timer > 10:
            blackout_Timer = pygame.time.get_ticks()
            volume -= 0.00001
            volume *= 0.95
            if volume <= 0.03:
                volume = 0.03
            Transition += 1
            Transition *= 1.08
            if Transition >= 150:
                Transition = 150

        main_bg.set_alpha(Transition)
        screen.blit(main_bg, (0, 0))

        if Transition == 150 and not Knight.Alive:                                   # RESETS HERE

            if restart_btn.draw(screen):
                Knight.reset("player", 3, 150, 300, .9, 3)
                Knight.Alive = True

            elif menu_btn.draw(screen) and not MainMenu:
                MainMenu = True
                Knight.Alive = False
                Transition = 0

            if audio_btn1.draw(screen):
                audiomute = not audiomute
                if audiomute:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1, 0.0, 500)

    if debug:

        screen.fill(pygame.Color(Deep_blue), (0, 0, debugWindow_X, Window_Height))
        debugWindow_X += 10
        debugWindow_X *= 1.1

        if debugWindow_X > Window_Width*0.3:
            debugWindow_X = Window_Width * 0.3
            debug_stats()
        pygame.draw.rect(screen, Red, Knight.rect, 1)

    if not debug:

        screen.fill(pygame.Color(Deep_blue), (0, 0, debugWindow_X, Window_Height))
        debugWindow_X *= 0.9

        if debugWindow_X < -1:
            debugWindow_X = -1

    if grid and not debug:
        hud_grid.draw_grid(screen, White, Window_Width, Window_Height, font_consolas)
        pygame.draw.rect(screen, Red, Knight.rect, 1)

    if play_ambiance and not MainMenu:
        play_ambiance = False
        ambiance.play(-1)

    screen.blit(update_fps(), (10, 3))     # Must be at last :)

    pygame.display.update()


def main_menu():
    global Transition, blackout_Timer, MainMenu, sChange, mainloop, fs, audiomute, flags, screen, volume,\
        stop_ambiance, play_ambiance
    screen.fill(Cyan)
    Knight.Alive = False

    ambiance.fadeout(1000)

    if fs:
        flags = HWSURFACE | DOUBLEBUF | FULLSCREEN
    else:
        flags = 0
    screen.blit(logo, (
        Window_Width//2 - logo.get_width()//2,
        Window_Height//4 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))

    if fs_btn.draw(screen):
        fs = not fs
        if fs:
            screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync = True)
        else:
            screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync = True)

    if audio_btn.draw(screen):
        audiomute = not audiomute
        if audiomute:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1, 0.0, 500)

    if start_btn.draw(screen) and Transition == 0:
        play_ambiance = True
        sChange = True

    if sChange:
        if pygame.time.get_ticks() - blackout_Timer > 10:
            blackout_Timer = pygame.time.get_ticks()
            Transition += 1
            Transition *= 1.05

            if Transition >= 150:
                Transition = 150
                sChange = False
                MainMenu = False
                Knight.Alive = True
    if exit_btn.draw(screen) and MainMenu:
        mainloop = False

    main_bg1.set_alpha(Transition)
    screen.blit(main_bg1, (0, 0))

    pygame.display.update()

    return flags


def cleanup():
    global WIN, level, level_data, pickle_opn, current_level
    WIN = False
    current_level += 1
    if os.path.exists(f"assets/levels/level{current_level}.dat"):
        slime_group.empty()
        killable_blocks_group.empty()
        gate_group.empty()
        with open(f"assets/levels/level{current_level}.dat", "rb") as pickle_opn:
            level_data = pickle.load(pickle_opn)
        level = Earth(level_data)


main_bg = pygame.image.load("assets/images/mainbg.png").convert_alpha()
main_bg1 = pygame.image.load("assets/images/mainbg1.png").convert_alpha()
restart_button = pygame.image.load("assets/images/buttons/restart.png").convert_alpha()
start_button = pygame.image.load("assets/images/buttons/start.png").convert_alpha()
exit_button = pygame.image.load("assets/images/buttons/exit.png").convert_alpha()
menu_button = pygame.image.load("assets/images/buttons/menu.png").convert_alpha()
fs_button = pygame.image.load("assets/images/buttons/fullscreen.png").convert_alpha()
audio_button = pygame.image.load("assets/images/buttons/audio.png").convert_alpha()
logo = pygame.image.load("assets/images/logoKoffee.png")
logo = pygame.transform.scale(logo, (logo.get_width()//3, logo.get_height()//3)).convert_alpha()

pygame.mixer.music.load("assets/audio/Koffee_ost.mp3")
pygame.mixer.music.set_volume(volume)

ambiance = pygame.mixer.Sound("assets/audio/Ambiance.mp3")
ambiance.set_volume(0.75)

portal_sfx = pygame.mixer.Sound("assets/audio/sfx/portal.wav")
portal_sfx.set_volume(0.6)

Knight = Player("player", 3, 150, 300, .9, 3)

jump_sfx = pygame.mixer.Sound("assets/audio/sfx/knight_jump.wav")
jump_sfx.set_volume(0.40)


death_sfx = pygame.mixer.Sound("assets/audio/sfx/knight_dead.wav")
death_sfx.set_volume(0.5)

if os.path.exists(f"assets/levels/level{current_level}.dat"):
    pickle_opn = open(f"assets/levels/level{current_level}.dat", "rb")
    level_data = pickle.load(pickle_opn)
    level = Earth(level_data)
    pickle_opn.close()

start_btn = Button(
    Window_Width//2 - start_button.get_width()//4,
    Window_Height//2 - start_button.get_height()//4, start_button, .5)

restart_btn = Button(
    Window_Width//2 - restart_button.get_width()//4,
    Window_Height//2 - restart_button.get_height()//4, restart_button, .5)
exit_btn = Button(
    Window_Width//2 - exit_button.get_width()//4,
    Window_Height//2 + exit_button.get_height()//1.5, exit_button, .5)
menu_btn = Button(
    Window_Width//1.21,
    Window_Height//1.25, menu_button, .35)

fs_btn = Button(
    Window_Width//2 - fs_button.get_width()//3,
    Window_Height//2 + fs_button.get_height()//3.2, fs_button, .3)

audio_btn = Button(
    Window_Width//2 + audio_button.get_width()//12 - audio_button.get_width()//24,
    Window_Height//2 + audio_button.get_height()//3.2, audio_button, .3)

audio_btn1 = Button(
    Window_Width//2 - audio_button.get_width()//6.65,
    Window_Height//2 + audio_button.get_height()//3.2, audio_button, .3)


def debug_stats():

    global rawTick, gameTime, gameRes, gameFps, activeFlags, playerMov, res, initial_time,\
        Knight_location, Knight_action, game_uptime, Knight_velocity, mouse_pos, Knight_animation_index, gameTick

    debug_update_timer = 50                                   # Timer for updating

    screen.blit(debug_title, (10, 40))
    screen.blit(game_info, (10, 60))
    screen.blit(gameFps, (10, 90))
    screen.blit(gameTime, (10, 110))
    screen.blit(rawTick, (150, 110))
    screen.blit(gameTick, (10, 130))
    screen.blit(activeFlags, (10, 150))
    screen.blit(gameRes, (10, 180))
    screen.blit(display_info, (10, 210))
    screen.blit(playerMov, (10, 230))
    screen.blit(Knight_location, (10, 250))
    screen.blit(Knight_velocity, (10, 270))
    screen.blit(Knight_action, (10, 290))
    screen.blit(Knight_animation_index, (10, 310))

    screen.blit(mouse_pos, (10, 350))

    screen.blit(game_uptime, (10, 380))

    screen.blit(debugNote, (10, 400))
    screen.blit(debugNote0, (10, 420))
    screen.blit(debugNote1, (10, 440))
    screen.blit(debugNote2, (10, 460))

    if pygame.time.get_ticks() - initial_time > debug_update_timer:

        initial_time = pygame.time.get_ticks()

        res = (Window_Width, Window_Height)

        rawTick = font_consolas.render(str(f"praw_tick:{gameClock.get_rawtime()}"), True, White)
        gameTime = font_consolas.render(str(f"previous_tick:{gameClock.get_time()}"), True, White)
        gameTick = font_consolas.render(str(f"game_tick:{pygame.time.get_ticks().__round__(5)}"), True, White)
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

game_info = font_consolas.render("version Alpha-1.9 | Dev(fe/be):210030", True, White)

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

    last_time = time.time()
    while mainloop:

        gameClock.tick(FPS)

        event_handler()

        if MainMenu:
            main_menu()

        if not MainMenu:
            renderer()

    pygame.mixer.quit()
    pygame.quit()

else:
    mainloop = False
# -2 - name
# 0 - menu
# 1 - game
# -1 - dead
# 2 - Victory
