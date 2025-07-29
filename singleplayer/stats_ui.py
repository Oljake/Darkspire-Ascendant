import pygame


class StatsUI:
    def __init__(self, pos=(10, 10), font=None, line_height=30):
        self.pos = pos
        self.font = font if font else pygame.font.SysFont('arial', 24, bold=True)
        self.line_height = line_height
        self.panel_width = 250
        self.padding = 10

    def draw(self, screen, stats):
        """Draw the stats UI panel with health bar, stats, and upgrades."""
        panel_height = 130 + (self.line_height * len(stats["Upgrades"]))  # Reduced height (no mana bar)

        # Draw semi-transparent background panel
        panel = pygame.Surface((self.panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(panel, self.pos)

        # Draw health bar
        health_ratio = stats["Current Health"] / stats["Health"]
        health_bar_width = (self.panel_width - 2 * self.padding) * health_ratio
        pygame.draw.rect(screen, (255, 50, 50),
                         (self.pos[0] + self.padding, self.pos[1] + self.padding, health_bar_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (
        self.pos[0] + self.padding, self.pos[1] + self.padding, self.panel_width - 2 * self.padding, 20), 2)  # Border
        health_text = self.font.render(f"Health: {stats['Current Health']:.1f}/{stats['Health']:.1f}", True,
                                       (255, 255, 255))
        screen.blit(health_text, (self.pos[0] + self.padding, self.pos[1] + self.padding + 25))

        # Draw other stats
        y = self.pos[1] + self.padding + 50
        for key in ["Speed", "Attack", "Attack Speed", "Defense"]:
            value = stats[key]
            text_surf = self.font.render(f"{key}: {value:.2f}", True, (255, 255, 255))
            screen.blit(text_surf, (self.pos[0] + self.padding, y))
            y += self.line_height

        # Draw regeneration stats with units
        text_surf = self.font.render(f"Health Regen: {stats['Health Regen']:.2f}/s", True, (255, 255, 255))
        screen.blit(text_surf, (self.pos[0] + self.padding, y))
        y += self.line_height

        # Draw applied upgrades
        for upgrade in stats["Upgrades"]:
            value_str = f" ({upgrade['value']})" if upgrade["value"] else ""
            text_surf = self.font.render(f"{upgrade['name']}{value_str}", True, (255, 255, 255))
            screen.blit(text_surf, (self.pos[0] + self.padding, y))
            y += self.line_height