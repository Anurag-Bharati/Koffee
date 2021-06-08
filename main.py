# [1] Importing the Modules

import math
import os
import pickle
import sys
import time

import pygame
from pygame.locals import *  # Importing pygame classes into global namespace :V Lol what?

import PlayerBluePrint
import hud_grid
import IO

from PlayerBluePrint import Player
from buttons import Button

from level_generator import Earth, slime_group, killable_blocks_group,\
    gate_group, coin_group, koffee_group, goffee_group


# [2] Init the pygame modules:
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()

pygame.display.set_caption("Koffee")


startDumping = True
startChecking = True

font_impact = pygame.font.SysFont("Impact", 18)
font_consolas = pygame.font.SysFont("consolas", 15)
font_calibri = pygame.font.SysFont("calibri", 24)
font_calibri0 = pygame.font.SysFont("calibri", 50)
font_calibriS = pygame.font.SysFont("calibri", 20)
font_calibriS.set_bold(True)
font_calibri.set_bold(True)
font_calibri0.set_bold(True)


# [3] Setting up a pause sys for main loop so that game match the given frame-rate:

WIN = PlayerBluePrint.WIN
gameClock = pygame.time.Clock()
current_level = 0

#           >---------[CONSTANTS]---------<

Window_Width = 1280     # 40 Tiles Width of 32
Window_Height = 720     # 24 Tiles Height of 30
USER = ""

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
VERSION = "Alpha-1.2"

coin = 0
coffee = 0

coffeeS = coffee
coinS = coin
score = coin * (coffee+1)
scoreH = 0
timePlayed = 0

goffee = 0

