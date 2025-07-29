import pygame
import time


class Player:
    def __init__(self, x, y, width, height, stats, image_path="images/player/Thomas.png"):
        self.rect = pygame.Rect(x, y, width, height)
        raw_img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(raw_img, (width, height))

        # Base stats (do not modify directly)
        self.base_stats = {
            "Health": stats[0],
            "Speed": stats[1],
            "Attack": stats[2],
            "Attack Speed": stats[3],
            "Defense": 1.0,
            "Health Regen": 0.1  # Health regenerated per second
        }

        # Current stats (modified via upgrades)
        self.stats = self.base_stats.copy()

        # Abilities unlocked
        self.abilities = set()

        # Upgrade pool
        self.upgrades = []  # List to store applied upgrades
        self.applied_upgrades = set()  # Track non-stackable upgrades by name

        # Derived values
        self.max_health = self.stats["Health"]
        self.current_health = self.max_health
        self.speed = self.stats["Speed"]
        self.attack = self.stats["Attack"]
        self.attack_speed = self.stats["Attack Speed"]

        self._last_regen_time = time.time()  # Needed for health regen tracking

    def has_ability(self, name):
        return name in self.abilities

    def unlock_ability(self, name):
        self.abilities.add(name)

    def apply_upgrade(self, upgrade):
        """Apply an upgrade from the upgrade pool."""
        name = upgrade["name"]
        upgrade_type = upgrade["type"]
        stat = upgrade.get("stat")
        value = upgrade.get("value")
        stackable = upgrade.get("stackable", True)

        # Check if non-stackable and already applied
        if not stackable and name in self.applied_upgrades:
            return False

        # Check prerequisites for abilities
        if upgrade_type in ["Offense", "Utility"] and "prerequisite" in upgrade:
            if upgrade["prerequisite"] not in self.abilities:
                return False

        # Apply the upgrade
        if upgrade_type in ["Offense", "Utility"] and stat is None and value is None:
            # Unlock abilities (Fireball, Greater Fireball, Dash)
            self.unlock_ability(name)
            self.upgrades.append({"name": name, "value": ""})  # No value for abilities
            if not stackable:
                self.applied_upgrades.add(name)
            return True
        elif name == "Magic Armor" and upgrade_type == "Defense" and stat == "Defense" and value == "12%":
            # Increase defense by 12% (stackable)
            self.stats["Defense"] *= 1.12
            self.upgrades.append({"name": name, "value": value})
            return True
        return False

    def get_stats(self):
        return {
            "Health": self.max_health,
            "Current Health": self.current_health,
            "Speed": self.speed,
            "Attack": self.attack,
            "Attack Speed": self.attack_speed,
            "Defense": self.stats.get("Defense", 0),
            "Health Regen": self.stats.get("Health Regen", 0),
            "Upgrades": self.upgrades  # List of applied upgrades with names and values
        }

    def apply_effects(self):
        # Sync derived stats with current
        self.max_health = self.stats.get("Health", self.max_health)
        self.current_health = min(self.current_health, self.max_health)

        self.speed = max(0, self.stats.get("Speed", self.speed))
        self.attack = self.stats.get("Attack", self.attack)
        self.attack_speed = max(0.1, self.stats.get("Attack Speed", self.attack_speed))
        self.stats["Defense"] = max(0, self.stats.get("Defense", 0))

        # Health regen per second
        now = time.time()
        elapsed = now - self._last_regen_time
        if elapsed >= 1.0:
            regen_amount = self.stats.get("Health Regen", 0) * int(elapsed)
            if regen_amount > 0 and self.current_health < self.max_health:
                self.current_health = min(self.current_health + regen_amount, self.max_health)
            self._last_regen_time = now

    def move(self, keys, collision, noclip=False):
        dx = dy = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed

        if not noclip:
            if dx and not collision.check(self.rect.x + dx, self.rect.y):
                self.rect.x += dx
            if dy and not collision.check(self.rect.x, self.rect.y + dy):
                self.rect.y += dy
        else:
            self.rect.x += dx
            self.rect.y += dy

    def get_pos(self):
        return self.rect.x, self.rect.y

    def draw(self, screen, offset, stats_ui):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
        stats_ui.draw(screen, self.get_stats())