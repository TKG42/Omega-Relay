import pygame
from pygame.sprite import Sprite

class HpUp(Sprite):
    """Hit point increase powerup."""
    def __init__(self, or_game, position):
        super().__init__()
        self.screen = or_game.screen
        self.settings = or_game.settings

        # Animation inits
        self.hpup_animation_frames = [pygame.image.load(f'images/fuel_cell_animation_frames/{i:02}.png').convert_alpha() for i in range(9)]
        self.current_frame = 0
        self.animation_rate = 100 # Milliseconds per frame
        self.last_update = pygame.time.get_ticks()
        self.image = self.hpup_animation_frames[self.current_frame]
        self.rect = self.image.get_rect(center=position)

        # Other attributes
        self.speed = self.settings.hpup_speed  

    def update(self):
        """Move the HP up"""
        self.rect.x -= self.speed
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.hpup_animation_frames)
            self.image = self.hpup_animation_frames[self.current_frame]

    def draw(self):
        """Draw the current frame."""
        self.screen.blit(self.image, self.rect)