rect_bar = pygame.Rect(Window_Width // 3, 600, Window_Width // 3, 60)

dataIN = []

# Debug tools

fs = False  # Enable or disable full-screen mode
grid = False
debug = False

MainMenu = False
sBox_X = 350
sBox_Y = 550
sBoxYLevel = -500
status_boxL = pygame.Rect(100, sBoxYLevel, sBox_X, sBox_Y)
status_boxR = pygame.Rect(830, sBoxYLevel, sBox_X, sBox_Y)
sbl_topBoxL = pygame.Rect(status_boxL.center[0] - 140, status_boxL.center[1]//4, 280, 50)
sbl_topBoxR = pygame.Rect(status_boxR.center[0] - 140, status_boxR.center[1]//4, 280, 50)
text_opacity = 0

sblBody_Y = 5
sbl_BodyColor = (194, 133, 105)
sbl_bodyBoxL = pygame.Rect(status_boxL.center[0] - 120, status_boxL.center[1] // 2, 240, sblBody_Y)
sbl_bodyBoxR = pygame.Rect(status_boxR.center[0] - 120, status_boxR.center[1] // 2, 240, sblBody_Y)

greet = True
intro_play = True
intro = True

FINISH = False

showStatus = False

creditAlpha = 0     # For Credit
fadeIn = True
fadeOut = False
pauseTimer = pygame.time.get_ticks()
Box_x = 400
Box_y = 80
text_box = pygame.Rect(box_x := Window_Width//2 - Box_x//1.35, box_y := Window_Height//1.5 - Box_y//2, Box_x, Box_y)
ok_box = pygame.Rect(ok_x := Window_Width//2 + 140, ok_y := Window_Height//1.5 - Box_y//2, 160, Box_y)
tbActive = False
text_color_passive = (204, 204, 204)
tbColor = text_color_passive

sChange = False     # used for Transitions
audiomute = True   # mute's audio.. used for toggle
reset = False   # Resets player with the key 'R'

portal_fx = True
death_fx = True

play_ambiance = False
stop_ambiance = False

volume = 0.1

# Creates a display

if fs:
    flags = HWSURFACE | DOUBLEBUF | FULLSCREEN
else:
    flags = HWSURFACE

screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 32, vsync=True)  # Size, flags, Color, verticalSy

icon = pygame.image.load("assets/images/Koffee.png").convert_alpha()

pygame.display.set_icon(icon)

#  LOADING SYSTEM

Actual = pygame.time.get_ticks()
endWait = pygame.time.get_ticks()

mainloop = True

notice = font_calibriS.render(
            "Name must be at least 3 char long.", True, White)
notice1 = font_calibriS.render(
            "You can leave this blank if you want", True, White)
notice2 = font_calibriS.render(
            "to. But you CAN NOT change it later.", True, White)

notice2.convert_alpha()
notice1.convert_alpha()
notice.convert_alpha()

notice.set_alpha(100)
notice1.set_alpha(100)
notice2.set_alpha(100)


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


def text_to_screen(x, y, text, font, color=(255, 255, 255), alpha=255):
    """
    :param x: position of text in x-axis
    :param y: position of text in y-axis
    :param text: should be string
    :param font: choose font
    :param color: choose color must provide a rgb value or tuple containing one
    :param alpha: opacity of text
    :return: no return
    """
    img_font = font.render(text, True, color)
    img_font.convert_alpha()
    img_font.set_alpha(alpha)
    screen.blit(img_font, (x, y))


def event_handler():            # All Event handling here

    global move_right, move_left, debug, grid, flags, reset, WIN, coffee, coin, mainloop, showStatus, goffee, goffee_img

    WIN = PlayerBluePrint.WIN

    coffee = PlayerBluePrint.kPoints
    coin = PlayerBluePrint.cPoints
    goffee = PlayerBluePrint.gPoint

    # Handling Animation
    if Knight.Alive and not FINISH:

        if Knight.above_ground:
            Player.change_action(Knight, new_action=2)  # 2 = jump
        elif (move_right or move_left) and not Knight.above_ground and Knight.current_vel[0] != 0:
            Player.change_action(Knight, new_action=1)  # 1 = run
        else:
            Player.change_action(Knight, new_action=0)  # 0 = idle
    if not Knight.Alive:
        Player.change_action(Knight, new_action=3)
    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            IO.start([score, coin, coffee, timePlayed])
            mainloop = False
        if event.type == KEYDOWN and goffee <= 0:  # Triggered when key is pressed down
            if event.key == K_a:
                move_left = True
            elif event.key == K_d:
                move_right = True
            if event.key == K_SPACE:
                if not Knight.above_ground:
                    jump_sfx.play()
                Knight.isJump = True
            if event.key == K_r:
                if not MainMenu and Knight.Alive:
                    reset = True

            if event.key == K_TAB:
                if not MainMenu:
                    if not debug:
                        grid = False
                        debug = True
                    else:
                        debug = False

            if event.key == K_LCTRL:
                if not MainMenu:
                    if not grid:
                        debug = False
                        grid = True
                    else:
                        grid = False

            if event.key == K_q:
                if MainMenu:
                    showStatus = not showStatus

        if event.type == KEYUP and not FINISH:  # Released when key is released
            if event.key == K_a:
                move_left = False

            elif event.key == K_d:
                move_right = False

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) and not FINISH:
            if MainMenu:
                if status_boxL.collidepoint(event.pos) or status_boxR.collidepoint(event.pos):
                    showStatus = not showStatus


debugWindow_X = 1
debug_Animation_Timer = pygame.time.get_ticks()
Transition = 0
blackout_Timer = pygame.time.get_ticks()


def renderer():                 # All graphics here

    global debugWindow_X, Transition, blackout_Timer, MainMenu, audiomute, reset, current_level, WIN, portal_fx,\
        death_fx, volume, play_ambiance, stop_ambiance, score, timePlayed, dataIN, startDumping, scoreH, coinS,\
        coffeeS, Actual, endWait, FINISH, startChecking, move_left, move_right

    screen.fill(Cyan)

    coin_group.draw(screen)
    coin_group.update()

    koffee_group.draw(screen)
    koffee_group.update()

    gate_group.draw(screen)
    gate_group.update()

    goffee_group.draw(screen)
    goffee_group.update()

    if goffee > 0:
        if goffee_img.get_alpha() < 200:
            endWait = pygame.time.get_ticks()
            goffee_img.set_alpha(255)
        move_right = False
        move_left = False
        if pygame.time.get_ticks() - endWait >= 4000:
            WIN = True
            MainMenu = False

    Knight.draw(screen)

    if Knight.Alive:
        Knight.mov(move_left, move_right, level)
        score = coin * (coffee + 1)
        if pygame.time.get_ticks() - Actual >= 1000:
            Actual = pygame.time.get_ticks()
            timePlayed += 1    # saves time played by the user

    Knight.update()
    level.draw(screen)

    slime_group.draw(screen)
    slime_group.update()

    killable_blocks_group.draw(screen)
    killable_blocks_group.update()

    pygame.mixer.music.set_volume(volume)

    text_to_screen(1200, 25, f"X {str(coin)}", font_calibri, White)
    screen.blit(coin_img, (1160, 22))
    text_to_screen(1200, 60, f"X {str(coffee)}", font_calibri, White)
    screen.blit(koffee_img, (1160, 57))

    # Use this in the next update

    """pygame.draw.rect(screen, (115, 62, 57), rect_bar)
    pygame.draw.rect(screen, (228, 166, 114), rect_bar, 2)
    pygame.draw.rect(screen, (162, 38, 51), rect_gK)
    pygame.draw.rect(screen, (228, 166, 114), rect_gK, 2)

    pygame.draw.rect(screen, (184, 111, 80), rectHP)
    pygame.draw.rect(screen, (228, 166, 114), rectHP, 2)

    pygame.draw.rect(screen, (184, 111, 80), rect_cK)
    pygame.draw.rect(screen, (228, 166, 114), rect_cK, 2)

    screen.blit(goffee_img,
                (rect_bar.center[0] - goffee_img.get_width() // 2, rect_bar.center[1] - goffee_img.get_height() // 2))
                """
    screen.blit(goffee_img,
                (1100, 20))

    if Knight.Alive:
        death_fx = True

        if reset and not FINISH:
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
            if portal_fx and not FINISH:
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
                if goffee == 1:
                    FINISH = True
                portal_fx = True
                cleanup()
                Knight.reset("player", 3, 150, 300, .9, 3)

        else:
            if pygame.time.get_ticks() - blackout_Timer > 10:
                blackout_Timer = pygame.time.get_ticks()
                Transition -= 0.5
                Transition *= 0.96
                if Transition <= 0:
                    Transition = 0
                volume += 0.0001
                volume *= 1.01
                if volume >= 0.1:
                    volume = 0.1

            main_bg1.set_alpha(Transition)
            screen.blit(main_bg1, (0, 0))

    elif not Knight.Alive and not MainMenu and not FINISH:
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
                start_sfx.play()
                Knight.reset("player", 3, 150, 300, .9, 3)
                Knight.Alive = True

            elif menu_btn.draw(screen) and not MainMenu:
                if startDumping:
                    startDumping = False
                    dataIN = IO.start([score, coin, coffee, timePlayed])
                    scoreH = dataIN[0]
                    coinS = dataIN[1]
                    coffeeS = dataIN[2]
                    timePlayed = dataIN[3]
                deselect_sfx.play()
                MainMenu = True
                Knight.reset("player", 3, 150, 300, .9, 3)
                Knight.Alive = False
                startDumping = True

                Transition = 0

            if audio_btn1.draw(screen):
                audiomute = not audiomute
                if audiomute:
                    deselect_sfx.play()
                    pygame.mixer.music.stop()
                else:
                    select_sfx.play()
                    pygame.mixer.music.play(-1, 0.0, 1000)

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
    if not FINISH:
        screen.blit(update_fps(), (10, 3))     # Must be at last :)

    pygame.display.update()
    return Knight.Alive


def greetings():
    global Transition, blackout_Timer, MainMenu, intro, fadeIn, fadeOut, creditAlpha, greet, mainloop, USER, tbActive,\
        tbColor, intro_play, showStatus, scoreH, coinS, coffeeS, dataIN, timePlayed

    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            mainloop = False

        if not intro:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if text_box.collidepoint(event.pos):
                    select_sfx.play()
                    tbActive = True
                else:
                    deselect_sfx.play()
                    tbActive = False
                if ok_box.collidepoint(event.pos) and (len(USER) > 2 or len(USER) == 0):

                    intro_sfx.fadeout(1000)
                    deselect_sfx.stop()
                    select_sfx.play()
                    greet = False

                    MainMenu = True
                    if USER == "":
                        USER = "Anonymous"
                    IO.init(USER)
                    dataIN = IO.start([score, coin, coffee, timePlayed])
                    scoreH = dataIN[0]
                    coinS = dataIN[1]
                    coffeeS = dataIN[2]
                    timePlayed = dataIN[3]
                    showStatus = True

                else:
                    tbColor = (255, 0, 0)
            if tbActive:
                if event.type == KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        USER = USER[:-1]
                    elif event.key == pygame.K_TAB:
                        print("210030")
                    elif event.key == pygame.K_SPACE:
                        pass
                    elif event.key == pygame.K_RETURN:

                        intro_sfx.fadeout(1000)
                        deselect_sfx.stop()
                        select_sfx.play()
                        greet = False

                        MainMenu = True
                        if USER == "":
                            USER = "Anonymous"
                        IO.init(USER)
                        dataIN = IO.start([score, coin, coffee, timePlayed])
                        scoreH = dataIN[0]
                        coinS = dataIN[1]
                        coffeeS = dataIN[2]
                        timePlayed = dataIN[3]
                        showStatus = True

                    elif not len(USER) > 9:
                        USER += event.unicode

    if intro:
        screen.fill(Black)
        main_bg1.set_alpha(Transition)
        screen.blit(main_bg1, (0, 0))
        credit.set_alpha(creditAlpha)
        screen.blit(credit,
                    (Window_Width // 2 - credit.get_width() // 2, Window_Height // 2 - credit.get_height() // 2))
        if fadeIn:
            if pygame.time.get_ticks() - blackout_Timer > 10:
                blackout_Timer = pygame.time.get_ticks()
                Transition += 5
                Transition *= 1.01
                if Transition >= 255:
                    Transition = 255
                if intro_play:
                    intro_play = False
                    intro_sfx.play()
                if Transition == 255:
                    creditAlpha += 1
                    creditAlpha *= 1.05

                    if pygame.time.get_ticks() - pauseTimer >= 5000:
                        fadeIn = False
                        intro = False

    else:
        screen.fill(Cyan)
        Transition = 0

        ask0 = font_calibri0.render(f"HI THERE!", True, White)
        ask = font_calibri0.render("What's your name? :)", True, White)

        USER = USER.capitalize()
        text_area = font_calibri0.render(USER, True, tbColor)

        ok_area = font_calibri0.render("SKIP", True, (234, 212, 170))

        if 2 >= len(USER) > 0:
            ok_area = font_calibri0.render("NO !", True, (234, 212, 170))
        if len(USER) > 2:
            ok_area = font_calibri0.render("SAVE", True, (234, 212, 170))

        pygame.draw.rect(screen, (184, 111, 80), text_box)
        pygame.draw.rect(screen, tbColor, text_box, 5)

        pygame.draw.rect(screen, (184, 111, 80), ok_box)
        pygame.draw.rect(screen, (234, 212, 170), ok_box, 5)
        screen.blit(text_area, (box_x + Box_x // 8 + 3, box_y + Box_y // 3 - 10))

        if USER == "":
            screen.blit(notice, (box_x + 15, box_y + Box_y // 3 - 15))
            screen.blit(notice1, (box_x + 15, box_y + Box_y // 3 + 5))
            screen.blit(notice2, (box_x + 15, box_y + Box_y // 3 + 25))

        screen.blit(ask0, (box_x + 180, box_y - 200 + math.sin(time.time()*5)*5 - 25))
        screen.blit(ask, (box_x + 30, box_y - 120))

        screen.blit(ok_area, (ok_x + 20, ok_y + 18))

    if tbActive:
        tbColor = White
    else:
        tbColor = text_color_passive

    pygame.display.update()


def finish():

    global MainMenu, mainloop, dataIN, startChecking,\
        scoreH, coinS, coffeeS, timePlayed

    screen.fill(Cyan)

    if startChecking:
        startChecking = False
        dataIN = IO.start([score, coin, coffee, timePlayed])
        scoreH = dataIN[0]
        coinS = dataIN[1]
        coffeeS = dataIN[2]
        timePlayed = dataIN[3]

    ambiance.fadeout(1000)
    pygame.mixer.music.fadeout(1000)

    text_to_screen(
        Window_Width // 6 + 140, Window_Height // 2 - 100 + math.sin(time.time() * 5) * 5 - 25,
        "CONGRATS        ", font_calibri0, White, 200)
    text_to_screen(
        Window_Width // 4, Window_Height // 2 - 100 + math.sin(time.time() * 5) * 5 - 25,
        f"                    {USER} ", font_calibri0, (254, 231, 97), 200)
    text_to_screen(
        Window_Width // 5 - 45, Window_Height // 2 - math.sin(time.time() * 5) * 5 - 25,
        "YOU HAVE COMPLETED THE DEMO!", font_calibri0, White, 200)
    if exit_btn.draw(screen):
        IO.start([score, coin, coffee, timePlayed])
        mainloop = False


def main_menu():
    global Transition, blackout_Timer, MainMenu, sChange, mainloop, fs, audiomute, flags, screen, volume,\
        stop_ambiance, play_ambiance, sBoxYLevel, status_boxL, status_boxR, showStatus, sbl_topBoxL, sbl_topBoxR, \
        sbl_bodyBoxL, sbl_bodyBoxR, sblBody_Y, sbl_BodyColor, text_opacity, dataIN, startChecking,\
        scoreH, coinS, coffeeS, timePlayed
    if startChecking:
        startChecking = False
        dataIN = IO.start([score, coin, coffee, timePlayed])
        scoreH = dataIN[0]
        coinS = dataIN[1]
        coffeeS = dataIN[2]
        timePlayed = dataIN[3]
    screen.fill(Cyan)
    Knight.Alive = False

    ambiance.fadeout(1000)

    if fs:
        flags = HWSURFACE | DOUBLEBUF | FULLSCREEN
    else:
        flags = HWSURFACE

    screen.blit(logo, (
        Window_Width//2 - logo.get_width()//2,
        Window_Height//4 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))

    text_to_screen(
        Window_Width//2 - 69, Window_Height//2.5 - 16 + math.sin(time.time()*5)*5 - 25,
        "Stage: Alpha", font_calibri, White, 200)

    if exit_btn.draw(screen) and MainMenu:
        IO.start([score, coin, coffee, timePlayed])
        mainloop = False

    if fs_btn.draw(screen):
        fs = not fs
        if fs:
            deselect_sfx.play()
            screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync = True)
        else:
            select_sfx.play()
            screen = pygame.display.set_mode((Window_Width, Window_Height), flags, 8, vsync = True)

    if audio_btn.draw(screen):
        audiomute = not audiomute
        if audiomute:
            deselect_sfx.play()
            pygame.mixer.music.stop()
        else:
            select_sfx.play()
            pygame.mixer.music.play(-1, 0.0, 1000)

    if start_btn.draw(screen) and Transition == 0:
        start_sfx.play()
        play_ambiance = True
        sChange = True
        showStatus = False
    if sChange:
        if pygame.time.get_ticks() - blackout_Timer > 10:
            blackout_Timer = pygame.time.get_ticks()
            Transition += 1
            Transition *= 1.09

            if Transition >= 150:
                Transition = 150
                sChange = False
                MainMenu = False
                sBoxYLevel = -500
                Knight.Alive = True

    if exit_btn.draw(screen) and MainMenu:
        IO.start([score, coin, coffee, timePlayed])
        mainloop = False

    status_boxL = pygame.Rect(100, sBoxYLevel, sBox_X, sBox_Y)
    status_boxR = pygame.Rect(830, sBoxYLevel, sBox_X, sBox_Y)
    sbl_topBoxL = pygame.Rect(status_boxL.center[0] - 140, status_boxL.center[1] // 4, 280, 50)
    sbl_topBoxR = pygame.Rect(status_boxR.center[0] - 140, status_boxR.center[1] // 4, 280, 50)
    sbl_bodyBoxL = pygame.Rect(status_boxL.center[0] - 120, status_boxL.center[1] // 2, 240, sblBody_Y)
    sbl_bodyBoxR = pygame.Rect(status_boxR.center[0] - 120, status_boxR.center[1] // 2, 240, sblBody_Y)  # 350

    pygame.draw.rect(screen, (115, 62, 57), status_boxL)
    pygame.draw.rect(screen, (115, 62, 57), status_boxR)
    pygame.draw.rect(screen, (234, 212, 170), status_boxL, 5)
    pygame.draw.rect(screen, (234, 212, 170), status_boxR, 5)
    pygame.draw.rect(screen, (190, 74, 47), sbl_topBoxL)
    pygame.draw.rect(screen, (190, 74, 47), sbl_topBoxR)
    pygame.draw.rect(screen, (234, 212, 170), sbl_topBoxL, 3)
    pygame.draw.rect(screen, (234, 212, 170), sbl_topBoxR, 3)

    text_to_screen(sbl_topBoxL[0] + 100, sbl_topBoxL[1] + 13, "STATUS", font_calibri, White, 255)
    text_to_screen(sbl_topBoxR[0] + 100, sbl_topBoxR[1] + 13, "CREDIT", font_calibri, White, 255)

    pygame.draw.rect(screen, sbl_BodyColor, sbl_bodyBoxL)
    pygame.draw.rect(screen, sbl_BodyColor, sbl_bodyBoxR)
    pygame.draw.rect(screen, (234, 212, 170), sbl_bodyBoxL, 3)
    pygame.draw.rect(screen, (234, 212, 170), sbl_bodyBoxR, 3)

    #   Greetings
    text_to_screen(
        sbl_bodyBoxL[0] + 35, sbl_bodyBoxL[1] + 13, "Welcome back!", font_calibri, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxL[0] + 35, sbl_bodyBoxL[1] + 35, f" {USER}", font_calibri, (254, 231, 97), text_opacity)

    #   Status display
    text_to_screen(
        sbl_bodyBoxL[0] + 20, sbl_bodyBoxL[1] + 80, f"Score: {score}", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxL[0] + 20, sbl_bodyBoxL[1] + 100,
                   f"High score: {scoreH}", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(
        sbl_bodyBoxL[0] + 20, sbl_bodyBoxL[1] + 120, f"Coin: {coinS}", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(
        sbl_bodyBoxL[0] + 20, sbl_bodyBoxL[1] + 140, f"Koffee: {coffeeS}", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxL[0] + 20, sbl_bodyBoxL[1] + 160,
                   f"Time played: {(timePlayed//60)} min", font_calibriS, (234, 212, 170), text_opacity)

    #   Credit
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 30,
                   "Game design:Anurag", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 50,
                   "Sound design:Anurag", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 70,
                   "Asset design:Anurag", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 90,
                   "Level Design:Anurag", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 130,
                   "Made by", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 130,
                   "             Anurag", font_calibriS, (254, 231, 97), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 160,
                   "Contacts:", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 180,
                   "  - Facebook:", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 200,
                   "    Anurag Bharati", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 220,
                   "  - Instagram:", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 240,
                   "    @gen.fro", font_calibriS, (234, 212, 170), text_opacity)
    text_to_screen(sbl_bodyBoxR[0] + 20, sbl_bodyBoxR[1] + 280,
                   f"Version - {VERSION}", font_calibriS, White, text_opacity//2)

    if showStatus:
        sbl_BodyColor = (194, 133, 105)
        sBoxYLevel += 0.5
        sBoxYLevel *= 0.959
        sblBody_Y += 0.1
        sblBody_Y *= 1.049
        if sblBody_Y >= 350:
            sblBody_Y = 350
            text_opacity += 1
            text_opacity *= 1.099
            if text_opacity >= 255:
                text_opacity = 255

        if sBoxYLevel >= -10:
            sBoxYLevel = -10
    if not showStatus:
        sbl_BodyColor = (162, 38, 51)
        text_opacity -= 0.69
        text_opacity *= 0.69
        if text_opacity <= 1:
            text_opacity = 0
            if sBoxYLevel >= -499:
                sBoxYLevel -= 1
                sBoxYLevel *= 1.2
            elif sBoxYLevel <= -500:
                sBoxYLevel = -500

    main_bg1.set_alpha(Transition)
    screen.blit(main_bg1, (0, 0))

    pygame.display.update()

    return flags


def cleanup():
    global WIN, level, level_data, pickle_opn, current_level

    WIN = False

    if not FINISH and goffee != 1:
        current_level += 1

        if os.path.exists(f"assets/levels/level{current_level}.dat"):
            slime_group.empty()
            killable_blocks_group.empty()
            gate_group.empty()
            coin_group.empty()
            koffee_group.empty()
            with open(f"assets/levels/level{current_level}.dat", "rb") as pickle_opn:
                level_data = pickle.load(pickle_opn)
            level = Earth(level_data)
    if FINISH and goffee == 1:
        finish()


credit = pygame.image.load("assets/images/credit.png").convert_alpha()
credit = pygame.transform.scale(credit, (credit.get_width()//4, credit.get_height()//4))
intro_sfx = pygame.mixer.Sound("assets/audio/sfx/intro.mp3")
intro_sfx.set_volume(0.5)

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

coin_img = pygame.image.load("assets/images/tiles/claimable/coin/0.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (int(coin_img.get_width()*0.75), int(coin_img.get_height()*0.75)))
koffee_img = pygame.image.load("assets/images/tiles/claimable/koffee/5.png").convert_alpha()
koffee_img = pygame.transform.scale(koffee_img, (int(koffee_img.get_width()*0.8), int(koffee_img.get_height()*0.8)))

goffee_img = pygame.image.load("assets/images/tiles/claimable/goffee/5.png")
goffee_img = pygame.transform.scale(goffee_img, (int(goffee_img.get_width()*1.2), int(goffee_img.get_height()*1.2)))
goffee_img.convert_alpha()
goffee_img.set_alpha(25)

rect_gK = goffee_img.get_rect()
rectHP = goffee_img.get_rect()
rect_cK = goffee_img.get_rect()

rect_gK.x, rect_gK.y = (rect_bar.center[0] - goffee_img.get_width() // 2 - 20,
                        rect_bar.center[1] - goffee_img.get_height() // 2 - 12)
rect_gK.width, rect_gK.height = 80, 60

rectHP.x, rectHP.y = (rect_bar.center[0] - goffee_img.get_width() // 2 - 170,
                      rect_bar.center[1] - goffee_img.get_height() // 2 - 12)
rectHP.width, rectHP.height = 120, 60

rect_cK.x, rect_cK.y = (rect_bar.center[0] - goffee_img.get_width() // 2 + 90,
                        rect_bar.center[1] - goffee_img.get_height() // 2 - 12)
rect_cK.width, rect_cK.height = 120, 60


pygame.mixer.music.load("assets/audio/Koffee_ost.mp3")
pygame.mixer.music.set_volume(volume)

ambiance = pygame.mixer.Sound("assets/audio/Ambiance.mp3")
ambiance.set_volume(2)

portal_sfx = pygame.mixer.Sound("assets/audio/sfx/portal.wav")
portal_sfx.set_volume(0.6)

Knight = Player("player", 3, 150, 300, .9, 3)

jump_sfx = pygame.mixer.Sound("assets/audio/sfx/knight_jump.wav")
jump_sfx.set_volume(0.40)


death_sfx = pygame.mixer.Sound("assets/audio/sfx/knight_dead.wav")
death_sfx.set_volume(0.5)

start_sfx = pygame.mixer.Sound("assets/audio/sfx/start_sfx.wav")
start_sfx.set_volume(0.1)

deselect_sfx = pygame.mixer.Sound("assets/audio/sfx/deselect.wav")
deselect_sfx.set_volume(0.1)
select_sfx = pygame.mixer.Sound("assets/audio/sfx/select.wav")
select_sfx.set_volume(0.1)

if os.path.exists(f"assets/levels/level{current_level}.dat"):
    pickle_opn = open(f"assets/levels/level{current_level}.dat", "rb")
    level_data = pickle.load(pickle_opn)
    level = Earth(level_data)
    pickle_opn.close()

start_btn = Button(
    Window_Width//2 - start_button.get_width()//4,
    Window_Height//2 - start_button.get_height()//4, start_button, .5)

exit_btn = Button(
    Window_Width//2 - exit_button.get_width()//4,
    Window_Height//2 + exit_button.get_height()//1.5, exit_button, .5)

fs_btn = Button(
    Window_Width//2 - fs_button.get_width()//3,
    Window_Height//2 + fs_button.get_height()//3.2, fs_button, .3)

audio_btn = Button(
    Window_Width // 2 + audio_button.get_width() // 12 - audio_button.get_width() // 24,
    Window_Height // 2 + audio_button.get_height() // 3.2, audio_button, .3)


restart_btn = Button(
    Window_Width // 2 - restart_button.get_width() // 4,
    Window_Height // 2 - restart_button.get_height() // 4, restart_button, .5)
menu_btn = Button(
    Window_Width//1.21,
    Window_Height//1.25, menu_button, .35)

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

    screen.blit(debugNote, (10, 420))
    screen.blit(debugNote0, (10, 440))
    screen.blit(debugNote1, (10, 460))
    screen.blit(debugNote2, (10, 480))

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

game_info = font_consolas.render(f"version {VERSION} | Dev(fe/be):210030", True, White)

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

        if not greet:
            event_handler()

        if greet:
            greetings()

        if MainMenu and not greet and not FINISH:
            main_menu()

        if not MainMenu and not greet:
            renderer()

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

else:
    mainloop = True
