import pygame
import random
import textwrap
from singleplayer.upgrade_pools import upgrade_pools

# A global heal_cards and other_cards list for use in generate_options
# You can customize these pools or load dynamically as well
heal_cards = [
    {"name": "Heal 25%", "description": None, "type": "Support", "stackable": True, "stat": None, "value": None},
    {"name": "Heal 50%", "description": None, "type": "Support", "stackable": True, "stat": None, "value": None},
    {"name": "Heal 75%", "description": None, "type": "Support", "stackable": True, "stat": None, "value": None},
    {"name": "Heal 100%", "description": None, "type": "Support", "stackable": True, "stat": None, "value": None},
]

other_cards = []
for cls_pool in upgrade_pools.values():
    for upgrade in cls_pool:
        if not any(upgrade["name"] == h["name"] for h in heal_cards):
            other_cards.append(upgrade)

class PlayerCardSystem:
    def __init__(self, player_class, player, screen_size):
        self.player_class = player_class
        self.player = player
        self.options = []
        self.font = pygame.font.SysFont("arial", 28)
        self.desc_font = pygame.font.SysFont("arial", 22)
        self.screen_width, self.screen_height = screen_size

        self.card_width = 260
        self.card_height = 160
        self.card_margin = 20

        self.surf = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.surf.fill((30, 30, 30, 160))  # Semi-transparent background

        self.card_rects = []  # Track clickable card positions

        self.upgrade_pools = upgrade_pools

    def generate_options(self):
        # Ensure descriptions are set
        class_pool = self.upgrade_pools.get(self.player_class.lower(), [])
        for upgrade in class_pool:
            if upgrade.get("description") is None:
                val = upgrade.get("value")
                stat = upgrade.get("stat")
                if stat and val is not None:
                    upgrade["description"] = f"+ {val} {stat.lower()}"
                else:
                    upgrade["description"] = "Special ability"

        for heal in heal_cards:
            if heal.get("description") is None:
                heal["description"] = heal["name"]

        # Pool: Knight abilities only + heal
        chosen_heal = random.sample(heal_cards, 1) if heal_cards else []
        combined = class_pool + chosen_heal

        self.options = random.sample(combined, min(3, len(combined)))

    def apply_upgrade(self, index):
        if 0 <= index < len(self.options):
            upgrade = self.options[index]
            name = upgrade["name"]
            print(name)
            print(f"\nApplying upgrade: {name}")
            self.player.unlock_ability(name)

            stat = upgrade.get("stat")
            value = upgrade.get("value")

            if stat and value is not None:
                current_val = self.player.stats.get(stat, 0)
                base_val = self.player.base_stats.get(stat, current_val)

                # Calculate value to add
                if isinstance(value, str) and value.endswith("%"):
                    try:
                        percent_val = float(value.strip("%")) / 100
                        add_val = current_val * percent_val  # Use current_val here for stacking
                    except Exception:
                        add_val = 0
                else:
                    try:
                        add_val = float(value)
                    except Exception:
                        add_val = 0

                new_val = current_val + add_val
                self.player.stats[stat] = new_val

                # If Health, apply to max_health and heal the difference
                if stat == "Health":
                    old_max = self.player.max_health
                    self.player.max_health = new_val
                    heal_amount = self.player.max_health - old_max
                    self.player.current_health = min(self.player.current_health + heal_amount, self.player.max_health)
                    print(f"Healed for {heal_amount} HP.")
                else:
                    print(f"{stat} increased by {add_val:.2f} → {self.player.stats[stat]:.2f}")

            elif "Heal" in name:
                # Special heal cards (e.g., Heal 25%)
                try:
                    percent = int(''.join(filter(str.isdigit, name))) / 100
                except Exception:
                    percent = 0.25  # fallback

                heal_amount = int(self.player.max_health * percent)
                self.player.current_health = min(self.player.current_health + heal_amount, self.player.max_health)
                print(f"Healed for {heal_amount} HP.")

            self.player.apply_effects()

            self.options = []

    def draw(self, screen):
        self.surf.fill((30, 30, 30, 160))
        self.card_rects = []

        total_width = 3 * self.card_width + 2 * self.card_margin
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height // 2 - self.card_height // 2

        for i, option in enumerate(self.options):
            x = start_x + i * (self.card_width + self.card_margin)
            rect = pygame.Rect(x, y, self.card_width, self.card_height)
            self.card_rects.append(rect)

            mouse_pos = pygame.mouse.get_pos()
            hover = rect.collidepoint(mouse_pos)

            bg_color = (90, 90, 90, 220) if not hover else (110, 110, 110, 240)
            pygame.draw.rect(self.surf, bg_color, rect, border_radius=12)
            pygame.draw.rect(self.surf, (200, 200, 200), rect, 3, border_radius=12)

            type_text = option.get("type", "")
            if type_text:
                type_surf = self.font.render(type_text, True, (180, 180, 250))
                self.surf.blit(type_surf, type_surf.get_rect(center=(rect.centerx, rect.top + 25)))

            title_surf = self.font.render(option["name"], True, (255, 255, 255))
            self.surf.blit(title_surf, title_surf.get_rect(center=(rect.centerx, rect.top + 60)))

            desc_lines = textwrap.wrap(option["description"], width=30)
            line_height = self.desc_font.get_linesize()
            for line_i, line in enumerate(desc_lines):
                desc_surf = self.desc_font.render(line, True, (200, 200, 200))
                desc_y = rect.top + 90 + line_i * line_height
                self.surf.blit(desc_surf, desc_surf.get_rect(center=(rect.centerx, desc_y)))

        screen.blit(self.surf, (0, 0))

    def handle_click(self, mouse_pos):
        for i, rect in enumerate(self.card_rects):
            if rect.collidepoint(mouse_pos):
                self.apply_upgrade(i)
                return True
        return False
