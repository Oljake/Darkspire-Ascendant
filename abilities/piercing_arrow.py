import pygame
import time


class PiercingArrow:
    def __init__(self, player, collision):
        self.player = player
        self.collision = collision
        self.icon = pygame.transform.scale(
            pygame.image.load("images/Abilities/Piercing_Arrow.png").convert_alpha(),
            (60, 60)
        )
        self.cooldown = 1.0
        self.last_used = 0.0

    def is_ready(self, current_time):
        """Check if the ability is off cooldown."""
        return current_time - self.last_used >= self.cooldown

    def handle_input(self, keys, current_time):
        """Handle input for the Piercing Arrow ability."""
        if not self.player.has_ability("Piercing Arrow"):
            return
        # Add input logic (e.g., key press to shoot arrow)
        if keys[pygame.K_p] and self.is_ready(current_time):  # Example: 'P' key to shoot
            print("Shooting Piercing Arrow!")
            self.execute()
            self.last_used = current_time

    def execute(self):
        """Execute the piercing arrow ability."""
        # Implement piercing arrow logic
        pass