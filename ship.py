import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, or_game):
        """Initialize the ship and set its starting position."""
        self.screen = or_game.screen
        self.settings = or_game.settings
        self.screen_rect = or_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/F3_ready150x150.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the left center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_up = False
        self.moving_down = False

        # attribute to control visibility
        self.visible = True

    def update(self):
        """Update the ship's position based on the movement flag."""
        top_limit = 50 # Margin space at the top

        # Update the ship's y value
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top > top_limit: # Top limit instead of 0
            self.y -= self.settings.ship_speed

        # Update rect object from self.y
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        if self.visible:
            self.screen.blit(self.image, self.rect)