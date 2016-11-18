# Import the main library to use for the game
import pygame
# Import self-made classes
from windowClass import *
import windowStates


# Main running code
# This will be all of the "game" stuff
if __name__ == '__main__':
    # Create the window
    window = Window()
    window.windowState = {'title':0,'playing':1,'pause':2,'settings':3,'makelevel':4}['title']
    window.playerOne.readSettings(currentDirectory + '\\Data\\settings.json')
    # window.playerOne.setController(1)
    window.playerTwo.buttons = {'up':pygame.K_w,'left':pygame.K_a,'down':pygame.K_s,'right':pygame.K_d,'fire':pygame.K_f}

    # Run the game while the quit button hasn't been pressed
    while True:
        # Get all player events
        window.getEvents()

        # Make so you can quit
        if not window.checkQuit():
            if window.windowState == 1:
                window.windowState = 0
            else:
                break

        # Increment frame count
        window.frame += 1

        # If playing or generating the level
        if window.windowState in [1, 4]:
            windowStates.playLevel(window)


        # If titlescreen
        elif window.windowState == 0:
            windowStates.titleScreen(window)


    # Out of the loop; kill the program
    pygame.quit()
