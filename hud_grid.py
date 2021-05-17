import pygame

grid_size_x = 32
grid_size_y = 30


def draw_grid(Where, Color, Screen_width, Screen_height, Font):
    for line in range(0, 25):
        pygame.draw.line(Where, Color, (0, line * grid_size_y), (Screen_width, line * grid_size_y))
        if line == 0 or line == 24:
            continue
        num = Font.render(str(line), True, Color)
        Where.blit(num, ((grid_size_x//4, line * grid_size_y + grid_size_y//4), (Screen_width, line * grid_size_y)))

    for line in range(0, 41):
        pygame.draw.line(Where, Color, (line * grid_size_x, 0), (line * grid_size_x, Screen_height))
        if line == 0 or line == 40:
            continue
        num = Font.render(str(line), True, Color)
        Where.blit(num, ((line * grid_size_x + grid_size_x//4, grid_size_y//4), (line * grid_size_x, Screen_height)))

