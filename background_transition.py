import pygame

# NOTE: this class is not being used. 

class BackgroundTransition:
    """Class for handling background transitions between phases."""
    def __init__(self, screen, transition_duration=1000):
        self.screen = screen
        self.transition_duration = transition_duration

    def crossfade(self, current_bg, next_bg):
        step = 5 # Control the speed of the crossfade
        for alpha in range(0, 255, step):
            current_bg.set_alpha(255 - alpha)
            next_bg.set_alpha(alpha)
            self.screen.blit(current_bg, (0, 0))
            self.screen.blit(next_bg, (0, 0))
            pygame.display.flip()
            pygame.time.wait(int(self.transition_duration / (255 / step)))