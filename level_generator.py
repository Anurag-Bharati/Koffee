import pygame
import random


from enemy import Enemy
from not_standable import killBlock
from change_level import Gate

slime_group = pygame.sprite.Group()
killable_blocks_group = pygame.sprite.Group()
gate_group = pygame.sprite.Group()

grid_x = 32
grid_y = 30

show_colloidal = False

# For unittest

slime_quantity = 0


class Earth:

    def __init__(self, world_data):
        global slime_quantity

        self.tile_list = []

        grass = pygame.image.load("assets/images/tiles/fixed/1.png").convert_alpha()
        bed_rock = pygame.image.load("assets/images/tiles/fixed/5.png").convert_alpha()
        dirt = pygame.image.load("assets/images/tiles/fixed/2.png").convert_alpha()
        rock = pygame.image.load("assets/images/tiles/fixed/4.png").convert_alpha()
        stone = pygame.image.load("assets/images/tiles/fixed/3.png").convert_alpha()
        key_a = pygame.image.load("assets/images/tiles/fixed/-1.png").convert_alpha()
        key_d = pygame.image.load("assets/images/tiles/fixed/-2.png").convert_alpha()
        arrow = pygame.image.load("assets/images/tiles/fixed/-6.png").convert_alpha()
        half_space = pygame.image.load("assets/images/tiles/fixed/-5.png").convert_alpha()

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
                if tile == -1:
                    block = key_a
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == -2:
                    block = key_d
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == -5:
                    block = half_space
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == -10:
                    half_space1 = pygame.transform.flip(half_space, True, False)
                    block = half_space1
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == -6:
                    block = arrow
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == -12:
                    arrow_l = pygame.transform.flip(arrow, True, False)
                    block = arrow_l
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x + 7
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)
                if tile == -18:
                    arrow_u = pygame.transform.rotate(arrow, -90)
                    block = arrow_u
                    img_rect = block.get_rect()
                    img_rect.x = at_column * grid_x
                    img_rect.y = at_row * grid_y
                    tile = (block, img_rect)
                    self.tile_list.append(tile)

                if tile == 7:
                    slime = Enemy(at_column * grid_x, at_row*grid_y+5, random.choice([-1, 1]), .9)
                    slime_group.add(slime)
                    # For debug
                    slime_quantity += 1

                if tile == 9:
                    lava = killBlock("lava", at_column * grid_x, at_row*grid_y+16, 1, 0.5)
                    killable_blocks_group.add(lava)

                if tile == 10:
                    lava = killBlock("lavab", at_column * grid_x, at_row*grid_y, 1, 1)
                    killable_blocks_group.add(lava)

                if tile == 11:
                    spike = killBlock("spikeup", at_column * grid_x, at_row*grid_y+16, 1, 0.5)
                    killable_blocks_group.add(spike)

                if tile == 12:
                    spike = killBlock("spikedown", at_column * grid_x, at_row*grid_y, 1, 0.5)
                    killable_blocks_group.add(spike)

                if tile == 14:
                    spike = killBlock("watera", at_column * grid_x, at_row*grid_y+15, 1, 0.5)
                    killable_blocks_group.add(spike)

                if tile == 15:
                    spike = killBlock("waterb", at_column * grid_x, at_row*grid_y, 1, 1)
                    killable_blocks_group.add(spike)
                if tile == 69:
                    gate = Gate(at_column * grid_x, at_row * grid_y-18, 1, 1)
                    gate_group.add(gate)
                at_column += 1
            at_row += 1

    def draw(self, Where):

        for tile in self.tile_list:

            Where.blit(tile[0], tile[1])
            if show_colloidal:
                pygame.draw.rect(Where, (0, 150, 0), tile[1], 1)
