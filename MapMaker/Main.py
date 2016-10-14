import pygame
import json
import tkinter
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

        # Store the last click point
        self.lastClick = None

    # Save the shizzay
    def saveWindow(self):
        root = tkinter.Tk()
        root.withdraw()
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if f is None:
            return 
        f.write(self.boxesToFile())
        f.close()

    def boxesToFile(self):
        toOut = {"TileSet":[]}
        for i in self.wallGroup:
            toOut['TileSet'].append({"Vertices":[i.topLeft,i.dimensions],"Colour":i.colour})
        return json.dumps(toOut,indent=4)

    # Check if the player clicked the window
    def checkClick(self):
        for e in pygame.event.get():
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
        return True

    def drawAll(self):
        self.window.blit(self.background.image,[0,0])
        self.wallGroup.draw(self.window)
        self.tempGroup.draw(self.window)

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
