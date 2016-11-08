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


    # Where it moves each frame tick
    def update(self):
        self.rect.x += self.transform[0]
        self.rect.y += self.transform[1]
        self.lifetime -= 1
        if self.health <= 0 or self.lifetime <= 0:
            self.deleteFlag = True


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

        self.transform = [X_c, Y_c]


    # Check collisions of walls
    def checkCollide(self, wallGroup):
        # Check what it's hit with - gives list of images
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        # Go through each one, find it's bound
        if len(hitList) > 0:

            # Bounce correctly
            if self.rotation in [0, 90, 180, 270, 360]:
                self.rotation += 180
            elif self.rotation < 90:
                self.rotation = 90 + self.rotation
            elif self.rotation <= 180:
                self.rotation = 180 + (self.rotation - 90)
            elif self.rotation <= 270:
                self.rotation = 270 + (self.rotation - 90)
            elif self.rotation <= 360:
                self.rotation = (self.rotation - 360) + 180
            
            # elif self.rotation < 90 and hitList[0].rect.x > self.rect.x: # Bullet hit left wall at r<90 deg angle
            #     self.rotation = self.rotation + 270
            # elif self.rotation < 90: # Bullet hit top wall at r<90 deg angle
            #     self.rotation = self.rotation + 90
            # elif self.rotation < 180 and hitList[0].rect.y < self.rect.y: # Bullet hit left wall at r<180 deg angle
            #     self.rotation = (self.rotation - 90) + 180
            # elif self.rotation < 180: # Bullet hit bottom wall at r<180 deg angle
            #     self.rotation = 90 - (90 - self.rotation)
            # elif self.rotation < 270 and hitList[0].rect.y < self.rect.y: # Bullet hit right wall at r<270 deg angle
            #     self.rotation = 180 - (self.rotation - 180)
            # elif self.rotation < 270: # Bullet hit bottom wall at r<270 deg angle
            #     self.rotation = self.rotation - 270
            # elif self.rotation < 360 and hitList[0].rect.x < self.rect.x: # Bullet hit right wall at r<360 deg angle
            #     self.rotation = 90 - (self.rotation - 270)
            # elif self.rotation < 360: # Bullet hit top wall at r<360 deg angle
            #     self.rotation = 180 + (90 - self.rotation)

            # elif self.rotation < 90 and hitList[0].rect.right >= self.rect.x: # Hit left wall at r<90
            #     print('a')
            #     self.rotation = self.rotation + 270
            # elif self.rotation < 90: # Hit top wall at r<90
            #     print('b')
            #     self.rotation = self.rotation + 90
            # elif self.rotation < 180 and hitList[0].rect.top <= self.rect.y: # Hit bottom wall at r<180
            #     print('c')
            #     self.rotation = 90 - (90 - self.rotation)
            # elif self.rotation < 180: # Hit left wall at r<180
            #     print('d')
            #     self.rotation = (self.rotation - 90) + 180
            # elif self.rotation < 270 and hitList[0].rect.bottom <= self.rect.y: # Hit bottom wall at r<270
            #     print('e')
            #     pass
            # elif self.rotation < 270: # Hit right wall at r<270
            #     print('f')
            #     self.rotation = 180 - (self.rotation - 180)
            # elif self.rotation < 360 and hitList[0].rect.left <= self.rect.x: # Hit right wall at r<360
            #     print('g')
            #     self.rotation = self.rotation - 270
            # elif self.rotation < 360: # Hit top wall at r<360
            #     print('h')
            #     self.rotation = 180 + (90 - self.rotation)




            # Be an actual rotation
            if self.rotation >= 360:
                self.rotation -= 360
            if self.rotation < 0:
                self.rotation += 360

            self.anglePosChange()
            self.update()
            self.update()
            self.health -= 1
