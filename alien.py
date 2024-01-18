from pygame.sprite import Sprite
from random import randint
from explosion import Explosion
import pygame

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, or_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.or_game = or_game # Reference to the main game instance
        self.screen = or_game.screen
        self.settings = or_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/Hostile1_armed175x175.png')
        self.rect = self.image.get_rect()

        top_limit = 50 # Margin space at the top

        self.rect.x = or_game.settings.screen_width
        self.rect.y = randint(top_limit, or_game.settings.screen_height - self.rect.height) # Top limit instead of zero

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

        # Random alien speed range
        min_speed, max_speed = self.settings.alien_speed_range
        self.speed = randint(min_speed, max_speed)

        # Random HP between 2 and 3
        self.hit_points = randint(2, 3)

        # State
        self.alive = True

    # NOTE: update method for refactor, to be filled out or removed...
        
    def die(self):
        """Trigger the death animation."""
        if self.alive:
            explosion = Explosion(self.screen, self.rect.center, "alien")
            self.or_game.explosions.add(explosion)
            self.kill()
            self.alive = False

    def update(self):
        """Update aliens"""
        self.rect.x -= self.speed
        # You can add more logic here if needed, like checking for off-screen