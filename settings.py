import pygame

class Settings:
    """A class to store all of the settings for Omega Relay."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings
        self.initial_background = pygame.image.load('images/backgrounds/Starfield1_xl.png')
        self.screen_width = self.initial_background.get_width()
        self.screen_height = self.initial_background.get_height()

        # Star settings
        self.star_move_speed = 25

        # Ship settings
        self.ship_speed = 30

        # Player HP - decreases to zero when hit by an alien,
        # decrements when alien ships pass player ship
        self.player_lives = 3

        # Bullet settings
        self.bullet_speed = 40 
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (0, 245, 0)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed_range = (1, 10) # Default speed. See Phase config for expected speeds per level. 