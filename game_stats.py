class GameStats:
    """Track statistics for OmegaRelay."""

    def __init__(self, or_game):
        """Initialize statistics."""
        self.settings = or_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.player_lives