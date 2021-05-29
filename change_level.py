import pygame
import os


class Gate(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, blockScaleX, blockScaleY):
        pygame.sprite.Sprite.__init__(self)  # Calling SuperClass to inherit form Sprite
        self.animation_index = 0
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.ANIMATION_TIMER = 80
        self.blockScaleX = blockScaleX
        self.blockScaleY = blockScaleY

        os_count_frame = len(os.listdir(f"assets/images/tiles/exit"))
        for i in range(os_count_frame):
            block_img = pygame.image.load(f'assets/images/tiles/exit/{i}.png')
            block_img = pygame.transform.scale(block_img,  # SCALING happens here
                                               (int(block_img.get_width() * self.blockScaleX),
                                                int(block_img.get_height() * self.blockScaleY)))
            block_img.convert_alpha()
            block_img.set_colorkey((24, 20, 37))
            self.animation_list.append(block_img)
        self.image = self.animation_list[self.animation_index]
        self.rect = self.image.get_rect()  # Creating a for self
        self.rect.center = (xPos, yPos)
        self.rect.x = xPos
        self.rect.y = yPos

    def update(self):  # Changing index with respect to timer happens here # Updating

        self.image = self.animation_list[self.animation_index]  # updating the previous index

        if pygame.time.get_ticks() - self.update_time > self.ANIMATION_TIMER:  # updating
            self.update_time = pygame.time.get_ticks()  # resets the update_time
            self.animation_index += 1  # increase the animation index
            if self.animation_index >= len(self.animation_list)-1:  # to prevent overflow
                self.animation_index = 0
