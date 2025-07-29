import pygame
import math
import time


class Fireball:
    def __init__(self, player, collision):
        self.player = player
        self.collision = collision
        self.icon = pygame.transform.scale(
            pygame.image.load("images/Abilities/Fireball.png").convert_alpha(),
            (60, 60)
        )
        # Load fireball sprite for projectiles
        self.projectile_sprite = pygame.transform.scale(
            pygame.image.load("images/Abilities/Fireball.png").convert_alpha(),
            (20, 20)  # Smaller size for fireball projectile
        )
        self.cooldown = 1.0
        self.last_used = 0.0
        self.speed = 300  # Pixels per second
        self.range = 2 * self.collision.map.tile_size  # 2 tiles
        self.projectiles = []  # List to store active fireballs (position, velocity, distance traveled)

    def is_ready(self, current_time):
        """Check if the ability is off cooldown."""
        return current_time - self.last_used >= self.cooldown

    def handle_input(self, keys, current_time):
        """Handle input for the Fireball ability."""
        if not self.player.has_ability("Fireball"):
            return
        if pygame.mouse.get_pressed()[0] and self.is_ready(current_time):
            mouse_pos = pygame.mouse.get_pos()
            player_screen_pos = (self.player.rect.centerx, self.player.rect.centery)  # Assume no camera offset for simplicity
            direction = self.calculate_direction(player_screen_pos, mouse_pos)
            if direction:  # Ensure valid direction
                self.last_used = current_time
                self.fire(player_screen_pos, direction)

    def calculate_direction(self, start_pos, mouse_pos):
        """Calculate normalized direction vector from start_pos to mouse_pos."""
        dx = mouse_pos[0] - start_pos[0]
        dy = mouse_pos[1] - start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return None
        return (dx / distance, dy / distance)

    def fire(self, start_pos, direction):
        """Create a new fireball projectile."""
        fireball = {
            "pos": list(start_pos),  # [x, y]
            "velocity": [direction[0] * self.speed, direction[1] * self.speed],  # Pixels per second
            "distance_traveled": 0
        }
        self.projectiles.append(fireball)

    def update(self, dt):
        """Update fireball positions and remove if they exceed range or hit a wall."""
        for fireball in self.projectiles[:]:  # Copy to allow removal
            fireball["pos"][0] += fireball["velocity"][0] * dt
            fireball["pos"][1] += fireball["velocity"][1] * dt
            fireball["distance_traveled"] += self.speed * dt

            # Check for collision or range limit
            if fireball["distance_traveled"] >= self.range or self.collision.check(fireball["pos"][0], fireball["pos"][1]):
                self.projectiles.remove(fireball)

    def draw(self, screen, offset):
        """Draw active fireballs with rotated sprites."""
        for fireball in self.projectiles:
            # Calculate rotation angle based on velocity
            angle = math.degrees(math.atan2(-fireball["velocity"][1], fireball["velocity"][0]))
            rotated_sprite = pygame.transform.rotate(self.projectile_sprite, angle)
            # Get the rotated sprite's rectangle to center it
            sprite_rect = rotated_sprite.get_rect(center=(int(fireball["pos"][0] - offset[0]), int(fireball["pos"][1] - offset[1])))
            screen.blit(rotated_sprite, sprite_rect)