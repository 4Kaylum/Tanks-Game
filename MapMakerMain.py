import pygame
import json
import tkinter
from gameConstants import *
from tkinter import filedialog


class Window:

    def __init__(self, *, dimensions=[1152, 647], title="Blank"):
        # Init the Pygame module
        pygame.init()

        self.clock = pygame.time.Clock()

        # Create the window itself
        self.window = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(title)
        self.window.fill([255, 255, 255])
        self.background = Wall(dimensions=dimensions)
        self.wallGroup = pygame.sprite.Group()
        self.tempGroup = pygame.sprite.Group()
        self.frame = 0

        # Make so you can't leave the map
        az = []
        for i in range(5):
            d = dimensions
            az.append( Wall(topLeft=[-5, 0], dimensions=[5, d[1]], colour=[0, 0, 0]) )
            az.append( Wall(topLeft=[d[0], 0], dimensions=[5, d[1]], colour=[0, 0, 0]) )
            az.append( Wall(topLeft=[0, -5], dimensions=[d[0], 5], colour=[0, 0, 0]) )
            az.append( Wall(topLeft=[0, d[1]], dimensions=[d[0], 5], colour=[0, 0, 0]) )
        for i in az:
            self.wallGroup.add(i)

        # Store the last click point
        self.lastClick = None

        # Store the tank objects
        self.tankGroup = pygame.sprite.Group()
        self.tanks = [None, None]
        self.place = 1

    # Save the shizzay
    def saveWindow(self):

        # Get strings to write
        toWriteOut = self.boxesToFile()
        if None not in self.tanks:
            tankOne = self.tanks[0].topLeft
            tankTwo = self.tanks[1].topLeft
            toWriteOut['PlayerOneStart'] = [tankOne[0], tankOne[1], 0]
            toWriteOut['PlayerTwoStart'] = [tankTwo[0], tankTwo[1], 0]
        else:
            print("No tanks placed - will cause errors in game")

        # Save file dialogue
        root = tkinter.Tk()
        root.withdraw()
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if f is None:
            return 

        # Write out
        f.write(json.dumps(toWriteOut,indent=4).replace('\t','    ')) # tabs to spaces~
        f.close()

    def boxesToFile(self):
        toOut = {"TileSet":[]}
        for i in self.wallGroup:
            toOut['TileSet'].append({"Vertices":[i.topLeft,i.dimensions],"Colour":i.colour})
        return toOut

    # Check if the player clicked the window
    def checkClick(self):
        for e in pygame.event.get():
            # Left click
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if self.lastClick == None:
                    self.lastClick = pygame.mouse.get_pos()
                    self.tempGroup.add(Wall(topLeft=pygame.mouse.get_pos(),dimensions=[2,2],colour=[0,0,0]))
                else:
                    cornerOne = self.lastClick
                    cornerTwo = pygame.mouse.get_pos()
                    self.lastClick = None

                    topLeft = []
                    dimensions = []

                    # If first click's X is further right than the second
                    if cornerOne[0] > cornerTwo[0]:
                        # If first click's Y is lower than the second
                        if cornerOne[1] > cornerTwo[1]:
                            topLeft = cornerTwo
                            dimensions = [cornerOne[0] - cornerTwo[0],
                                          cornerOne[1] - cornerTwo[1]]
                        else:
                            topLeft = [cornerTwo[0],cornerOne[1]]
                            dimensions = [cornerOne[0] - cornerTwo[0],
                                          cornerTwo[1] - cornerOne[1]]

                    # If second click's X is further right than the first
                    if cornerOne[0] < cornerTwo[0]:
                        # If second click's Y is lower than the first
                        if cornerOne[1] < cornerTwo[1]:
                            topLeft = cornerOne
                            dimensions = [cornerTwo[0] - cornerOne[0],
                                          cornerTwo[1] - cornerOne[1]]
                        else:
                            topLeft = [cornerOne[0],cornerTwo[1]]
                            dimensions = [cornerTwo[0] - cornerOne[0],
                                          cornerOne[1] - cornerTwo[1]]

                    print(dimensions)

                    self.wallGroup.add(
                        Wall(topLeft=topLeft, dimensions=dimensions, colour=[0, 0, 0]))

                    for i in self.tempGroup:
                        i.kill()


            if e.type == pygame.QUIT:
                self.saveWindow()
                pygame.quit()
                return False


            # Right click
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:

                # Only place two tanks
                if self.place > 2:
                    return True

                # Get position and dimensions
                placement = pygame.mouse.get_pos()
                dimensions = [playerSize, playerSize]

                # Create object
                self.tanks[self.place-1] = Wall(topLeft=placement, dimensions=dimensions, colour=playerColour[self.place-1])
                self.tankGroup.add(self.tanks[self.place-1])

                # Increment the tank ID of placed
                self.place += 1

        return True

    def drawAll(self):
        self.window.blit(self.background.image,[0,0])
        self.wallGroup.draw(self.window)
        self.tempGroup.draw(self.window)
        self.tankGroup.draw(self.window)

        pygame.display.flip()
        self.clock.tick(30)



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
        self.dimensions = dimensions
        self.colour = colour


window = Window()
while window.checkClick():
    window.drawAll()
    window.frame = window.frame + 1
    print('[{}] [{}]'.format(window.frame, window.lastClick))
