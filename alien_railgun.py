from pygame.sprite import Sprite
from random import randint
import pygame

# NOTE: This enemy has unique behavior. It does not move across the screen.
# Instead, this alien spawns from the right side of the screen like other enemy types, but it only moves a few paces forward before halting
# Then it fires at the player continuosly from its position until its killed. 

# NOTE: this class needs a method to handle the firing animation.

class AlienRailgun(Sprite):
    """Class representing large, powerful railgun enemy."""
    def __init__(self, or_game):
        super().__init__()
        self.or_game = or_game # Reference to the main game instance
        self.screen = or_game.screen
        self.settings = or_game.settings

        # Load animation frames
        self.idle_frames = self.load_animation_frames('images/alien_railgun/tile', frame_count=29) 
        self.death_frames = self.load_animation_frames('images/alien_railgun_death/tile', frame_count=14) 
        self.firing_frames = self.load_animation_frames('images/alien_railgun_firing/tile', frame_count=25)

        # Set the initial animation state
        self.animation_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect()

        # Set initial position
        top_limit = 50
        self.rect.x = or_game.settings.screen_width
        self.rect.y = randint(top_limit, or_game.settings.screen_height - self.rect.height)

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        # Speed
        self.speed = randint(*self.settings.alien_speed_range)

        # Flag for checking if alien has stopped moving
        self.has_stopped = False

        # HP
        self.hit_points = 13

        # Animation timing
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100 # milliseconds per frame

        # State 
        self.alive = True
        self.is_dying = False

    def load_animation_frames(self, base_path, frame_count):
        """Load frames for the animation."""
        frames = []
        for i in range(frame_count):
            filename = f"{base_path}{str(i).zfill(3)}.png"
            frame = pygame.image.load(filename).convert_alpha()
            frames.append(frame)
        return frames
    
    def fire(self):
        """Handle firing behavior and animation."""
        # Switch to firing animation
        if not self.has_stopped:
            return
        self.animation_frames = self.firing_frames
        self.frame_index = 0

        # NOTE Implemenet firing logic
        # This could involve creating bullets or other projectiles
        # and adding them to a relevant sprite group in the game.

    def die(self):
        """Trigger the death animation."""
        if not self.is_dying:
            self.is_dying = True
            self.animation_frames = self.death_frames
            self.frame_index = 0
            self.alive = False
            # Do not call self.kill() here; let the update method handle it

    def update(self):
        """Update the alien's position and animation."""
        # Update position
        if self.alive:
            self.x -= self.speed
            self.rect.x = self.x

        if self.alive and not self.has_stopped:
            if self.rect.x <= self.settings.screen_width * 0.8:  # change as needed
                self.has_stopped = True

        # Update animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.frame_index]

            if not self.alive and self.frame_index == len(self.death_frames) - 1:
                self.kill() # Remove the sprite after the death animation.
                self.or_game.handle_alien_defeat()

        # If the alien has halted and is alive, start firing
        if self.has_stopped and self.alive:
            self.fire()