# Import the main library to use for the game
import pygame
# Import the JSON library to be able to read stored data
import json


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
        # Create the array of drawn walls
        self.levelWalls = []
        # Store the players within the class
        self.playerOne = Player(1)
        self.playerTwo = Player(2)
        # Create the Pygame allspritelist group
        self.allSprites = pygame.sprite.Group()
        # Add the players to the sprite list
        self.allSprites.add(self.playerOne)
        self.allSprites.add(self.playerTwo)

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
            self.allSprites.add(temp)

    # Draw all sprites to screen
    def drawAll(self):
        self.allSprites.draw(self.window)
        pygame.display.flip()
        self.clock.tick(60)


# Create the wall class
class Wall(pygame.sprite.Sprite):

    # To be called when the class is created
    # Will be created at the beginning of each level
    def __init__(self, *, topLeft=[0, 0], dimensions=[0, 0], colour=[255, 255, 255]):
        """Build a great wall... and make the class pay for it!"""
        super().__init__()

        # Create the surface of the wall
        self.image = pygame.Surface(dimensions)
        # Colour it
        self.image.fill(colour)
        # Give its rect
        self.rect = self.image.get_rect()
        # Store its top left
        self.topLeft = topLeft
        self.rect.x = self.topLeft[0]
        self.rect.y = self.topLeft[1]


# Create the player class
class Player(pygame.sprite.Sprite):

    # Defines everything about the player
    def __init__(self, playerNumber=0):
        # Init the class
        super().__init__()
        # Read buttons from the settings
        self.buttons = []
        # Create X and Y coords, don't set: to be set by level
        self.X = None
        self.Y = None
        # Store playerNumber so it doesn't need to be read again later
        self.playerNumber = playerNumber
        # Create it as an object - just debug as red for now
        self.image = pygame.Surface([15,15])
        self.image.fill([255,0,0])
        # Store its rect
        self.rect = self.image.get_rect()


    # Set a player's location depending on the map
    def setLocation(self, coOrds):
        self.rect.x = coOrds[0]
        self.rect.y = coOrds[1]

    # Load the settings from the file
    def readSettings(self, jsonFile):
        with open(settingsJSON) as a:
            settings = json.load(a)
        self.buttons = settings['Player{}'.format(playerNumber)]

    # Check if the player clicked quit
    def checkQuit(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
        return True

    # Check any collisions between itself and another object
    def checkCollision(self, otherObject):
        # self.
        pass

# Main running code
# This will be all of the "game" stuff
if __name__ == '__main__':
    # Create the window
    window = Window()
    tick = True
    # Run the game while the quit button hasn't been pressed
    while window.checkQuit():
        if tick:
            tick = not tick
            window.makeWalls('Data/Levels/blankLevel.json')
        window.playerOne.setLocation([100,100])
        window.drawAll()


    # Out of the loop; kill the program
    pygame.quit()
