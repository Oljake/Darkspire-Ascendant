import pygame
import time


class AbilityHandler:
    def __init__(self, player, collision):
        self.player = player
        self.collision = collision
        self.double_shift_time = 0.3  # Max seconds between shift taps
        self.last_shift_time = 0.0
        self.shift_tap_count = 0
        self.last_dir_pressed = None
        self.last_shift_pressed = False
        self.notifications = []  # List to store (ability_name, timestamp) for notifications
        self.notification_duration = 3.0  # Seconds to show notification

        # Dictionary to store ability data: icon, cooldown, last used time
        self.abilities = {
            "Dash": {
                "icon": pygame.transform.scale(
                    pygame.image.load("images/Abilities/Dash.png").convert_alpha(),
                    (60, 60)
                ),
                "cooldown": 1.0,  # 1 second cooldown
                "last_used": 0.0
            },
            "Fireball": {
                "icon": pygame.transform.scale(
                    pygame.image.load("images/Abilities/Fireball.png").convert_alpha(),
                    (60, 60)
                ),
                "cooldown": 1.0,
                "last_used": 0.0
            },
            "Greater Fireball": {
                "icon": pygame.transform.scale(
                    pygame.image.load("images/Abilities/Greater_Fireball.png").convert_alpha(),
                    (60, 60)
                ),
                "cooldown": 1.5,
                "last_used": 0.0
            },
            "Piercing Arrow": {
                "icon": pygame.transform.scale(
                    pygame.image.load("images/Abilities/Piercing_Arrow.png").convert_alpha(),
                    (60, 60)
                ),
                "cooldown": 1.0,  # Placeholder; adjust as needed
                "last_used": 0.0
            }
        }

    def add_notification(self, ability_name):
        """Add a notification for a newly unlocked ability."""
        if ability_name in self.abilities:
            self.notifications.append((ability_name, time.time()))

    def handle_dash(self, keys, current_time):
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
            print(
                f"Shift tap count: {self.shift_tap_count}, Time since last shift: {current_time - self.last_shift_time:.3f}s")

        self.last_shift_pressed = shift_pressed

        # Trigger dash on second tap with direction and no cooldown
        if self.shift_tap_count >= 2 and direction and current_time - self.abilities["Dash"]["last_used"] >= \
                self.abilities["Dash"]["cooldown"]:
            print(f"Dashing! Time since last dash: {current_time - self.abilities['Dash']['last_used']:.3f}s")
            self.dash(direction)
            self.abilities["Dash"]["last_used"] = current_time
            self.shift_tap_count = 0
        elif self.shift_tap_count >= 2 and direction:
            print(
                f"Cannot dash, cooldown remaining: {self.abilities['Dash']['cooldown'] - (current_time - self.abilities['Dash']['last_used']):.3f}s")

        # Reset tap count if time window expires
        if current_time - self.last_shift_time >= self.double_shift_time and not shift_pressed:
            self.shift_tap_count = 0

    def is_ability_ready(self, ability_name, current_time):
        return current_time - self.abilities[ability_name]["last_used"] >= self.abilities[ability_name]["cooldown"]

    def dash(self, direction):
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

    def draw_cooldown_icons(self, screen, current_time):
        icon_x = screen.get_width() - 70  # Adjusted for 60x60 icons
        icon_y = 20
        spacing = 70  # Increased spacing for larger icons
        icon_width, icon_height = 60, 60  # Fixed size for all icons

        # Draw icons for abilities the player has, using index of unlocked abilities
        unlocked_abilities = [ability for ability in self.abilities if self.player.has_ability(ability)]
        for i, ability_name in enumerate(unlocked_abilities):
            y_position = icon_y + i * spacing
            if self.is_ability_ready(ability_name, current_time):
                # Draw normal icon
                screen.blit(self.abilities[ability_name]["icon"], (icon_x, y_position))
            else:
                # Draw faded icon with cooldown text
                cooldown_left = self.abilities[ability_name]["cooldown"] - (
                            current_time - self.abilities[ability_name]["last_used"])
                faded = self.abilities[ability_name]["icon"].copy()
                faded.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(faded, (icon_x, y_position))

                # Draw cooldown text centered on the icon
                font = pygame.font.SysFont("arial", 20)
                text = font.render(f"{cooldown_left:.1f}s", True, (255, 255, 255))
                text_rect = text.get_rect(center=(icon_x + icon_width / 2, y_position + icon_height / 2))
                screen.blit(text, text_rect)

        # Draw notifications for newly unlocked abilities, starting from the top
        notification_x = screen.get_width() - 130  # Left of the cooldown icons
        notification_y = 20  # Start at the top, same as first cooldown icon
        valid_notifications = []
        for ability_name, timestamp in self.notifications:
            if current_time - timestamp < self.notification_duration:
                screen.blit(self.abilities[ability_name]["icon"], (notification_x, notification_y))
                # Draw "Unlocked!" text below the icon
                font = pygame.font.SysFont("arial", 16)
                text = font.render("Unlocked!", True, (255, 255, 255))
                text_rect = text.get_rect(center=(notification_x + icon_width / 2, notification_y + icon_height + 10))
                screen.blit(text, text_rect)
                valid_notifications.append((ability_name, timestamp))
                notification_y += spacing  # Move down for the next notification
        self.notifications = valid_notifications  # Update list to remove expired notifications