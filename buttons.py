import pygame


class Button:

    def __init__(self, x, y, image, scale):
        self.image = image
        self.scale = scale
        self.image = pygame.transform.scale(
            self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pressed = False

    def draw(self, Where):
        action = False

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed(3)[0] == 1 and not self.pressed and not action:
                self.pressed = True
                action = True
            if pygame.mouse.get_pressed(3)[0] == 0:
                action = False
                self.pressed = False

        Where.blit(self.image, self.rect)

        return action
