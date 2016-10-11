import pygame
from wallClass import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self, parent):
        super().__init__()

        # Pick the direction from which it is fired
        self.direction = parent.direction

        # Create a graphical object
        self.image = pygame.Surface([15, 15])
        self.image.fill([255, 0, 0])
        self.rect = self.image.get_rect()

        # Set it to the right place
        self.rect.x = parent.rect.x
        self.rect.y = parent.rect.y

        # Make sure it GOES to the right place when moving
        self.transform = [0, 0]
        if parent.direction ==  0:
            self.transform = [0, -5]
        elif parent.direction == 1:
            self.transform = [-5, 0]
        elif parent.direction == 2:
            self.transform = [0, 5]
        elif parent.direction == 3:
            self.transform = [5, 0]


    # Where it moves each frame tick
    def update(self):
        self.rect.x += self.transform[0]
        self.rect.y += self.transform[1]