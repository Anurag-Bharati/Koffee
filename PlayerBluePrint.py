import pygame
import os
from level_generator import killable_blocks_group, slime_group


GRAVITY = 0.75
GAME_SCENE = 0


class Player(pygame.sprite.Sprite):

    def __init__(self, player_type, health, xPos, yPos, player_scale, velocity):
        pygame.sprite.Sprite.__init__(self)

        self.reset(player_type, health, xPos, yPos, player_scale, velocity)

    def reset(self, player_type, health, xPos, yPos, player_scale, velocity):

        global GAME_SCENE

        self.current_vel = 0, 0
        self.Alive = True
        self.health = health
        self.init_health = health
        self.player_type = player_type
        self.facing = 1
        self.flip = False
        self.velocity = velocity
        self.jump_vel = 0
        self.terminal_vel = 20  # Max y_vel while falling 20
        self.isJump = False
        self.above_ground = True
        self.animation_list = []  # Stores all the animations
        self.animation_index = 0  # used to change index and make an animation
        self.action = 0  # used to change action
        self.update_time = pygame.time.get_ticks()  # used to make timer

        self.startingtime = pygame.time.get_ticks()

        self.damage_cooldown = 0

        self.ANIMATION_TIMER = 125  # when to update (in ms)

        animation_types = ["idle", "run", "jump", "dead"]
        for animation in animation_types:

            animation_cache = []

            os_count_frame = len(os.listdir(f"assets/images/{self.player_type}/{animation}"))

            for i in range(os_count_frame):
                player_img = pygame.image.load(f'assets/images/{self.player_type}/{animation}/{i}.png')
                player_img = pygame.transform.scale(player_img,  # SCALING happens here
                                                    (int(player_img.get_width() * player_scale),
                                                     int(player_img.get_height() * player_scale)))
                player_img.convert_alpha()  # Optimizing
                animation_cache.append(player_img)
            self.animation_list.append(animation_cache)

        #       print(self.animation_list)
        self.player_image = self.animation_list[self.action][self.animation_index]
        self.rect = self.player_image.get_rect()  # Creating a for self
        self.rect.center = (xPos, yPos)  # setting the rect location to player's loc
        self.player_width = self.player_image.get_width()
        self.player_height = self.player_image.get_height()

    def update(self):

        self.update_animation()
        self.check_alive()

    def mov(self, move_left, move_right, What):  # htf its showing this? not a error skip.

        global GAME_SCENE

        # Resets mov var
        dx = 0  # Created to assign the change
        dy = 0

        if (move_left or move_right) and self.current_vel[0] != 0:      # Changing the animation timer for run animation
            self.ANIMATION_TIMER = 70

        else:
            self.ANIMATION_TIMER = 150

        if move_left or move_right and self.Alive:
            if move_left:
                dx = -self.velocity  # sets vel
                self.flip = True
                self.facing = -1  # for flipping
            if move_right:
                dx = self.velocity
                self.flip = False
                self.facing = 1  # for flipping

        if self.isJump and not self.above_ground:
            self.jump_vel = -12
            self.isJump = False
            self.above_ground = True

        self.jump_vel += GRAVITY                                    # applying gravity

        if self.jump_vel > self.terminal_vel:
            self.jump_vel = self.terminal_vel

        dy += self.jump_vel

        for tile in What.tile_list:                           # New collision system - Checks before updating

            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.player_width, self.player_height):
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.player_width, self.player_height):
                if self.jump_vel < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.jump_vel = 0

                elif self.jump_vel >= 1:
                    dy = tile[1].top - self.rect.bottom
                    self.jump_vel = 0
                    self.above_ground = False

        if pygame.sprite.spritecollide(self, killable_blocks_group, False) \
                and (pygame.time.get_ticks() - self.startingtime > self.damage_cooldown):
            self.startingtime = pygame.time.get_ticks()
            self.health -= 1
            self.isJump = True
            self.damage_cooldown = 3000
            if self.health >= 4:
                self.animation_list[0][0].set_alpha(220)
            if 2 <= self.health < 4:
                self.animation_list[0][0].set_alpha(150)
            if self.health < 2:
                self.animation_list[0][2].set_alpha(80)
            print(self.health)

        if pygame.sprite.spritecollide(self, slime_group, False) \
                and (pygame.time.get_ticks() - self.startingtime > self.damage_cooldown):
            self.startingtime = pygame.time.get_ticks()
            self.health -= 1

            self.isJump = True

            self.damage_cooldown = 2000

            if self.health == 2:
                self.animation_list[0][0].set_alpha(220)
            if self.health <= 1:
                self.animation_list[0][0].set_alpha(80)
                self.animation_list[0][2].set_alpha(80)



        """if self.rect.bottom + dy > 480:          # Old collision system
            dy = 480 - self.rect.bottom
            self.above_ground = False"""

        self.rect.x += dx
        self.rect.y += dy

        self.current_vel = dx, dy

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.velocity = 0
            self.Alive = False
            self.change_action(3)

    def draw(self, Where):
        Where.blit(pygame.transform.flip(self.player_image, self.flip, False), self.rect)

    def update_animation(self):  # Changing index with respect to timer happens here

        self.player_image = self.animation_list[self.action][self.animation_index]  # updating the previous index

        if pygame.time.get_ticks() - self.update_time > self.ANIMATION_TIMER:  # updating
            self.update_time = pygame.time.get_ticks()  # resets the update_time
            self.animation_index += 1  # increase the animation index
            if self.animation_index >= len(self.animation_list[self.action]):  # to prevent overflow
                if self.action == 3:
                    self.animation_index = len(self.animation_list[self.action]) -1
                else:
                    self.animation_index = 0

    def change_action(self, new_action):  # changes action

        if new_action != self.action:
            self.action = new_action

            self.animation_index = 0
            self.update_time = pygame.time.get_ticks()
