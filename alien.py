from pygame.sprite import Sprite
from random import randint
import pygame

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, or_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = or_game.screen
        self.settings = or_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/Hostile1_armed175x175.png')
        self.rect = self.image.get_rect()

        self.rect.x = or_game.settings.screen_width
        self.rect.y = randint(0, or_game.settings.screen_height - self.rect.height)

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

        # Random alien speed range
        self.speed = randint(1, 10)

        # Random HP between 2 and 3
        self.hit_points = randint(2, 3)