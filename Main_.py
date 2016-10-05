# Import the main library to use for the game
import pygame
# Import the JSON library to be able to read stored data
import json


# Create a window object for the class
class Window:

    # To be called when the class is created
    def __init__(self, *, dimensions=[1152, 647], title="Blank", players=[0, 0]):
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
        self.PlayerOne = players[0]
        self.PlayerTwo = players[1]
        # Create the Pygame allspritelist group
        self.allSprites = pygame.sprite.Group()

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
                wall['Vertices'][0],
                wall['Vertices'][1],
                wall['Colour'])
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
    def __init__(self, *, settingsJSON='', playerNumber=0):
        # Read settings from the JSON
        with open(settingsJSON) as a:
            settings = json.load(a)
        # Read buttons form the settings
        self.buttons = settings['Player{}'.format(playerNumber)]
        # Create X and Y coords, don't set: to be set by level
        self.X = None
        self.Y = None
        # Store playerNumber so it doesn't need to be read again later
        self.playerNumber = playerNumber

    # Set a player's location depending on the map
    def setLocation(self, map):
        pass

    # Check if the player clicked quit
    def checkQuit(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
        return True

# Main running code
# This will be all of the "game" stuff
if __name__ == '__main__':
    # Create the window
    window = Window()
    # Run the game while the quit button hasn't been pressed
    while window.checkQuit():
        if tick:
            tick = not tick
            window.makeWalls('Data/Levels/levelOne.json')
        window.drawAll()

    # Out of the loop; kill the program
    pygame.quit()
