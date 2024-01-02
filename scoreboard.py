import pygame

class Scoreboard:
    """ A class to report scoring information."""

    def __init__(self, or_game):
        """Initialize scorekeeping attributes."""
        self.screen = or_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = or_game.settings
        self.stats = or_game.stats

        # Load the player life image
        self.life_image = pygame.image.load('images/fuelcell2_t40x40.png') 
        self.life_rect = self.life_image.get_rect()
        self.lives = []

    def prep_lives(self):
        """Show how many lives are left."""
        self.lives = []
        for life_number in range(self.stats.lives_left):
            life = self.life_image.get_rect()
            life.x = 10 + life_number * (life.width + 10) # 10 pixels apart
            life.y = 10 # 10 pixels from the top
            self.lives.append(life)

    def show_lives(self):
        """Draw lives to the screen."""
        for life in self.lives:
            self.screen.blit(self.life_image, life)