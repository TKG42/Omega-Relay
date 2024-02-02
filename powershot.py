import pygame
from pygame.sprite import Sprite

class PowerShot(Sprite):
    """Represents a power shot that causes splash damage."""
    def __init__(self, or_game, pos):
        super().__init__()
        self.screen = or_game.screen
        self.settings = or_game.settings
        self.position = pos

        # Powerup animation inits
        self.shot_animation_frames = [pygame.image.load(f'images/PowerShotFrames/{i:02}.png').convert_alpha() for i in range(8)]
        self.current_frame = 0
        self.animation_rate = 100 # Milliseconds per frame
        self.last_update = pygame.time.get_ticks()
        self.image = self.shot_animation_frames[self.current_frame]
        self.rect = self.image.get_rect(center=self.position)

        # Other attributes
        self.speed = self.settings.power_shot_speed

    def update(self):
        """Move the power shot."""
        self.rect.x += self.speed
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.shot_animation_frames)
            self.image = self.shot_animation_frames[self.current_frame]

    def draw(self):
        """Draw the current frame."""
        self.screen.blit(self.image, self.rect)
        