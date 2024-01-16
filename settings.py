import pygame

class Settings:
    """A class to store all of the settings for Omega Relay."""

    def __init__(self):
        """Initialize game's settings."""
        # Screen settings
        # NOTE: Make sure all png images have 32 bit depth. Use png bit depth converter.py. 
        self.background = pygame.image.load('images/backgrounds/Starfield1_xl.png')
        self.backgrounds = {
            'main_menu': pygame.image.load('images/backgrounds/Starfield1_xl.png'),
            'phase_1': pygame.image.load('images/backgrounds/PurpleNebula1_xl32.png'),              
            'phase_2': pygame.image.load('images/backgrounds/PurpleNebula2_xl32.png'),
            'phase_3': pygame.image.load('images/backgrounds/PurpleNebula3_xl.png'),
            'phase_4': pygame.image.load('images/backgrounds/PurpleNebula4_xl.png'),
            'phase_5': pygame.image.load('images/backgrounds/PurpleNebula5_xl.png'),
        }
    
        self.screen_width = self.background.get_width()
        self.screen_height = self.background.get_height()

        # Star settings
        self.star_move_speed = 25

        # Ship settings
        self.ship_speed = 30

        # Player HP - decreases to zero when hit by an alien,
        # decrements when alien ships pass player ship
        self.player_lives = 20   # HACK: for testing. return to 3 when done. 

        # Bullet settings
        self.bullet_speed = 40 
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (0, 245, 0)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed_range = (1, 10) # Default speed. See Phase config for expected speeds per level. 