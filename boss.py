import pygame
from pygame.sprite import Sprite
import random

class Boss(Sprite):
    def __init__(self, or_game):
        super().__init__()
        self.game = or_game
        self.health = 300 # Total health
        self.current_phase = 1 # Boss's current phase
        self.attack_patterns = [self.attack1, self.attack2, self.super_attack]
        # Define thresholds for phase transitions
        self.phase_2_threshold = 200
        self.phase_3_threshold = 100
        self.off_screen = False
        self.super_attack_performed = False
        self.entrance_complete = False

        # Attributes for movement and attack logic
        self.vertical_speed = 3
        self.off_screen_speed = 5
        self.top_limit = 100
        self.bottom_limit = self.game.screen_height - 100
        self.target_position = self.game.screen_width // 2

        # Load animation frames
        self.idle_frames = self.load_animation_frames('images/LB_idle_frames/tile', frame_count=48) 
        self.death_frames = self.load_animation_frames('images/LB_death_frames/tile', frame_count=24) 
        self.forward_attack_frames = self.load_animation_frames('images/LB_attack_forward/tile', frame_count=60)
        self.swept_attack_frames = self.load_animation_frames('images/LB_super_attack_frames/tile', frame_count=121)
        self.hurt_frames = self.load_animation_frames('images/LB_hurt_frames/tile', frame_count=7)
        self.jump_frames = self.load_animation_frames('images/LB_jump_frames/tile', frame_count=24)

        # Set the initial animation state
        self.animation_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.animation_frames[self.frame_index]

    def load_animation_frames(self, base_path, frame_count):
        """Load frames for the animation."""
        frames = []
        for i in range(frame_count):
            filename = f"{base_path}{str(i).zfill(3)}.png"
            frame = pygame.image.load(filename).convert_alpha()
            frames.append(frame)
        return frames

    def update(self):
        """Update the boss's behavior based on its current phase."""
        # Implement phase-based behavior and attack patterns
        if self.health <= self.phase_3_threshold:
            self.current_phase = 3
        elif self.health <= self.phase_2_threshold:
            self.current_phase = 2

        if not self.entrance_complete:
            self.boss_entrance()
        else:
            self.attack_patterns[self.current_phase - 1]()

    def boss_entrance(self):
        """Logic to move boss from right side to its starting position."""
        # Once in position, set self.entrance_complete to True
        if self.rect.x > self.target_position:
            self.rect.x -= 5
        else:
            self.entrance_complete = True
            # Trigger phase 1 behavior

    def phase_1_behavior(self):
        """Includes attack 1"""
        # Vertical movement 
        self.rect.y += self.vertical_speed
        if self.rect.top <= self.top_limit or self.rect.bottom >= self.bottom_limit:
            self.vertical_speed = -self.vertical_speed # Change direction

        # Firing logic
        self.fire_projectile()

    def phase_2_behavior(self):
        """Includes attack 2"""
        if not self.off_screen:
            self.move_off_screen()
        else:
            self.spawn_enemies() # Implement enemy spawning
            self.fire_off_screen_projectile() # Implement off-screen firing

    def phase_3_behavior(self):
        """Includes attacks 1, 2 and super attack"""
        if not self.super_attack_performed:
            self.super_attack()
        else:
            # Randomly choose between phase 1 and 2 behaviors
            if random.choice([True, False]):
                self.phase_1_behavior()
            else:
                self.phase_2_behavior()

    def attack1(self):
        """Boss primary attack. Fires large scattered laser beam."""
        # Implement attack 1 logic
        if self.current_phase == 1:
            self.phase_1_behavior()
        elif self.current_phase == 2:
            self.phase_2_behavior()
        elif self.current_phase == 3:
            self.phase_3_behavior()
        
    def attack2(self):
        """Alien rush plus off screen primary attack."""
        # Implement attack 2 logic

    def take_damage(self, damage):
        """Handle boss taking damage"""
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def fire_projectile(self):
        """Logic to fire a projectile at the player"""
        projectile_image_path = 'images/LB_projectile.png'
        projectile = Projectile(self.rect.center, self.game.player.rect.center, projectile_image_path)
        self.game.alien_bullets.add(projectile)

    def fire_off_screen_projectile(self):
        """Logic to randomly fire projectiles from off-screen"""
        # Fire from random off-screen positions
        projectile_image_path = 'images/LB_projectile.png'
        x_positions = [random.randint(-100, -10), random.randint(self.game.screen_width + 10, self.game.screen_width + 100)]
        y_position = random.randint(0, self.game.screen_height)
        random_position = (random.choice(x_positions), y_position)

        projectile = Projectile(random_position, self.game.player.rect.center, projectile_image_path)
        self.game.alien_bullets.add(projectile)

    def super_attack(self):
        """Powerful, wide beam attack."""
        # Perform the super attack
        self.move_to_bottom_center()
        self.sweep_attack()

        self.super_attack_performed = True

    def move_off_screen(self):
        """Logic to move the boss off the right side of the screen"""
        # Set self.off_screen to True when complete
        self.rect.x += self.off_screen_speed
        if self.rect.left > self.game.screen_width:
            self.off_screen = True

    def move_to_bottom_center(self):
        """Logic to position the boss at the bottom center of the screen"""
        self.rect.x = self.game.screen_width // 2 - self.rect.width // 2
        self.rect.y = self.game.screen_height - self.rect.height

    def take_damage(self, damage):
        """Handle taking damage and transitioning between phases."""
        self.health -= damage
        # Check for health thresholds to change phases

class Projectile(pygame.sprite.Sprite):
    """Boss fight laser projectile"""
    def __init__(self, position, target, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.target = target
        self.speed = 5

    def update(self):
        """Move the projectile towards the target"""
        # Simple straight-line movement - improve as needed
        dir_vector = pygame.math.Vector2(self.target) - self.rect.center
        dir_vector.normalize_ip()
        self.rect.centerx += dir_vector.x * self.speed
        self.rect.centery += dir_vector.y * self.speed
        
        # Check if the projectile is off-screen
        if (self.rect.x < 0 or self.rect.x > self.game.screen_width or
            self.rect.y < 0 or self.rect.y > self.game.screen_height):
            self.kill()

    
