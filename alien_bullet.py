import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """Class for bullets fired by AlienRailgun."""

    def __init__(self, alien):
        super().__init__()
        self.screen = alien.or_game.screen
        self.settings = alien.or_game.settings
        self.load_animation_frames('images/alien_railgun_bullet/tile', frame_count=8) # Adjust frame count to correct amount
        self.animation_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midleft = alien.rect.midleft

        # Initialize animation timing
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100 # Adjust this value as needed for the animation speed. 

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def load_animation_frames(self, base_path, frame_count):
        """Load frames for the animation."""
        self.idle_frames = []
        for i in range(frame_count):
            filename = f"{base_path}{str(i).zfill(3)}.png"
            frame = pygame.image.load(filename).convert_alpha()
            self.idle_frames.append(frame)

    def update(self):
        """Move the bullet across the screen."""
        self.x -= self.settings.alien_bullet_speed
        self.rect.x = self.x
        self._animate()

        # Remove the bullet if it moves off the screen
        if self.rect.right < 0:
            self.kill()

    def _animate(self):
        """Animate the bullet."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.frame_index]

    def draw(self):
        """draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)
