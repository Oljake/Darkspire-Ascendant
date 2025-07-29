import pygame
from abilities.dash import Dash
from abilities.fireball import Fireball
from abilities.greater_fireball import GreaterFireball
from abilities.piercing_arrow import PiercingArrow
from abilities.upgrade_pools import upgrade_pools


class AbilityHandler:
    def __init__(self, player, collision):
        self.player = player
        self.collision = collision
        self.notifications = []  # (ability_name, timestamp)
        self.notification_duration = 3.0
        self.equipped_ability = None
        self.offensive_abilities = {"Fireball", "Greater Fireball", "Piercing Arrow"}
        self.ability_instances = {
            "Dash": Dash(player, collision),
            "Fireball": Fireball(player, collision),
            "Greater Fireball": GreaterFireball(player, collision),
            "Piercing Arrow": PiercingArrow(player, collision)
        }

        # Initialize dynamic abilities from upgrade_pools
        for abilities in upgrade_pools.values():
            for ability in abilities:
                name = ability["name"]
                if name not in self.ability_instances and name in globals():
                    instance = globals()[name.replace(' ', '')](player, collision)
                    self.ability_instances[name] = instance
                    if ability["type"] == "Offense":
                        self.offensive_abilities.add(name)

    def handle_abilities(self, keys, current_time):
        # Handle offensive ability switching
        unlocked_offensive = [a for a in self.offensive_abilities if self.player.has_ability(a)]
        if unlocked_offensive:
            # Number key switching
            for i, ability in enumerate(unlocked_offensive[:3]):  # Limit to 3 for keybinds
                if keys[pygame.K_1 + i]:
                    self.equipped_ability = ability

            # Scroll wheel switching
            for event in pygame.event.get(pygame.MOUSEWHEEL):
                current_index = unlocked_offensive.index(
                    self.equipped_ability) if self.equipped_ability in unlocked_offensive else 0
                self.equipped_ability = unlocked_offensive[(current_index + event.y) % len(unlocked_offensive)]

        # Handle ability input
        for ability_name, ability in self.ability_instances.items():
            if self.player.has_ability(ability_name):
                if ability_name == self.equipped_ability or ability_name not in self.offensive_abilities:
                    ability.handle_input(keys, current_time)

    def draw_cooldown_icons(self, screen, current_time):
        icon_size = 60
        equipped_scale = 1.2
        spacing = 70
        screen_width, screen_height = screen.get_size()

        # Separate abilities
        offensive = [a for a in self.ability_instances if self.player.has_ability(a) and a in self.offensive_abilities]
        non_offensive = [a for a in self.ability_instances if
                         self.player.has_ability(a) and a not in self.offensive_abilities]

        # Draw offensive abilities (bottom center)
        if offensive:
            total_width = sum(
                spacing if a != self.equipped_ability else spacing * equipped_scale for a in offensive) - (
                                      spacing - icon_size)
            start_x = screen_width // 2 - total_width // 2
            icon_y = screen_height - int(icon_size * equipped_scale) - 20

            current_x = start_x
            for ability_name in offensive:
                ability = self.ability_instances[ability_name]
                is_equipped = ability_name == self.equipped_ability
                size = (int(icon_size * equipped_scale), int(icon_size * equipped_scale)) if is_equipped else (
                icon_size, icon_size)
                icon = pygame.transform.scale(ability.icon, size)

                if ability.is_ready(current_time):
                    screen.blit(icon, (current_x, icon_y + (size[1] - icon_size) if is_equipped else icon_y))
                else:
                    cooldown_left = ability.cooldown - (current_time - ability.last_used)
                    faded = icon.copy()
                    faded.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(faded, (current_x, icon_y + (size[1] - icon_size) if is_equipped else icon_y))

                    font = pygame.font.SysFont("arial", 18)
                    text = font.render(f"{cooldown_left:.1f}s", True, (255, 255, 255))
                    screen.blit(text, text.get_rect(center=(current_x + size[0] / 2, icon_y + size[1] / 2)))

                current_x += spacing * equipped_scale if is_equipped else spacing

        # Draw non-offensive abilities (top right)
        if non_offensive:
            total_width = len(non_offensive) * spacing - (spacing - icon_size)
            start_x = screen_width - total_width - 20
            icon_y = 20

            for i, ability_name in enumerate(non_offensive):
                ability = self.ability_instances[ability_name]
                icon = ability.icon
                x = start_x + i * spacing

                if ability.is_ready(current_time):
                    screen.blit(icon, (x, icon_y))
                else:
                    cooldown_left = ability.cooldown - (current_time - ability.last_used)
                    faded = icon.copy()
                    faded.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(faded, (x, icon_y))

                    font = pygame.font.SysFont("arial", 18)
                    text = font.render(f"{cooldown_left:.1f}s", True, (255, 255, 255))
                    screen.blit(text, text.get_rect(center=(x + icon_size / 2, icon_y + icon_size / 2)))

        # Draw notifications
        notification_x = screen_width - 130
        notification_y = 20
        font = pygame.font.SysFont("arial", 16)
        self.notifications = [(n, t) for n, t in self.notifications if current_time - t < self.notification_duration]

        for ability_name, _ in self.notifications:
            ability = self.ability_instances[ability_name]
            screen.blit(ability.icon, (notification_x, notification_y))
            text = font.render("Unlocked!", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(notification_x + icon_size / 2, notification_y + icon_size + 10)))
            notification_y += spacing