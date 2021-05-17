import pygame
from main import screen, White, Window_Width, Window_Height, font_consolas

grid_size_x = 32
grid_size_y = 30


def draw_grid():
    for line in range(0, 25):
        pygame.draw.line(screen, White, (0, line * grid_size_y), (Window_Width, line * grid_size_y))
        if line == 0 or line == 24:
            continue
        num = font_consolas.render(str(line), True, White)
        screen.blit(num, ((grid_size_x//4, line * grid_size_y + grid_size_y//4), (Window_Width, line * grid_size_y)))

    for line in range(0, 41):
        pygame.draw.line(screen, White, (line * grid_size_x, 0), (line * grid_size_x, Window_Height))
        if line == 0 or line == 40:
            continue
        num = font_consolas.render(str(line), True, White)
        screen.blit(num, ((line * grid_size_x + grid_size_x//4, grid_size_y//4), (line * grid_size_x, Window_Height)))

