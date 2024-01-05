class PhaseManager:
    def __init__(self, or_game):
        self.game = or_game
        self.current_phase = 1
        self.total_phases = 5 # Excluding boss fight

        # Define phase characteristics like enemy speed, spawn rates, etc.
        self.phase_configs = [
            {"speed_range": (1, 10), "spawn_rate": 75, "player_speed": 30, "bullet_speed": 40}, # Phase 1
             {"speed_range": (1, 15), "spawn_rate": 150, "player_speed": 30, "bullet_speed": 40}, # Phase 2
              {"speed_range": (5, 20), "spawn_rate": 200, "player_speed": 40, "bullet_speed": 50}, # Phase 3
               {"speed_range": (5, 20), "spawn_rate": 200, "player_speed": 40, "bullet_speed": 50, "enemy_bullet_speed": 30}, # Phase 4
                {"speed_range": (7, 25), "spawn_rate": 300, "player_speed": 50, "bullet_speed": 60, "enemy_bullet_speed": 40}, # Phase 5
             # ... Add configurations for each phase}
        ]

    def next_phase(self):
        """Transition to the next phase if there are remaining phases."""
        if self.current_phase < self.total_phases:
            self.current_phase += 1
            self.apply_phase_config()
            # Display new phase level in the center of the screen (HUD update)

    def apply_phase_config(self):
        """Apply the configurations for the current phase."""
        config = self.phase_configs[self.current_phase - 1]
        # Update the game settings based on phase configurations
        # E.g., self.game.settings.alien_speed = config["speed_range"]
        # And so on for spawn rate, player speed, and bullet speed

    def update(self):
        """Update phase-related conditions and check for phase completion."""
        # Check if all enemies for the current phase have been spawned and defeated
        # If so, call self.next_phase()
