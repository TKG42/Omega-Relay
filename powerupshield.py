import pygame

class ShieldPowerup:
    """Class to represent and manage the player shield powerup."""
    def __init__(self, or_game):
        self.screen = or_game.screen
        self.settings = or_game.settings
        self.phase_manager = or_game.phase_manager

        self.active_image = pygame.image.load('images/powerup-icons/shield_active.png')  
        self.inactive_image = pygame.image.load('images/powerup-icons/shield_inactive.png')
        self.shield_icon_rect = self.inactive_image.get_rect()
        self.shield_icon_rect.topright = (self.settings.screen_width - 10, 10) # Adjust as needed

        # Powerup stats
        self.active = False
        self.shield_strength = 3
        self.cooldown = 30000 # Miliseconds. Test to be sure
        self.last_activation_time = 0

        # Powerup animation inits
        number_of_frames = 0 # NOTE: add animation # of frames for shields here, or directly in self.animation_frames.
        self.animation_frames = [pygame.image.load(f'images/FullShieldFrames/{i}.png') for i in range(number_of_frames)]
        self.current_frame = 0
        self.animation_rate = 100 # Milliseconds per frame
        self.last_update = pygame.time.get_ticks()

    def update_animation(self):
        """Update the animation for the shield around the player."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_rate:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def draw_shield(self, ship):
        """Draw the animated player shield to the screen."""
        if self.active:
            self.update_animation()
            frame = self.animation_frames[self.current_frame]
            frame_rect = frame.get_rect(center=ship.rect.center)
            self.screen.blit(frame, frame_rect)

    def update(self):
        """Update method for shield powerup."""
        if self.phase_manager.current_phase < 3:
            return
        current_time = pygame.time.get_ticks()
        if self.active and (current_time - self.last_activation_time > self.cooldown * 1000):
            self.active = False

        # Additional update logic here
            
    def draw(self):
        """Draw shield powerup icon to the screen."""
        if self.phase_manager.current_phase < 3:
            return
        image = self.active_image if self.active else self.inactive_image
        self.screen.blit(image, self.shield_icon_rect)

    def activate(self):
        """Change shield status to active state."""
        if not self.active and self.phase_manager.current_phase >= 3:
            self.active = True
            self.shield_strength = 3
            self.last_activation_time = pygame.time.get_ticks()

    def take_damage(self):
        """Handle shield health."""
        if self.active:
            self.shield_strength -= 1
            if self.shield_strength <= 0:
                self.active = False
