import pygame

# Create the wall class
class Wall(pygame.sprite.Sprite):

    # To be called when the class is created
    # Will be created at the beginning of each level
    def __init__(self, *, topLeft=[0, 0], dimensions=[0, 0], colour=[255, 255, 255], name=None):
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

        # Store a name
        self.name = name

    # See if self was clicked
    def checkClick(self, mousePoint):
        return self.rect.collidepoint(mousePoint)
