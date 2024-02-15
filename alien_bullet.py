import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """Class for bullets fired by AlienRailgun."""

    def __init__(self, alien, position):
        super().__init__()
        self.screen = alien.or_game.screen
        self.settings = alien.or_game.settings

        # Load different animations based on position
        if position == alien.top_bullet:
            self.animation_frames = self.load_animation_frames('images/alien_railgun_bullet_top/tile', frame_count=6) # Top arm bullet frames
        elif position == alien.bottom_bullet:
            self.animation_frames = self.load_animation_frames('images/alien_railgun_bullet_bottom/tile', frame_count=6) # Bottom arm bullet frames
       
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midleft = position
        self.alien = alien

        # Initialize animation timing
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100 # Adjust this value as needed for the animation speed. 

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def load_animation_frames(self, base_path, frame_count):
        """Load frames for the animation."""
        frames = []
        for i in range(frame_count):
            filename = f"{base_path}{str(i).zfill(3)}.png"
            try:
                frame = pygame.image.load(filename).convert_alpha()
                frames.append(frame)
            except pygame.error as e:
                print(f"Failed to load frame {filename}: {e}")
        return frames

    def update(self):
        """Move the bullet across the screen."""
        self.x -= self.settings.alien_bullet_speed + self.alien.speed
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
