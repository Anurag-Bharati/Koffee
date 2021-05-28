import pygame


class Gate(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, blockScaleX, blockScaleY):
        pygame.sprite.Sprite.__init__(self)  # Calling SuperClass to inherit form Sprite
        self.blockScaleX = blockScaleX
        self.blockScaleY = blockScaleY
        gate = pygame.image.load("assets/images/tiles/gate.png").convert_alpha()
        gate = pygame.transform.scale(gate,  # SCALING happens here
                                      (int(gate.get_width() * self.blockScaleX),
                                       int(gate.get_height() * self.blockScaleY)))
        self.image = gate
        self.rect = self.image.get_rect()  # Creating a for self
        self.rect.center = (xPos, yPos)
        self.rect.x = xPos
        self.rect.y = yPos
