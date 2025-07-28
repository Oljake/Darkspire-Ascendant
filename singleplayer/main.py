import pygame
import sys
from singleplayer.camera import Camera
from singleplayer.map import Map
from singleplayer.collision import Collision
from singleplayer.pause_menu import PauseMenu
from singleplayer.player import Player
from singleplayer.loading_status import LoadingStatus

class SingleplayerGame:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 128
        self.map_width = 100
        self.map_height = 100
        self.player_width = 40
        self.player_height = 50
        self.player_speed = 20
        self.noclip: bool = False
        self.positions = {"player": (self.map_width * self.tile_size // 2, self.map_height * self.tile_size // 2)}

        # Initialize systems
        self.map = Map(self.map_width, self.map_height, self.tile_size, self.positions["player"])
        self.collision = Collision(self.map, self.player_width, self.player_height)
        self.camera = Camera(screen, self.map, self.player_width, self.player_height)
        self.player = Player(self.positions["player"][0], self.positions["player"][1],
                            self.player_width, self.player_height, self.player_speed)
        self.pause_menu = PauseMenu(screen)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.fixed_dt = 1000 / 60  # Fixed timestep for 60 FPS updates (ms)
        self.accum_time = 0  # Accumulator for fixed-timestep updates

        self.paused = False
        self.running = True
        self.loading = True

        # Start map generation
        self.map.start_generation()
        LoadingStatus.set_status("Generating world...")

    def run(self):
        last_progress = 0.0

        while self.running:
            dt = self.clock.tick()  # No FPS cap for unlimited rendering

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_LALT:
                        self.noclip = not self.noclip
                elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                    action = self.pause_menu.handle_click(event.pos)
                    if action == "Resume":
                        self.paused = False
                    elif action == "Settings":
                        self.paused = False
                    elif action == "Quit to Menu":
                        self.running = False
                    elif action == "Quit to Desktop":
                        self.cleanup()
                        return

            if self.loading:
                raw_progress = self.map.get_generation_progress()
                if raw_progress == 1.0:
                    self.loading = False
                    self.collision.update_map(self.map)
                    last_progress = 1.0
                elif isinstance(raw_progress, float):
                    last_progress = raw_progress
                else:
                    last_progress = min(last_progress + 0.003, 0.99)

                self.draw_loading(last_progress)
                continue

            # Fixed-timestep movement updates
            if not self.paused:
                self.accum_time += dt
                while self.accum_time >= self.fixed_dt:
                    keys = pygame.key.get_pressed()
                    self.player.move(keys, self.collision, self.noclip)
                    self.accum_time -= self.fixed_dt

            # Render (unlimited FPS)
            self.screen.fill((30, 30, 30))
            cx, cy = self.camera.get_offset(self.player.get_pos())

            # Optimize tile rendering
            start_x = max(cx // self.tile_size, 0)
            end_x = min((cx + self.screen.get_width()) // self.tile_size + 1, self.map.width)
            start_y = max(cy // self.tile_size, 0)
            end_y = min((cy + self.screen.get_height()) // self.tile_size + 1, self.map.height)

            tile_blits = [
                (self.map.get_tile_image(x, y, self.map.map_data[y, x]),
                 (x * self.tile_size - cx, y * self.tile_size - cy))
                for y in range(start_y, end_y)
                for x in range(start_x, end_x)
            ]

            self.screen.blits(tile_blits)
            self.player.draw(self.screen, (cx, cy))

            if self.paused:
                self.pause_menu.draw()

            # Display FPS
            fps_surf = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 0))
            self.screen.blit(fps_surf, (5, 5))
            pygame.display.flip()

    def draw_loading(self, progress):
        self.screen.fill((30, 30, 30))
        dots = (pygame.time.get_ticks() // 400) % 4
        text = (LoadingStatus.get_status() or "Loading") + "." * dots

        # Render loading text
        loading_surf = self.font.render(text, True, (255, 255, 255))
        rect = loading_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        self.screen.blit(loading_surf, rect)

        # Render progress bar
        bar_width = self.screen.get_width() // 2
        bar_height = 30
        bar_x = self.screen.get_width() // 4
        bar_y = self.screen.get_height() // 2 + 10
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        fill_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=5)

        # Render percentage
        percent_surf = self.font.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        percent_rect = percent_surf.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        self.screen.blit(percent_surf, percent_rect)

        pygame.display.flip()

    def cleanup(self):
        self.map.stop_generation()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game = SingleplayerGame(screen)
    game.run()
    game.cleanup()