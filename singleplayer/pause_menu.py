import pygame


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Resume", "Settings", "Quit to Menu", "Quit to Desktop"]
        self.rects = [pygame.Rect(200, 200 + i * 60, 200, 40) for i in range(len(self.options))]
        self.font = pygame.font.SysFont(None, 36)

    def draw(self):
        surf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        surf.fill((30, 30, 30, 128))
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(self.options):
            rect = self.rects[i]
            color = (0, 200, 0) if rect.collidepoint(mouse_pos) else (255, 255, 255)
            text_surf = self.font.render(option, True, color)
            text_rect = text_surf.get_rect(center=rect.center)
            pygame.draw.rect(surf, (50, 50, 50, 200), rect, border_radius=10)
            pygame.draw.rect(surf, (255, 255, 255, 255), rect, 2, border_radius=10)
            surf.blit(text_surf, text_rect)
        self.screen.blit(surf, (0, 0))

    def handle_click(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                return self.options[i]
        return None
