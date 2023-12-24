from pygame.sprite import Sprite
import pygame

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, or_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = or_game.screen
        self.settings = or_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set the correct position.
        self.image = pygame.image.load('images/biggblast50x20.png')
        self.rect = self.image.get_rect()

        self.rect.midright = or_game.ship.rect.midright

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet across the screen."""
        # Update the decimal position of the bullet.
        self.x += self.settings.bullet_speed
        # Update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)