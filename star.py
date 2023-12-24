from pygame.sprite import Sprite
from random import randint
import pygame

class Star(Sprite):
    """A class to represent a single star."""

    def __init__(self, or_game):
        """Initialize the star and set its starting position."""
        super().__init__()
        self.screen = or_game.screen

        # Load the star image and set its rect attribute.
        self.image = pygame.image.load('images/sparklestar210x10.png') 
        self.rect = self.image.get_rect()

        self.rect.x = or_game.settings.screen_width
        self.rect.y = randint(0, or_game.settings.screen_height - self.rect.height)

        # Store the stars exact horizontal position.
        self.x = float(self.rect.x)