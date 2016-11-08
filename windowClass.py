import pygame
# Import the JSON library to be able to read stored data
import json
# Import OS and random to get random levels
from os import listdir
from random import choice

from wallClass import *
from playerClass import *
from gameConstants import *

# Create a window object for the class
class Window:

    # To be called when the class is created
    def __init__(self, *, dimensions=[1152, 647], title="Blank"):
        # Init the Pygame module
        pygame.init()


        self.clock = pygame.time.Clock()
        self.level = 'levelThree'

        # Create the window itself
        self.window = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(title)
        self.window.fill([255, 255, 255])
        self.background = Wall(dimensions=dimensions)

        # Create the array of drawn walls
        self.levelWalls = []

        # Store the players within the class
        self.playerOne = Player(1, self)
        self.playerTwo = Player(2, self)

        # Create the Pygame allspritelist group
        self.wallGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()

        # Add the players to the sprite list
        self.playerGroup.add(self.playerOne)
        self.playerGroup.add(self.playerTwo)

        # Variable to see whether or not to regen walls
        self.frame = 0

        # Scoreboard
        self.score = [0, 0]

        # Set the window state
        # {0: Title, 1: Playing, 2: Pause, 3: Settings, 4: Make level}
        self.windowState = 0

    def setLevel(self, *, levelName='', randomLevel=True):
        if levelName == '':
            levelName = self.level
        if randomLevel:
            z = listdir(currentDirectory + '\\Data\\Levels\\')
            levelName = choice(z)[:-5] # Cut off the .json
        self.level = levelName
        self.tick = True
        print('DEBUG [Loading level {}]'.format(levelName))
        self.changeCaption(levelName)
    
    def levelPath(self):
        return currentDirectory + '\\Data\\Levels\\{}.json'.format(self.level)

    def getEvents(self):
        self.events = pygame.event.get()
        return self.events

    # Change the title of the window
    def changeCaption(self, title="Blank"):
        pygame.display.set_caption(title)
        print('DEBUG [Changing window name {}]'.format(title))

    # Check if the player clicked quit
    def checkQuit(self):
        for e in self.events:
            if e.type == pygame.QUIT:
                # pygame.quit()
                return False
        return True

    # Fill the window with white
    def clean(self):
        self.window.fill([255, 255, 255])

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
            print(wall)
            # topLeft=[0, 0], dimensions=[0, 0], colour=[255, 255, 255]
            temp = Wall(
                topLeft=wall['Vertices'][0],
                dimensions=wall['Vertices'][1],
                colour=wall['Colour'])
            # Add the wall to the global lists
            self.levelWalls.append(temp)
            self.wallGroup.add(temp)

    # Draw all sprites to screen
    def drawAll(self, *, drawFPS=True, drawPlayers=True, drawPlayerData=True, clear=True, update=True):
        self.window.blit(self.background.image,[0,0]) if clear else None
        self.wallGroup.draw(self.window)
        self.bulletGroup.draw(self.window) if drawPlayers else None
        self.playerGroup.draw(self.window) if drawPlayers else None
        self.makeFont(str(hex(self.frame)).upper()[2:], [0,0]) if drawFPS else None # Puts the hex in the topleft
        self.makeFont(str(self.playerOne.score),20*self.playerOne.playerNumber) if drawPlayerData else None
        self.makeFont(str(self.playerTwo.score),20*self.playerTwo.playerNumber) if drawPlayerData else None

        pygame.display.flip() if update else None
        self.clock.tick(fpsCounter)

    # Check if the tanks generated any bullets that need to be added
    def addBullets(self):
        if self.playerOne.bullet != None:
            self.bulletGroup.add(self.playerOne.bullet)
            self.playerOne.bullet = None
        if self.playerTwo.bullet != None:
            self.bulletGroup.add(self.playerTwo.bullet)
            self.playerTwo.bullet = None
        
    # Add a font to the screen
    def makeFont(self, text, location, *, colour=[10, 10, 10], size=36):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, colour)
        textpos = text.get_rect()
        if type(location) == int:
            location = [0, location]
        self.window.blit(text, location)

    # Oh god there are so many items save me
    def collisionHell(self):
        # Check wall collisions
        # -- between tanks/walls
        self.playerOne.checkCollide(self.wallGroup)
        self.playerTwo.checkCollide(self.wallGroup)
        # -- between bullets/walls
        for i in self.bulletGroup:
            i.checkCollide(self.wallGroup)
            if i.deleteFlag == True:
                i.kill()
                print('Bullet {} killed.'.format(i))

        self.playerOne.bulletCollide(self.bulletGroup)
        self.playerTwo.bulletCollide(self.bulletGroup)


    def playerStartupLocations(self, pathToLevel):
        with open(pathToLevel) as a:
            jsonified = json.load(a)
        self.playerOne.setLocation([jsonified['PlayerOneStart'][0], jsonified['PlayerOneStart'][1]])
        self.playerTwo.setLocation([jsonified['PlayerTwoStart'][0], jsonified['PlayerTwoStart'][1]])
        self.playerOne.rotation = jsonified['PlayerOneStart'][2]
        self.playerTwo.rotation = jsonified['PlayerTwoStart'][2]


    def do(self, drawFPS=True):
        self.playerOne.checkKeypress()
        self.playerTwo.checkKeypress()
        self.addBullets()
        self.bulletGroup.update()
        self.collisionHell()
        self.playerOne.grace -= 1
        self.playerTwo.grace -= 1
        self.drawAll(drawFPS=drawFPS)

