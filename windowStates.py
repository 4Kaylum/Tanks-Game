from wallClass import *
from windowClass import *

def playLevel(window):
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

def titleScreen(window):
    # Clear the window
    window.clean()
    window.wallGroup = pygame.sprite.Group()
    window.bulletGroup = pygame.sprite.Group()
    
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
