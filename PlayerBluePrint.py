import pygame
import os

GRAVITY = 0.75


class Player(pygame.sprite.Sprite):

    def __init__(self, player_type, health, xPos, yPos, player_scale, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.debug_vel = 0, 0
        self.Alive = True
        self.health = health
        self.init_health = health
        self.player_type = player_type
        self.facing = 1
        self.flip = False
        self.velocity = velocity
        self.jump_vel = 0
        self.terminal_vel = 20   # Max y_vel while falling 20
        self.isJump = False
        self.above_ground = True
        self.animation_list = []  # Stores all the animations
        self.animation_index = 0  # used to change index and make an animation
        self.action = 0  # used to change action
        self.update_time = pygame.time.get_ticks()  # used to make timer

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

    def update(self):

        self.update_animation()
        self.check_alive()

    def mov(self, screen_width, move_left, move_right):  # htf its showing this? not a error skip.

        # Resets mov var
        dx = 0  # Created to assign the change
        dy = 0

        if move_left or move_right:         # Changing the animation timer for run animation
            self.ANIMATION_TIMER = 70

        else:
            self.ANIMATION_TIMER = 150

        if move_left and not self.rect.left <= 0:
            dx = -self.velocity  # sets vel
            self.flip = True
            self.facing = -1  # for flipping
        if move_right and not self.rect.right >= screen_width:
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

        # temp collision

        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.above_ground = False

        self.rect.x += dx
        self.rect.y += dy

        self.debug_vel = dx, dy

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.velocity = 0
            self.Alive = False
            self.change_action(2)

    def draw(self, Where):
        Where.blit(pygame.transform.flip(self.player_image, self.flip, False), self.rect)

    def update_animation(self):  # Changing index with respect to timer happens here

        self.player_image = self.animation_list[self.action][self.animation_index]  # updating the previous index

        if pygame.time.get_ticks() - self.update_time > self.ANIMATION_TIMER:  # updating
            self.update_time = pygame.time.get_ticks()  # resets the update_time
            self.animation_index += 1  # increase the animation index
            if self.animation_index >= len(self.animation_list[self.action]):  # to prevent overflow
                self.animation_index = 0

    def change_action(self, new_action):  # changes action

        if new_action != self.action:
            self.action = new_action

            self.animation_index = 0
            self.update_time = pygame.time.get_ticks()
