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
            'phase_1': pygame.image.load('images/backgrounds/Starfield1_xl.png'),              
            'phase_2': pygame.image.load('images/backgrounds/BlueNebula1_xl.png'),
            'phase_3': pygame.image.load('images/backgrounds/BlueNebula2_xl.png'),
            'phase_4': pygame.image.load('images/backgrounds/BlueNebula3_xl.png'),
            'phase_5': pygame.image.load('images/backgrounds/BlueNebula4_xl.png'),
            'phase_6': pygame.image.load('images/backgrounds/PurpleNebula6_xl.png'),
            'phase_7': pygame.image.load('images/backgrounds/PurpleNebula2_xl.png'),
            'phase_8': pygame.image.load('images/backgrounds/PurpleNebula3_xl.png'),
            'phase_9': pygame.image.load('images/backgrounds/PurpleNebula5_xl.png'),
            'phase_10': pygame.image.load('images/backgrounds/PurpleNebula4_xl.png'),
        }
    
        self.screen_width = self.background.get_width()
        self.screen_height = self.background.get_height()

        # Star settings
        self.star_move_speed = 25

        # Ship settings
        self.ship_speed = 30

        # Player HP - decreases to zero when hit by an alien,
        # decrements when alien ships pass player ship
        self.player_lives = 5
        self.hpup_speed = 5

        # Power Shot settings
        self.power_shot_speed = 12
        self.power_shot_damage = 7
        self.power_shots_allowed = 3
        self.power_shot_splash_radius = 300
        self.power_shot_splash_damage = 3

        # Bullet settings
        self.bullet_speed = 40 
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (0, 245, 0)
        self.bullets_allowed = 7

        # Alien bullet speed
        self.alien_bullet_speed = 5

        # Alien settings
        self.alien_speed_range = (1, 10) # Default speed. See Phase config for expected speeds per level. 