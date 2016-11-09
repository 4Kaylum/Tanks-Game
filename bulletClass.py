import pygame
from wallClass import *
from gameConstants import *
from math import sin, cos, radians, fabs

class Bullet(pygame.sprite.Sprite):

    def __init__(self, parent):
        super().__init__()

        # Pick the direction from which it is fired
        self.rotation = parent.rotation

        # Create a graphical object
        self.image = pygame.Surface([5, 5])
        self.image.fill([255, 0, 0])
        self.rect = self.image.get_rect()

        # Set it to the right place
        self.rect.center = parent.rect.center

        # Make sure it GOES to the right place when moving
        self.transform = 0
        self.anglePosChange()

        # Make the bullets despawn if health > 5000 or if bounced twice
        self.lifetime = bulletLifetimeTimeout
        self.health = bulletHealthStartup
        self.deleteFlag = False


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

        X_c = multiplier[0] * forwardMultiplier * bulletMovementAmount * sin(radians(r_raw))
        Y_c = multiplier[1] * forwardMultiplier * bulletMovementAmount * cos(radians(r_raw))

        self.transform = [X_c, Y_c]


    # Where it moves each frame tick
    def update(self):
        # self.rect.x += self.transform[0]
        # self.rect.y += self.transform[1]
        # self.checkCollide([self.transform[0], 0])
        # self.checkCollide([0, self.transform[1]])
        # self.checkCollide(self.transform)

        self.lifetime -= 1
        if self.health <= 0 or self.lifetime <= 0:
            self.deleteFlag = True

    # Move by an amount
    def moveBy(self, moveAmount):
        self.rect.x += moveAmount[0]
        self.rect.y += moveAmount[1]


    # Check collisions of walls
    def checkCollide(self, wallGroup):
        # Check what it's hit with - gives list of images
        moveAmount = self.transform
        self.moveBy([moveAmount[0], 0])
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        # Go through each one, find it's bound
        if len(hitList) > 0:
            self.transform[0] = self.transform[0] * -1
            self.moveBy([moveAmount[0], 0])
            self.health -= 1

        self.moveBy([0, moveAmount[1]])
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        if len(hitList) > 0:
            self.transform[1] = self.transform[1] * -1
            self.moveBy([0, moveAmount[1]])
            self.health -= 1

