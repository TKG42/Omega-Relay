import sys 
import pygame
from random import randint
from settings import Settings
from star import Star
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# NOTE: Next feature to implement: Player powerups


class OmegaRelay:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Omega Relay")

        self.ship = Ship(self)
        
        # Add a star every x frames
        self.star_add_interval = 5
        self.frame_counter = 0

        # Add an alien every x frames
        self.alien_add_interval = 100
        self.frame_counter2 = 0

        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # Instance for storing game stats.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Make the start game button
        self.start_game_button = Button(self, "Engage", 0)

        # Active state for state machine.
        self.state = "playing"
        self.danger_start_time = None

        # Initialize timer
        self.game_over_start = None # Start with None to indicate no timer is running

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.state == "playing":
                self.playing_state()
            elif self.state == "danger": 
                self.danger_state()
            elif self.state == "game_over":
                self.game_over_state()
            elif self.state == "main_menu":
                self.main_menu_state()
            self._update_screen()

    def playing_state(self): 
        """Handle all playing logic, updating the ship, stars, bullets, etc."""
        self.ship.update()
        self._update_starshower()
        self._update_bullets()
        self._update_aliens()
        self._check_aliens_leftscreen()

    def danger_state(self):
        """ Display the danger message and return to playing state after a brief period."""
        current_time = pygame.time.get_ticks()
        if current_time - self.danger_start_time > 2000:  # 2 seconds passed
            self.state = "playing"
        self.ship.blitme() # Make sure the ship is drawn
        # Continue updating the game elements while in danger state
        self.playing_state()
        
    def game_over_state(self):
        """ Display the game over message and stop updating the ship"""
         # Stop player control
        self.ship.moving_up = False 
        self.ship.moving_down = False
        # You can update the background elements here if you want them to continue animating
        self._update_starshower()
        self._game_over_message()

        # Continue with the 5-second wait
        if self.game_over_start is None: # Initialize timer if not already set. 
            self.game_over_start = pygame.time.get_ticks()

        # Transition to the main menu after 5 seconds
        if pygame.time.get_ticks() - self.game_over_start > 5000:
            self.game_over_start = None # Reset the timer for next game over
            self.state = "main_menu"

    def main_menu_state(self): 
        """Display the start game button, score data and other options."""
        # Ensure all game elements are reset for a clean state
        self.reset_game()
        self.stars.empty() # Optionally clear the stars or handle them differently for the main menu.

        # Draw the main menu
        if isinstance(self.settings.background, tuple): # For a color background
            self.screen.fill(self.settings.background)
        else:                                           # For a background image
            self.screen.blit((self.settings.background), (0, 0))
        self.start_game_button.draw_button()

        # Update the screen
        pygame.display.flip()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_button_down(event)
                # Handle immediate transition from game over to main menu
                if self.state == "game_over":
                    self.game_over_start = None # Reset timer
                    self.state = "main_menu"
                    return # Skip further processing

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def reset_game(self):
        """Reset all game dynamics and stats for a new game."""
        self.stats.reset_stats()
        self.ship = Ship(self)
        self.bullets.empty()
        self.aliens.empty()
        self.explosions.empty()
        # Add any other necessary resets here (e.g., resetting scores, lives)

    def _check_mouse_button_down(self, event):
        """Handle mouse button down events for the entire game."""
        mouse_x, mouse_y = event.pos 
        if self.state == "main_menu":
            if self.start_game_button.rect.collidepoint(mouse_x, mouse_y):
                # Reset necessary game elements here before switching to playing state.
                self.reset_game()
                self.state = "playing"

    def _create_star(self, star_number):
        """Create a star and place it in the column."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 2 * star_width * star_number

        # Random star position
        star.rect.x = randint(star_width, 1792 - 2 * star_width)
        star.rect.y = randint(star_height, 1024 - 2 * star_height)
        self.stars.add(star)

    def _starflight(self):
        """Cause all stars to rush from the right side of the screen to the left."""
        for star in self.stars.sprites():
            star.rect.x -= self.settings.star_move_speed

    def _update_starshower(self):
        """Update the position of all stars."""
        self._starflight()
        # Remove any stars that have moved to the edge of the left side screen
        for star in self.stars.copy():
            # if star.rect.top > self.settings.screen_height:
            if star.rect.right < 0:
                self.stars.remove(star)
        # Add new stars with a random y position from the right side screen
        self.frame_counter = (self.frame_counter + 1) % self.star_add_interval
        if self.frame_counter == 0:
            self._create_new_column_of_stars()
    
    def _create_new_column_of_stars(self):
        """Create a new column of stars at the right side of the screen."""
        for _ in range(3): # Change the range to add more stars
            star = Star(self)
            # Start the new star at a random y position on the right side of the screen.
            star.rect.y = randint(0, self.settings.screen_height - star.rect.height)
            star.rect.x = self.settings.screen_width
            self.stars.add(star)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared or gone off of the right edge.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        # Change self.bullets boolean pair to False for super bullets that rip through (good for testing)

        for aliens in collisions.values():
            for alien in aliens:
                alien.hit_points -= 1
                if alien.hit_points <= 0:
                    explosion = Explosion(self.screen, alien.rect.center, "alien")
                    self.explosions.add(explosion)
                    self.aliens.remove(alien)

        if not self.aliens:
            # Destroy existing bullets
            self.bullets.empty()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Player lives immediately set to zero
        self.stats.lives_left = 0
        self.ship.visible = False # Hide the ship
        explosion = Explosion(self.screen, self.ship.rect.center, "player")
        self.explosions.add(explosion)
        # Set state to game over
        self.state = "game_over"
        # Destroy existing bullets and aliens
        self.bullets.empty()
        self.aliens.empty() 
        # Update the screen immediately to show the explosion
        self._update_screen()

    def _check_aliens_leftscreen(self):
        """Check if any aliens made it to the left side of the screen."""
        for alien in self.aliens.sprites():
            # Threshold for checking if an alien has passed
            if alien.rect.right < self.settings.screen_width * 0.02: # 2% of screen width
                self.aliens.remove(alien)
                self.stats.lives_left -= 1
                if self.stats.lives_left <= 0:
                    self.state = "game_over"
                    break  # Exit the loop as we're going to game over
                elif self.state == "playing":  # Only set to danger if we're currently playing
                    self.state = "danger"
                    self.danger_start_time = pygame.time.get_ticks()
                    break  # Only trigger once per frame

    def _update_aliens(self):
        """Update the position of all aliens."""
        self._alien_rush()
        # Remove any aliens that have moved to the edge of the left side screen
        for alien in self.aliens.copy():
            if alien.rect.right < 0:
                self.aliens.remove(alien)

        # Add new aliens with a random y position from the right side screen
        self.frame_counter2 = (self.frame_counter2 + 1) % self.alien_add_interval
        if self.frame_counter2 == 0:
            self._create_new_column_of_aliens()

        # Look for alien-ship-collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens that have reached the left side of the screen
        self._check_aliens_leftscreen()

    def _create_new_column_of_aliens(self):
        """Create a new column of aliens at the right side of the screen."""
        for _ in range(3): # Change the range to add more aliens
            alien = Alien(self)
            # Start the new alien at a random y position on the right side of the screen.
            alien.rect.y = randint(0, self.settings.screen_height - alien.rect.height)
            alien.rect.x = self.settings.screen_width
            self.aliens.add(alien)

    def _alien_rush(self):
        """Cause all Aliens to rush from the right side of the screen to the left."""
        for alien in self.aliens.sprites():
            alien.rect.x -= alien.speed

    def _create_alien(self, alien_number):
        """Create an alien and place it in the column."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number

        alien.rect.x = randint(alien_width, 1792 - 2 * alien_width)
        alien.rect.y = randint(alien_width, 1024 - 2 * alien_height)
        self.aliens.add(alien)

    def _flash_danger_message(self):
        font = pygame.font.SysFont(None, 64)
        danger_message = font.render('DANGER!!', True, (255, 0, 0))
        message_rect = danger_message.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(danger_message, message_rect)

    def _game_over_message(self):
        # Code to display MISSION FAILED message
        font = pygame.font.SysFont(None, 72)
        game_over_message = font.render('MISSION FAILED', True, (255, 0, 0))
        message_rect = game_over_message.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_message, message_rect)
        # TODO: implement menu features here

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.background, (0, 0))
        self.stars.draw(self.screen)
        self.aliens.draw(self.screen)

        if self.state == "playing" or self.state == "danger":
            self.ship.blitme() # Draw the ship in both playing and danger states
            self.sb.prep_lives()
            self.sb.show_lives()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.explosions.update()
        self.explosions.draw(self.screen)

        if self.state == "danger":
            self._flash_danger_message()
        elif self.state == "game_over":
            self._game_over_message()

        if self.state == "main_menu":
            self.start_game_button.draw_button() # Ensure button is drawn only in main menu state

        pygame.display.flip()

if __name__ == '__main__':
    orgame = OmegaRelay()
    orgame.run_game()