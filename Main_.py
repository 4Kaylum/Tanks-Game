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
        
        print(str(hex(window.frame)).upper()[2:]+' [P1 '+str([str(window.playerOne.rect.center[0]),str(window.playerOne.rect.center[1]),str(window.playerOne.rotation)])+'] [P2 '+str([str(window.playerTwo.rect.center[0]),str(window.playerTwo.rect.center[1]),str(window.playerTwo.rotation)])+']')

    # Out of the loop; kill the program
    pygame.quit()
