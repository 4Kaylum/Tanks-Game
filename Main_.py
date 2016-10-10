# Import the main library to use for the game
import pygame
# Import self-made classes
from wallClass import *
from playerClass import *
from windowClass import *


# Main running code
# This will be all of the "game" stuff
if __name__ == '__main__':
    # Create the window
    window = Window()
    # window.playerOne.readSettings('Data/settings.json')
    window.playerOne.setLocation([200, 200])
    window.playerOne.buttons = {'up':pygame.K_UP,'left':pygame.K_LEFT,'down':pygame.K_DOWN,'right':pygame.K_RIGHT,'fire':pygame.K_KP0}
    window.playerTwo.buttons = {'up':pygame.K_w,'left':pygame.K_a,'down':pygame.K_s,'right':pygame.K_d,'fire':pygame.K_f}
    tick = True

    # Run the game while the quit button hasn't been pressed
    while window.checkQuit():
        if tick:
            tick = not tick
            window.makeWalls('Data/Levels/levelTwo.json')
        window.playerOne.checkKeypress()
        window.playerTwo.checkKeypress()
        window.playerOne.checkCollide(window.wallGroup)
        window.playerTwo.checkCollide(window.wallGroup)
        window.drawAll()

    # Out of the loop; kill the program
    pygame.quit()
