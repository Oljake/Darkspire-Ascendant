import pygame
import time


class Dash:
    def __init__(self, player, collision):
        self.player = player
        self.collision = collision
        self.icon = pygame.transform.scale(
            pygame.image.load("images/Abilities/Dash.png").convert_alpha(),
            (60, 60)
        )
        self.cooldown = 1.0  # 1 second cooldown
        self.last_used = 0.0
        self.double_shift_time = 0.3  # Max seconds between shift taps
        self.last_shift_time = 0.0
        self.shift_tap_count = 0
        self.last_shift_pressed = False

    def is_ready(self, current_time):
        """Check if the ability is off cooldown."""
        return current_time - self.last_used >= self.cooldown

    def handle_input(self, keys, current_time):
        """Handle input for the Dash ability."""
        if not self.player.has_ability("Dash"):
            return

        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        direction = None
        if keys[pygame.K_w]:
            direction = "up"
        elif keys[pygame.K_s]:
            direction = "down"
        elif keys[pygame.K_a]:
            direction = "left"
        elif keys[pygame.K_d]:
            direction = "right"

        # Handle double-tap logic
        if shift_pressed and not self.last_shift_pressed:  # Detect new Shift press
            if current_time - self.last_shift_time < self.double_shift_time:
                self.shift_tap_count += 1
            else:
                self.shift_tap_count = 1  # Start new tap sequence
            self.last_shift_time = current_time

        self.last_shift_pressed = shift_pressed

        # Trigger dash on second tap with direction and no cooldown
        if self.shift_tap_count >= 2 and direction and self.is_ready(current_time):
            self.execute(direction)
            self.last_used = current_time
            self.shift_tap_count = 0

        # Reset tap count if time window expires
        if current_time - self.last_shift_time >= self.double_shift_time and not shift_pressed:
            self.shift_tap_count = 0

    def execute(self, direction):
        """Execute the dash movement."""
        distance = self.player.speed * 50
        dx, dy = 0, 0

        if direction == "up":
            dy = -distance
        elif direction == "down":
            dy = distance
        elif direction == "left":
            dx = -distance
        elif direction == "right":
            dx = distance

        steps = 10
        step_dx = dx / steps
        step_dy = dy / steps

        for i in range(steps):
            new_x = self.player.rect.x + step_dx
            new_y = self.player.rect.y + step_dy
            if not self.collision.check(new_x, self.player.rect.y):
                self.player.rect.x = new_x
            if not self.collision.check(self.player.rect.x, new_y):
                self.player.rect.y = new_y
