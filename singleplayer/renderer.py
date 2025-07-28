import pygame
import psutil
import os


class Renderer:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        self.process = psutil.Process(os.getpid())

        # Cache and previous values
        self.cached_fps_surf = None
        self.cached_mem_surf = None
        self.prev_fps = -1
        self.prev_mem = -1

        self.frame_counter = 0
        self.update_interval = 30  # Update stats every 30 frames

    def render(self):
        game = self.game
        screen = game.screen
        screen.fill((30, 30, 30))

        cx, cy = game.camera.get_offset(game.player.get_pos())

        # Optimize tile rendering
        start_x = max(cx // game.tile_size, 0)
        end_x = min((cx + screen.get_width()) // game.tile_size + 1, game.map.width)
        start_y = max(cy // game.tile_size, 0)
        end_y = min((cy + screen.get_height()) // game.tile_size + 1, game.map.height)

        tile_blits = [
            (game.map.get_tile_image(x, y, game.map.map_data[y, x]),
             (x * game.tile_size - cx, y * game.tile_size - cy))
            for y in range(start_y, end_y)
            for x in range(start_x, end_x)
        ]

        screen.blits(tile_blits)
        game.player.draw(screen, (cx, cy))

        if game.paused:
            game.pause_menu.draw()

        self.draw_stats()

        pygame.display.flip()

    def draw_stats(self):
        self.frame_counter += 1
        if self.frame_counter >= self.update_interval:
            self.frame_counter = 0

            # Rounded values to avoid frequent redraws
            fps = int(round(self.game.clock.get_fps() / 5.0) * 5)
            mem_mb = round(self.process.memory_info().rss / 1024 / 1024, 1)

            if fps != self.prev_fps:
                self.cached_fps_surf = self.font.render(f"FPS: {fps}", True, (255, 255, 0))
                self.prev_fps = fps

            if mem_mb != self.prev_mem:
                self.cached_mem_surf = self.font.render(f"RAM: {mem_mb:.1f} MB", True, (0, 255, 255))
                self.prev_mem = mem_mb

        # Blit the last cached values
        if self.cached_mem_surf:
            self.game.screen.blit(self.cached_mem_surf, (5, 5))
        if self.cached_fps_surf:
            self.game.screen.blit(self.cached_fps_surf, (5, 40))