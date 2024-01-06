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

        # Adjust size as needed
        self.phase_level_font = pygame.font.SysFont(None, 92)
        self.phase_level_image = None
        self.phase_level_rect = None

    def show_phase_level(self, phase):
        """Display the phase level on-screen."""
        phase_str = f"PHASE {phase}"
        self.phase_level_image = self.phase_level_font.render(phase_str, True, (255, 255, 255))
        self.phase_level_rect = self.phase_level_image.get_rect()
        self.phase_level_rect.center = self.screen_rect.center

    def draw_phase_level(self):
        """Draw the phase level to the screen."""
        if hasattr(self, 'phase_level_image') and self.phase_level_image: # Check for initialization
            self.screen.blit(self.phase_level_image, self.phase_level_rect)

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