import pygame
import random
import textwrap
from abilities.upgrade_pools import upgrade_pools

# Simplified card pools
heal_cards = [
    {"name": f"Heal {pct}%", "description": f"Heal {pct}% of max health", "type": "Support", "stackable": True}
    for pct in (25, 50, 75, 100)
]


class PlayerCardSystem:
    def __init__(self, player_class, player, screen_size):
        self.player_class = player_class.lower()
        self.player = player
        self.screen_width, self.screen_height = screen_size
        self.options = []
        self.font = pygame.font.SysFont("arial", 28, bold=True)
        self.desc_font = pygame.font.SysFont("arial", 20)

        # Precompute surface and dimensions
        self.surf = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.card_width, self.card_height = 250, 150
        self.card_margin = 15
        self.card_rects = []

    def generate_options(self):
        # Get class-specific upgrades
        class_pool = upgrade_pools.get(self.player_class, [])

        # Set descriptions for upgrades
        for upgrade in class_pool:
            if not upgrade.get("description"):
                stat, val = upgrade.get("stat"), upgrade.get("value")
                upgrade["description"] = f"+{val} {stat.lower()}" if stat and val is not None else "Special ability"

        # Filter available upgrades
        available = [
            u for u in class_pool + heal_cards
            if u.get("stackable", False) or not self.player.has_ability(u["name"])
        ]

        # Select up to 3 random options
        self.options = random.sample(available, min(3, len(available))) if available else []

    def apply_upgrade(self, index):
        if not (0 <= index < len(self.options)):
            return

        upgrade = self.options[index]
        name = upgrade["name"]
        self.player.unlock_ability(name)
        print(f"Applied upgrade: {name}")

        # Handle stat-based upgrades
        if (stat := upgrade.get("stat")) and (value := upgrade.get("value")) is not None:
            current_val = self.player.stats.get(stat, 0)
            add_val = float(value.strip("%")) / 100 * current_val if isinstance(value, str) and "%" in value else float(
                value)
            new_val = current_val + add_val
            self.player.stats[stat] = new_val

            if stat == "Health":
                old_max = self.player.max_health
                self.player.max_health = new_val
                self.player.current_health = min(self.player.current_health + (new_val - old_max), new_val)
                print(f"Healed for {new_val - old_max:.1f} HP")
            else:
                print(f"{stat} increased by {add_val:.1f} → {new_val:.1f}")

        # Handle heal cards
        elif "Heal" in name:
            percent = int(''.join(filter(str.isdigit, name))) / 100 if "Heal" in name else 0.25
            heal_amount = int(self.player.max_health * percent)
            self.player.current_health = min(self.player.current_health + heal_amount, self.player.max_health)
            print(f"Healed for {heal_amount} HP")

        self.player.apply_effects()
        self.options = []

    def draw(self, screen):
        self.surf.fill((30, 30, 30, 160))
        self.card_rects.clear()

        total_width = 3 * self.card_width + 2 * self.card_margin
        start_x = (self.screen_width - total_width) // 2
        y = (self.screen_height - self.card_height) // 2

        for i, option in enumerate(self.options):
            x = start_x + i * (self.card_width + self.card_margin)
            rect = pygame.Rect(x, y, self.card_width, self.card_height)
            self.card_rects.append(rect)

            # Draw card with hover effect
            bg_color = (110, 110, 110, 240) if rect.collidepoint(pygame.mouse.get_pos()) else (90, 90, 90, 220)
            pygame.draw.rect(self.surf, bg_color, rect, border_radius=12)
            pygame.draw.rect(self.surf, (200, 200, 200), rect, 3, border_radius=12)

            # Render type
            if type_text := option.get("type"):
                type_surf = self.font.render(type_text, True, (180, 180, 250))
                self.surf.blit(type_surf, type_surf.get_rect(center=(rect.centerx, rect.top + 25)))

            # Render title
            title_surf = self.font.render(option["name"], True, (255, 255, 255))
            self.surf.blit(title_surf, title_surf.get_rect(center=(rect.centerx, rect.top + 60)))

            # Render description with wrapping
            for i, line in enumerate(textwrap.wrap(option["description"], width=28)):
                desc_surf = self.desc_font.render(line, True, (200, 200, 200))
                self.surf.blit(desc_surf, desc_surf.get_rect(
                    center=(rect.centerx, rect.top + 90 + i * self.desc_font.get_linesize())))

        screen.blit(self.surf, (0, 0))

    def handle_click(self, mouse_pos):
        for i, rect in enumerate(self.card_rects):
            if rect.collidepoint(mouse_pos):
                self.apply_upgrade(i)
                return True
        return False