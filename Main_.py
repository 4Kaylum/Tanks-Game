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
    window.playerOne.readSettings(currentDirectory + '\\Data\\settings.json')
    window.playerTwo.buttons = {'up':pygame.K_w,'left':pygame.K_a,'down':pygame.K_s,'right':pygame.K_d,'fire':pygame.K_f}

    # Run the game while the quit button hasn't been pressed
    while window.checkQuit():
        window.frame += 1
        if window.tick:
            window.tick = not window.tick
            window.makeWalls(window.levelPath())
            window.playerStartupLocations(window.levelPath())

        window.do()

        frameString = str(hex(window.frame)).upper()[2:]

        playerOne = window.playerOne.rect.center
        playerOneRotation = window.playerOne.rotation

        playerTwo = window.playerTwo.rect.center
        playerTwoRotation = window.playerTwo.rotation
        
        print('{} [P1 [{}, {}], {}] [P2 [{}, {}], {}]'.format(frameString, \
            playerOne[0], playerOne[1], playerOneRotation, \
            playerTwo[0], playerTwo[1], playerTwoRotation))

    # Out of the loop; kill the program
    pygame.quit()
