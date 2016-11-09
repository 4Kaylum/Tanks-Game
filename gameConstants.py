import os 
currentDirectory = os.path.dirname(os.path.realpath(__file__)) # Do not change.

playerMovementAmount = 5
playerRotationAmount = 9
bulletFrameTimeout = 15
bulletMovementAmount = 7
bulletLifetimeTimeout = 500
bulletHealthStartup = 5
fpsCounter = 30
playerSize = 30
playerColour = [[255, 0, 0], [0, 255, 0]] # Array for P1, array for P2 (RGB)
gracePeriod = 30
loadLevel = 'totalBlank' # Leave blank for random level
