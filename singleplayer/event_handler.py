import pygame


class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.paused = not self.game.paused
                elif event.key == pygame.K_LALT:
                    self.game.noclip = not self.game.noclip
            elif event.type == pygame.MOUSEBUTTONDOWN and self.game.paused:
                action = self.game.pause_menu.handle_click(event.pos)
                if action == "Resume":
                    self.game.paused = False
                elif action == "Settings":
                    self.game.paused = False
                elif action == "Quit to Menu":
                    self.game.running = False
                elif action == "Quit to Desktop":
                    self.game.cleanup()
                    return
