import pygame
from main import screen, White, Window_Width, Window_Height

grid_size_x = 32
grid_size_y = 30


def draw_grid():
    for line in range(0, 25):
        pygame.draw.line(screen, White, (0, line * grid_size_y), (Window_Width, line * grid_size_y))
    for line in range(0, 41):
        pygame.draw.line(screen, White, (line * grid_size_x, 0), (line * grid_size_x, Window_Height))

