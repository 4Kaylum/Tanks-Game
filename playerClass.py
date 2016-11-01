import pygame
from bulletClass import *
from time import time
import math
from gameConstants import *
import json

# Create the player class
class Player(pygame.sprite.Sprite):

    # Defines everything about the player
    def __init__(self, playerNumber, parent):
        # Init the class
        super().__init__()

        # Keep track of frame tick
        self.parent = parent

        # Read buttons from the settings
        self.buttons = {}

        # Set change variables - these will be checked before moving the player to make sure
        # that there are no collisions
        self.X_c = 0.0
        self.Y_c = 0.0

        # Store playerNumber so it doesn't need to be read again later
        self.playerNumber = playerNumber

        # Create it as an object - just debug as red for now
        self.imageOriginal = pygame.Surface([playerSize, playerSize])
        # self.imageOriginal = pygame.image.load(currentDirectory + '\\Data\\PlayerOne.png')
        self.rectOriginal = self.imageOriginal.get_rect()
        self.image = self.imageOriginal
        self.rect = self.rectOriginal

        # Store it's last generated bullet. This is always temporary to go into the Window class
        self.bullet = None

        # Store it's last moved direction.
        self.rotation = 0 

        # Make it so you can't spam bullets
        self.lastShot = -5000

        # Keep score for the user
        self.score = 0


    # Set a player's location depending on the map
    def setLocation(self, coOrds):
        self.rect.x = coOrds[0]
        self.rect.y = coOrds[1]

    # Moves a player's relative location
    def moveLocation(self, coOrds):
        # self.rect.x += self.X_c
        # self.rect.y += self.Y_c
        self.rect.x += coOrds[0]
        self.rect.y += coOrds[1]        

    # Load the settings from the file
    def readSettings(self, jsonFile):
        with open(jsonFile) as a:
            settings = json.load(a)
        self.buttons = settings['Player{}'.format(self.playerNumber)]

    # Check if the player clicked quit
    def checkQuit(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
        return True

    # Check the assigned buttons to see if there's any keypresses
    def checkKeypress(self):
        x = pygame.key.get_pressed()

        # Change rotation value based on LR values
        if x[self.buttons['right']]:
            self.rotation -= playerRotationAmount
        if x[self.buttons['left']]:
            self.rotation += playerRotationAmount
        self.anglePosChange(True, False)

        # Change XY values based on UD values
        if x[self.buttons['up']]:
            # self.Y_c -= playerMovementAmount
            self.anglePosChange(True)
            # move = True
            # actuallyMove = True
            # rotate = True
        if x[self.buttons['down']]:
            # self.Y_c += playerMovementAmount
            self.anglePosChange(False)
            # move = False
            # actuallyMove = True
            # rotate = True

        if self.rotation >= 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360

        if self.parent.frame > self.lastShot + bulletFrameTimeout:
            self.lastShot = self.parent.frame
            if x[self.buttons['fire']]:
                self.bullet = Bullet(self)


    # Get X/Y change values from an angle
    def anglePosChange(self,forward=True,actuallyMove=True):
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

        # self.image, self.rect = self.rotCentre()
        self.rotCentre()

        if actuallyMove == False:
            return

        # math.acos(math.radians(r_y)) * playerMovementAmount * multiplier[1] * forwardMultiplier
        self.X_c = multiplier[0] * forwardMultiplier * playerMovementAmount * math.sin(math.radians(r_raw))
        self.Y_c = multiplier[1] * forwardMultiplier * playerMovementAmount * math.cos(math.radians(r_raw))


    def rotCentre(self):

        self.image.fill(playerColour[self.playerNumber-1])

        return # Uncomment to turn off image rotation

        rot_image = pygame.transform.rotate(self.imageOriginal, self.rotation)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        self.image = rot_image
        self.rect = rot_rect
        
        # self.image.fill([255, 0, 0]) # Uncomment this to fill image hitbox

    # Check any collisions between itself and another object
    def checkCollide(self, wallGroup):
        # Move the object to make sure it's collided
        self.moveLocation([0, self.Y_c])
        # Check what it's hit with - gives list of images
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        # Go through each one, find it's bound
        for block in hitList:
            # Check top-bottom
            if self.Y_c < 0: # If going up set top to block's bottom
                self.rect.top = block.rect.bottom
            elif self.Y_c > 0:
                self.rect.bottom = block.rect.top

        # Regenerate list to avoid conflits
        self.moveLocation([self.X_c, 0])
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        for block in hitList:
            # Check left-right
            if self.X_c < 0:
                self.rect.left = block.rect.right
            elif self.X_c > 0:
                self.rect.right = block.rect.left

        self.X_c = self.Y_c = 0

    def bulletCollide(self, bulletGroup):
        # Check what it's hit with - gives list of images
        hitList = pygame.sprite.spritecollide(self, bulletGroup, False)
        if len(hitList) > 0:
            print("ouch {}".format(self.playerNumber))

