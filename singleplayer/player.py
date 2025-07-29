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
            "Mana": stats[2],
            "Attack": stats[3],
            "Attack Speed": stats[4],
            "Defense": 1.0,
            "Health Regen": 0.1
        }

        # Current stats (modified via upgrades)
        self.stats = self.base_stats.copy()

        # Abilities unlocked
        self.abilities = set()

        # Derived values
        self.max_health = self.stats["Health"]
        self.current_health = self.max_health

        self.max_mana = self.stats["Mana"]
        self.current_mana = self.max_mana

        self.speed = self.stats["Speed"]
        self.attack = self.stats["Attack"]
        self.attack_speed = self.stats["Attack Speed"]

        self._last_regen_time = time.time()  # Needed for health regen tracking

    def has_ability(self, name):
        return name in self.abilities

    def unlock_ability(self, name):
        self.abilities.add(name)

    def get_stats(self):
        return {
            "Health": self.max_health,
            "Current Health": self.current_health,
            "Speed": self.speed,
            "Mana": self.max_mana,
            "Attack": self.attack,
            "Attack Speed": self.attack_speed,
            "Defense": self.stats.get("Defense", 0),
            "Health Regen": self.stats.get("Health Regen", 0)
        }

    def apply_effects(self):
        # Sync derived stats with current
        self.max_health = self.stats.get("Health", self.max_health)
        self.current_health = min(self.current_health, self.max_health)

        self.max_mana = self.stats.get("Mana", self.max_mana)
        self.current_mana = min(self.current_mana, self.max_mana)

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

    def draw_stats(self, screen, pos=(10, 10), font=None, line_height=20):
        if font is None:
            font = pygame.font.SysFont('arial', 18)
        stats = self.get_stats()
        y = pos[1]

        # Draw each stat as "StatName: value"
        for key, value in stats.items():
            text_surf = font.render(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}", True,
                                    (255, 255, 255))
            screen.blit(text_surf, (pos[0], y))
            y += line_height


    def draw(self, screen, offset):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
        self.draw_stats(screen, pos=(1920/2-50, 200), font=pygame.font.SysFont('arial', 18))
