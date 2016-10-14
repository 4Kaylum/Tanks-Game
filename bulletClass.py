import pygame
from wallClass import *
from gameConstants import *
import math

class Bullet(pygame.sprite.Sprite):

    def __init__(self, parent):
        super().__init__()

        # Pick the direction from which it is fired
        self.rotation = parent.rotation

        # Create a graphical object
        self.image = pygame.Surface([15, 15])
        self.image.fill([255, 0, 0])
        self.rect = self.image.get_rect()

        # Set it to the right place
        self.rect.x = parent.rect.x
        self.rect.y = parent.rect.y

        # Make sure it GOES to the right place when moving
        self.transform = self.anglePosChange()


    # Where it moves each frame tick
    def update(self):
        self.rect.x += self.transform[0]
        self.rect.y += self.transform[1]

    # Copied the code from player to work out direction
    def anglePosChange(self,forward=True):
        r_raw = self.rotation

        # decreasing x decreasing y
        if r_raw >= 0 and r_raw < 90:
            multiplier = [-1,-1]
        # decreasing x increasing y
        elif r_raw >= 90 and r_raw < 180:
            multiplier = [-1,-1]         
        # increasing x increasing y
        elif r_raw >= 180 and r_raw < 270:
            multiplier = [1,1]
            r_raw -= 180
        # increasing x decreasing y
        else:
            multiplier = [-1,-1]


        r_y = r_raw - ( r_raw // 90 )
        r_x = 90 - r_y
        forwardMultiplier = {True:1,False:-1}[forward]

        X_c = multiplier[0] * forwardMultiplier * bulletMovementAmount * math.sin(math.radians(r_raw))
        Y_c = multiplier[1] * forwardMultiplier * bulletMovementAmount * math.cos(math.radians(r_raw))

        return [X_c, Y_c]