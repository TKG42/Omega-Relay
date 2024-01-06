class PhaseManager:
    def __init__(self, or_game):
        """Manages phases/levels of the game"""
        self.game = or_game
        self.current_phase = 1
        self.total_phases = 5 # Excluding boss fight
        self.aliens_spawned_this_phase = 0
        self.aliens_defeated_in_phase = 0

        # Define phase characteristics like enemy speed, spawn rates, etc.
        self.phase_configs = [
            {"speed_range": (1, 10), "spawn_rate": 12, "player_speed": 30, "bullet_speed": 30}, # Phase 1
             {"speed_range": (1, 15), "spawn_rate": 12, "player_speed": 30, "bullet_speed": 40}, # Phase 2
              {"speed_range": (5, 20), "spawn_rate": 12, "player_speed": 40, "bullet_speed": 50}, # Phase 3
               {"speed_range": (5, 20), "spawn_rate": 12, "player_speed": 40, "bullet_speed": 50, "enemy_bullet_speed": 30}, # Phase 4
                {"speed_range": (10, 25), "spawn_rate": 12, "player_speed": 50, "bullet_speed": 60, "enemy_bullet_speed": 40}, # Phase 5
             # ... Add configurations for each phase}
        ]

    def initiate_phase_change(self):
        """Initiate the phase change state."""
        self.game.state = "phase_change"
        self.game.sb.show_phase_level(self.current_phase)
        # ... any other setup for phase change

    def next_phase(self):
        """Transition to the next phase if there are remaining phases."""
        if self.current_phase < self.total_phases:
            self.current_phase += 1
            self.game.state = "phase_change"
            self.apply_phase_config()
            # Display new phase level in the center of the screen (HUD update)
            self.game.sb.show_phase_level(self.current_phase)
            # Reset the counter for the new phase
            self.aliens_spawned_this_phase = 0
            self.aliens_defeated_in_phase = 0

            # NOTE: debugging
            print(f"Transitioning to Phase {self.current_phase}")

    def apply_phase_config(self):
        """Apply the configurations for the current phase."""
        config = self.phase_configs[self.current_phase - 1]
        # Update the game settings based on phase configurations
        self.game.settings.alien_speed_range = config["speed_range"]
        self.game.settings.alien_spawn_rate = config["spawn_rate"]
        self.game.settings.ship_speed = config["player_speed"]
        self.game.settings.bullet_speed = config["bullet_speed"]

        # Apply additional phase-sepcific changes as needed
        if "enemy_bullet_speed" in config:
            self.game.settings.enemy_bullet_speed = config["enemy_bullet_speed"]
        
    def update(self):
        """Update phase-related conditions and check for phase completion."""
        current_config = self.phase_configs[self.current_phase - 1]
        # NOTE: debugging
        # print(f"Phase: {self.current_phase}, Spawned: {self.aliens_spawned_this_phase}, Defeated: {self.aliens_defeated_in_phase}, Spawn Rate: {current_config['spawn_rate']}")
        if (self.aliens_spawned_this_phase >= current_config["spawn_rate"]
            and self.game.aliens_defeated_in_phase >= self.aliens_spawned_this_phase):
            # Transition to the next phase if it exists
            self.next_phase()
            # Reset counters for the next phase
            self.aliens_spawned_this_phase = 0
            self.game.aliens_defeated_in_phase = 0

            # NOTE: debugging
            print("Updating PhaseManager...")
            print(f"Spawned: {self.aliens_spawned_this_phase}, Defeated: {self.game.aliens_defeated_in_phase}")
