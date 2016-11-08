# Import the main library to use for the game
import pygame
# Import self-made classes
from wallClass import *
from playerClass import *
from windowClass import *
from bulletClass import *
from gameConstants import *


# Main running code
# This will be all of the "game" stuff
if __name__ == '__main__':
    # Create the window
    window = Window()
    window.windowState = {'title':0,'playing':1,'pause':2,'settings':3,'makelevel':4}['title']
    window.playerOne.readSettings(currentDirectory + '\\Data\\settings.json')
    window.playerTwo.buttons = {'up':pygame.K_w,'left':pygame.K_a,'down':pygame.K_s,'right':pygame.K_d,'fire':pygame.K_f}

    # Run the game while the quit button hasn't been pressed
    while True:
        # Get all player events
        window.getEvents()

        # Make so you can quit
        if not window.checkQuit():
            break

        # Increment frame count
        window.frame += 1

        # Clean the map
        window.clean()
        window.wallGroup = pygame.sprite.Group()

        # If playing or generating the level
        if window.windowState in [1, 4]:
            # Set level up
            if window.windowState == 4:
                window.windowState = 1

                # Load the level
                if loadLevel != '':
                    window.setLevel(levelName=loadLevel,randomLevel=False)
                else:
                    window.setLevel(randomLevel=True)

                # Generate the level
                window.makeWalls(window.levelPath())
                window.playerStartupLocations(window.levelPath())

            # Do all the movement and collision and stuff
            window.do()

            # Debug strings~
            frameString = str(hex(window.frame)).upper()[2:]
            print('{} {} {}'.format(frameString, window.playerOne, window.playerTwo))

        # If titlescreen
        elif window.windowState == 0:
            # Create the clickbox
            window.wallGroup.add(Wall(topLeft=[50, 50], dimensions=[300, 50], colour=[0,0,0], name='PlayButton'))

            # Update and draw
            window.drawAll(drawPlayerData=False, drawPlayers=False, clear=False, update=False)

            # Draw the text on top of it
            window.makeFont('Play', [200,75], colour=[255, 255, 255])

            # Update display
            pygame.display.flip()

            # Check if it was clicked
            if pygame.MOUSEBUTTONDOWN in [i.type for i in window.events]:
                ifClicked = [o.checkClick(pygame.mouse.get_pos()) for o in window.wallGroup][0]
                if ifClicked:
                    window.windowState = 4



    # Out of the loop; kill the program
    pygame.quit()
