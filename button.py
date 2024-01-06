import pygame.font

class Button:
    """A class for text buttons."""

    def __init__(self, or_game, msg, y_offset):
        """Initialize button attributes."""
        self.screen = or_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 250, 70
        self.button_color = (245, 245, 245)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont("Helvetica", 48) 

        # Build the buttons rect object and position it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += y_offset # Apply vertical offset

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
