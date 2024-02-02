import pygame

# NOTE: this class is not being used. 

class BackgroundTransition:
    """Class for handling background transitions between phases."""
    def __init__(self, or_game, transition_duration=1000):
        self.game = or_game
        self.screen = self.game.screen
        self.transition_duration = transition_duration
        self.step = 2
        self.alpha = 0
        self.current_bg = self.game.settings.backgrounds['phase_' + str(self.game.phase_manager.current_phase)]
        self.next_bg = self.game.settings.backgrounds['phase_' + str(self.game.phase_manager.current_phase + 1)]
        self.started = False

    def crossfade(self):
        """Handles background transitions during phase change."""

        # Update alpha for transition
        self.alpha = min(255, self.alpha + self.step) # Increment alpha
        self.current_bg.set_alpha(255 - self.alpha)
        self.next_bg.set_alpha(self.alpha)

        # Blit the transitioning backgrounds
        self.screen.blit(self.current_bg, (0, 0))
        self.screen.blit(self.next_bg, (0, 0))

        if self.alpha >= 255:
            # End of transition
            self.started = False
