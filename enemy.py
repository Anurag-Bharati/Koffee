# All hostile blueprint here
import random

import pygame
import os


class Enemy(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, velocity, enemy_scale):
        pygame.sprite.Sprite.__init__(self)  # Calling SuperClass to inherit form Sprite
        self.animation_index = 0
        self.animation_list = []
        self.velocity = velocity
        self.update_time = pygame.time.get_ticks()
        self.ANIMATION_TIMER = 50
        self.enemy_scale = enemy_scale
        self.MOVE_TIMER = 1000
        self.move_unit = 0
        self.update_mov = pygame.time.get_ticks()

        """self.image = pygame.image.load("assets/images/enemy/slime/0.png").convert_alpha()
        self.rect = self.image.get_rect()  # Creating a for self
        self.rect.x = xPos
        self.rect.y = yPos"""

        os_count_frame = len(os.listdir(f"assets/images/enemy/slime"))
        for i in range(os_count_frame):
            enemy_img = pygame.image.load(f'assets/images/enemy/slime/{i}.png')
            enemy_img = pygame.transform.scale(enemy_img,  # SCALING happens here
                                               (int(enemy_img.get_width() * self.enemy_scale),
                                                int(enemy_img.get_height() * self.enemy_scale)))
            enemy_img.convert_alpha()
            self.animation_list.append(enemy_img)
        self.image = self.animation_list[self.animation_index]
        self.rect = self.image.get_rect()  # Creating a for self
        self.rect.center = (xPos, yPos)
        self.rect.x = xPos
        self.rect.y = yPos

    def update(self):  # Changing index with respect to timer happens here # Updating the slime group

        self.image = self.animation_list[self.animation_index]  # updating the previous index

        if pygame.time.get_ticks() - self.update_time > self.ANIMATION_TIMER:  # updating
            self.update_time = pygame.time.get_ticks()  # resets the update_time
            self.animation_index += 1  # increase the animation index
            if self.animation_index >= len(self.animation_list)-1:  # to prevent overflow
                self.animation_index = 0

        if pygame.time.get_ticks() - self.update_mov > (x := self.MOVE_TIMER + random.randint(-500, 500)):

            self.rect.x += self.velocity
            self.move_unit += 1
            if abs(self.move_unit) > 50:
                self.move_unit *= -1
                self.velocity *= -1
                self.update_mov = pygame.time.get_ticks()







