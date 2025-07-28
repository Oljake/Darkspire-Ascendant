# loading_screen.py
import pygame
from singleplayer.loading_status import LoadingStatus

class LoadingScreen:
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font or pygame.font.SysFont(None, 36)

    def draw(self, progress):
        self.screen.fill((30, 30, 30))
        dots = (pygame.time.get_ticks() // 400) % 4
        text = (LoadingStatus.get_status() or "Loading") + "." * dots

        # Loading text
        loading_surf = self.font.render(text, True, (255, 255, 255))
        rect = loading_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        self.screen.blit(loading_surf, rect)

        # Progress bar
        bar_width = self.screen.get_width() // 2
        bar_height = 30
        bar_x = self.screen.get_width() // 4
        bar_y = self.screen.get_height() // 2 + 10
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        fill_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=5)

        # Percentage
        percent_surf = self.font.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        percent_rect = percent_surf.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        self.screen.blit(percent_surf, percent_rect)

        pygame.display.flip()
