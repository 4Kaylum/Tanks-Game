import pygame
# Import the JSON library to be able to read stored data
import json

from wallClass import *
from playerClass import *

# Create a window object for the class
class Window:

    # To be called when the class is created
    def __init__(self, *, dimensions=[1152, 647], title="Blank"):
        # Init the Pygame module
        pygame.init()
        self.clock = pygame.time.Clock()

        # Create the window itself
        self.window = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(title)
        self.window.fill([255, 255, 255])
        self.background = Wall(dimensions=dimensions)

        # Create the array of drawn walls
        self.levelWalls = []

        # Store the players within the class
        self.playerOne = Player(1)
        self.playerTwo = Player(2)

        # Create the Pygame allspritelist group
        self.wallGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()

        # Add the players to the sprite list
        self.playerGroup.add(self.playerOne)
        self.playerGroup.add(self.playerTwo)

        # Variable to see whether or not to regen walls
        self.tick = True

    # Change the title of the window
    def changeCaption(self, title="Blank"):
        self.window.set_caption(title)

    # Check if the player clicked quit
    def checkQuit(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
        return True

    # Create and draw the walls onto the canvas
    def makeWalls(self, level):
        # Clear the arrays, should there be anything in them
        self.wallGroup.empty()
        self.levelWalls = []
        # Read the level from the JSON
        with open(level) as a:
            settings = json.load(a)

        # Get the walls from that level
        wallList = settings['TileSet']

        for wall in wallList:
            # topLeft=[0, 0], dimensions=[0, 0], colour=[255, 255, 255]
            temp = Wall(
                topLeft=wall['Vertices'][0],
                dimensions=wall['Vertices'][1],
                colour=wall['Colour'])
            # Add the wall to the global lists
            self.levelWalls.append(temp)
            self.wallGroup.add(temp)

    # Draw all sprites to screen
    def drawAll(self):
        self.window.blit(self.background.image,[0,0])
        self.wallGroup.draw(self.window)
        self.bulletGroup.draw(self.window)
        self.playerGroup.draw(self.window)

        pygame.display.flip()
        self.clock.tick(60)

    # Check if the tanks generated any bullets that need to be added
    def addBullets(self):
        if self.playerOne.bullet != None:
            self.bulletGroup.add(self.playerOne.bullet)
            self.playerOne.bullet = None
        if self.playerTwo.bullet != None:
            self.bulletGroup.add(self.playerTwo.bullet)
            self.playerTwo.bullet = None
        

