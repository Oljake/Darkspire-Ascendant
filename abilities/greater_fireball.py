import pygame
import math

class GreaterFireball:
    def __init__(self, player, collision):
        self.player = player
        self.collision = collision
        # Load and cache images once
        self._icon = pygame.image.load("images/Abilities/Greater_Fireball.png").convert_alpha()
        self.icon = pygame.transform.scale(self._icon, (60, 60))
        self.projectile_sprite = pygame.transform.scale(self._icon, (30, 30))  # Larger size for projectile
        self.cooldown = 1.5
        self.last_used = 0.0
        self.speed = 300  # Pixels per second
        self.range = 4 * collision.map.tile_size  # 4 tiles
        self.projectiles = []  # List of active fireballs: {"pos": [x, y], "velocity": [vx, vy], "distance_traveled": float}

    def is_ready(self, current_time):
        """Check if the ability is off cooldown."""
        return current_time - self.last_used >= self.cooldown

    def handle_input(self, keys, current_time):
        """Handle input for firing Greater Fireball, disabled when card menu is active."""
        if not self.player.has_ability("Greater Fireball"):
            return
        if pygame.mouse.get_pressed()[0] and self.is_ready(current_time):
            mouse_pos = pygame.mouse.get_pos()
            player_screen_pos = self.player.rect.center  # Use rect.center directly
            direction = self.calculate_direction(player_screen_pos, mouse_pos)
            if direction:
                self.last_used = current_time
                self.fire(player_screen_pos, direction)

    def calculate_direction(self, start_pos, mouse_pos):
        """Calculate normalized direction vector from start_pos to mouse_pos."""
        dx, dy = mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)  # Faster than sqrt(dx**2 + dy**2)
        return (dx / distance, dy / distance) if distance > 0 else None

    def fire(self, start_pos, direction):
        """Create a new greater fireball projectile."""
        self.projectiles.append({
            "pos": list(start_pos),
            "velocity": [direction[0] * self.speed, direction[1] * self.speed],
            "distance_traveled": 0
        })

    def update(self, dt):
        """Update fireball positions and remove if out of range or colliding."""
        for fireball in self.projectiles[:]:
            fireball["pos"][0] += fireball["velocity"][0] * dt
            fireball["pos"][1] += fireball["velocity"][1] * dt
            fireball["distance_traveled"] += self.speed * dt

            if (fireball["distance_traveled"] >= self.range or
                self.collision.check(fireball["pos"][0], fireball["pos"][1])):
                self.projectiles.remove(fireball)

    def draw(self, screen, offset):
        """Draw active fireballs with rotated sprites."""
        for fireball in self.projectiles:
            angle = math.degrees(math.atan2(-fireball["velocity"][1], fireball["velocity"][0]))
            rotated_sprite = pygame.transform.rotate(self.projectile_sprite, angle)
            sprite_rect = rotated_sprite.get_rect(
                center=(int(fireball["pos"][0] - offset[0]), int(fireball["pos"][1] - offset[1]))
            )
            screen.blit(rotated_sprite, sprite_rect)