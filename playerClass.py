import pygame
from bulletClass import *

# Create the player class
class Player(pygame.sprite.Sprite):

    # Defines everything about the player
    def __init__(self, playerNumber=0):
        # Init the class
        super().__init__()

        # Read buttons from the settings
        self.buttons = {}

        # Set change variables - these will be checked before moving the player to make sure
        # that there are no collisions
        self.X_c = 0
        self.Y_c = 0

        # Store playerNumber so it doesn't need to be read again later
        self.playerNumber = playerNumber

        # Create it as an object - just debug as red for now
        self.image = pygame.Surface([15, 15])
        self.image.fill([255, 0, 0])

        # Store its rect
        self.rect = self.image.get_rect()

        # Store it's last generated bullet. This is always temporary to go into the Window class
        self.bullet = None

        # Store it's last moved direction. Up left down right, 0 1 2 3
        self.direction = 0

    # Set a player's location depending on the map
    def setLocation(self, coOrds):
        self.rect.x += coOrds[0]
        self.rect.y += coOrds[1]

    # Moves a player's relative location
    def moveLocation(self):
        self.rect.x += self.X_c
        self.rect.y += self.Y_c
        self.X_c = 0
        self.Y_c = 0

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

        ## Change rotation value based on LR values
        if x[self.buttons['right']]:
            self.X_c += 3 # Subject to change
            self.direction = 3
        if x[self.buttons['left']]:
            self.X_c -= 3 # Subject to change
            self.direction = 1

        ## Change XY values based on UD values
        if x[self.buttons['up']]:
            self.Y_c -= 3 # Subject to change
            self.direction = 0
        if x[self.buttons['down']]:
            self.Y_c += 3 # Subject to change
            self.direction = 2

        if x[self.buttons['fire']]:
            self.bullet = Bullet(self)

        # self.moveLocation()
        # self.checkCollide()

    # Check any collisions between itself and another object
    def checkCollide(self, wallGroup):
        # Check what it's hit with - gives list of images
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        # Go through each one, find it's bound
        for block in hitList:
            # Check top-bottom
            if self.Y_c < 0: # If going up set top to block's bottom
                self.rect.top = block.rect.bottom + 3
            elif self.Y_c > 0:
                self.rect.bottom = block.rect.top - 3

        # Regenerate list to avoid conflits
        hitList = pygame.sprite.spritecollide(self, wallGroup, False)
        for block in hitList:
            # Check left-right
            if self.X_c < 0:
                self.rect.left = block.rect.right + 3
            elif self.X_c > 0:
                self.rect.right = block.rect.left - 3
        self.moveLocation()
