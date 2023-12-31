from game_state import GameState

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
        self.game.state = GameState.PHASE_CHANGE
        self.game.sb.show_phase_level(self.current_phase)
        # ... any other setup for phase change

    def next_phase(self):
        """Transition to the next phase if there are remaining phases."""
        if self.current_phase < self.total_phases:
            self.current_phase += 1

            # Ensure all settings and counters are reset before updating
            self.apply_phase_config()
            self.reset_phase_counters()

            # Display new phase level in the center of the screen (HUD update)
            self.game.state = GameState.PHASE_CHANGE
            self.game.sb.show_phase_level(self.current_phase)
            # Reset the counter for the new phase
                    
    def reset_phase_counters(self):
        """Reset the counters for aliens spawned and defeated in the current phase."""
        self.aliens_spawned_this_phase = 0
        self.game.aliens_defeated_in_phase = 0
        # NOTE: debugging
        print(f"Transitioning to Phase {self.current_phase}")

    def should_change_phase(self):
        """Determine if a phase change should occur."""
        current_config = self.phase_configs[self.current_phase - 1]
        return (self.aliens_spawned_this_phase >= current_config["spawn_rate"] and
                self.game.aliens_defeated_in_phase >= self.aliens_spawned_this_phase)

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
        if self.should_change_phase():
            self.next_phase()

            # Reset counters for the next phase
            # self.aliens_spawned_this_phase = 0
            # self.game.aliens_defeated_in_phase = 0
            self.reset_phase_counters()

            # NOTE: debugging
            print("Updating PhaseManager...")
            print(f"Spawned: {self.aliens_spawned_this_phase}, Defeated: {self.game.aliens_defeated_in_phase}")
