import pygame
import random

import main
import enemy

slime_group = pygame.sprite.Group()

grid_x = 32
grid_y = 30

show_colloidal = False


class Earth:

    def __init__(self, world_data):

        self.tile_list = []

        grass = pygame.image.load("assets/images/tiles/fixed/1.png").convert_alpha()
        bed_rock = pygame.image.load("assets/images/tiles/fixed/5.png").convert_alpha()
        dirt = pygame.image.load("assets/images/tiles/fixed/2.png").convert_alpha()
        rock = pygame.image.load("assets/images/tiles/fixed/4.png").convert_alpha()
        stone = pygame.image.load("assets/images/tiles/fixed/3.png").convert_alpha()

        at_row = 0
        for row in world_data:
            at_column = 0
            for tile in row:
                if tile == 1:
                    block = pygame.transform.scale(bed_rock, (grid_x, grid_y))
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:

                    block = pygame.transform.scale(grass, (grid_x, grid_y))
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    dirt = pygame.transform.flip(dirt, bool(random.randint(0, 1)), bool(random.randint(0, 1)))
                    block = pygame.transform.scale(dirt, (grid_x, grid_y))
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    stone = pygame.transform.flip(stone, bool(random.randint(0, 1)), False)
                    block = pygame.transform.scale(stone, (grid_x, grid_y))
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    rock = pygame.transform.flip(rock, bool(random.randint(0, 1)), bool(random.randint(0, 1)))
                    block = pygame.transform.scale(rock, (grid_x, grid_y))
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)

                if tile == 7:
                    slime = enemy.Enemy(at_column * grid_x, at_row*grid_y, 1, 1)
                    slime_group.add(slime)
                at_column += 1
            at_row += 1

    def draw(self, Where):

        for tile in self.tile_list:

            Where.blit(tile[0], tile[1])
            if show_colloidal:
                pygame.draw.rect(main.screen, (0, 150, 0), tile[1], 1)
