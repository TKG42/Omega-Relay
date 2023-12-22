import pygame

class Settings:
    """A class to store all of the settings for Omega Relay."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings
        self.background = pygame.image.load('images/ORB2.png')
        self.screen_width = self.background.get_width()
        self.screen_height = self.background.get_height()

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

        # # Alien settings
        # self.alien_speed = 1.0