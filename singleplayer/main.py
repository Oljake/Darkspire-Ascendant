import pygame
import sys
import psutil
import time
from singleplayer.camera import Camera
from singleplayer.map import Map, Tile
from singleplayer.collision import Collision
from singleplayer.pause_menu import PauseMenu
from singleplayer.player import Player
from singleplayer.loading_status import LoadingStatus


class SingleplayerGame:
    def __init__(self, screen):
        self.screen = screen
        self.tile_size = 100  # Optimal for fewer blits
        self.map_width = 1_000_000
        self.map_height = 1_000_000
        self.player_width = 30
        self.player_height = 50
        self.player_speed = 5
        self.positions = {"player": (self.map_width * self.tile_size // 2, self.map_height * self.tile_size // 2)}

        self.map = Map(self.map_width, self.map_height, self.tile_size, self.positions["player"], seed=42, screen=self.screen)
        self.collision = Collision(self.map, self.player_width, self.player_height)
        self.camera = Camera(screen, self.map, self.player_width, self.player_height)
        self.player = Player(self.positions["player"][0], self.positions["player"][1], self.player_width,
                            self.player_height, self.player_speed)
        self.pause_menu = PauseMenu(screen)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.paused = False
        self.running = True
        self.loading = True
        self.loading_stage = 0
        self.loading_generators = []
        self.current_generator = None
        self.loading_progress = 0.0
        self.loading_texts = ["Loading initial chunks...", "Generating collision...", "Finalizing map..."]

        self.frame_buffer = None  # Cache for static map
        self.last_camera_pos = None  # Track camera movement
        self.last_player_pos = None  # Track player movement

        self.start_loading()

        self.process = psutil.Process()
        self.render_time = 0
        self.update_time = 0

    def start_loading(self):
        self.loading_stage = 0
        self.loading_generators = [
            self.map.load_step(),
            self._generate_collision(),
            self._finalize_map()
        ]
        self.current_generator = None
        self.loading_progress = 0.0
        LoadingStatus.set_status("Starting...")

    def _generate_collision(self):
        yield 0.5
        yield 1.0

    def _finalize_map(self):
        yield 0.5
        yield 1.0

    def generate_step(self):
        if self.current_generator is None:
            if self.loading_stage >= len(self.loading_generators):
                self.loading = False
                return
            self.current_generator = self.loading_generators[self.loading_stage]
            self.loading_progress = 0.0

        try:
            self.loading_progress = next(self.current_generator)
            self.draw_loading()
            pygame.time.wait(50)
        except StopIteration:
            self.loading_stage += 1
            self.current_generator = None
            self.loading_progress = 0.0

    def draw_loading(self):
        self.screen.fill((30, 30, 30))
        text = LoadingStatus.get_status()
        loading_surf = self.font.render(text, True, (255, 255, 255))
        rect = loading_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        self.screen.blit(loading_surf, rect)

        bar_width = self.screen.get_width() // 2
        bar_height = 30
        bar_x = self.screen.get_width() // 4
        bar_y = self.screen.get_height() // 2 + 10
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
        fill_width = int(bar_width * self.loading_progress)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, fill_width, bar_height), border_radius=5)

        pygame.display.flip()

    def run(self):
        self.accum_time = 0
        FIXED_UPDATE_TIME = 1000 / 60

        while self.running:
            dt = self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                    action = self.pause_menu.handle_click(event.pos)
                    if action == "Resume":
                        self.paused = False
                    elif action == "Quit to Menu":
                        self.running = False
                    elif action == "Quit to Desktop":
                        self.running = False
                        pygame.quit()
                        sys.exit()

            if self.loading:
                self.generate_step()
                continue

            update_start = time.time()
            if not self.paused:
                self.accum_time += dt
                while self.accum_time >= FIXED_UPDATE_TIME:
                    keys = pygame.key.get_pressed()
                    self.player.move(keys, self.collision)
                    self.accum_time -= FIXED_UPDATE_TIME
            self.update_time = time.time() - update_start

            render_start = time.time()
            current_camera_pos = self.camera.get_offset(self.player.get_pos())
            current_player_pos = self.player.get_pos()

            # Check if re-rendering is needed
            needs_render = (
                self.frame_buffer is None or
                self.last_camera_pos != current_camera_pos or
                self.last_player_pos != current_player_pos
            )

            if needs_render:
                self.map.clear_visible_cache()
                self.screen.fill((30, 30, 30))
                cx, cy = current_camera_pos
                tile_blits = []
                start_x = max(cx // self.tile_size, 0)
                end_x = min((cx + self.screen.get_width()) // self.tile_size + 1, self.map.width)
                start_y = max(cy // self.tile_size, 0)
                end_y = min((cy + self.screen.get_height()) // self.tile_size + 1, self.map.height)

                for y in range(int(start_y), int(end_y)):
                    for x in range(int(start_x), int(end_x)):
                        img = self.map.get_tile_image(x, y)
                        tile_blits.append((img, (x * self.tile_size - cx, y * self.tile_size - cy)))

                self.frame_buffer = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
                self.frame_buffer.blit(self.screen, (0, 0))
                self.screen.blits(tile_blits)
                self.player.draw(self.screen, (cx, cy))
                self.frame_buffer.blit(self.screen, (0, 0))  # Cache full frame
                self.last_camera_pos = current_camera_pos
                self.last_player_pos = current_player_pos
            else:
                self.screen.blit(self.frame_buffer, (0, 0))
                self.player.draw(self.screen, current_camera_pos)

            if self.paused:
                self.pause_menu.draw()

            fps_surf = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 0))
            memory = self.process.memory_info().rss / (1024 ** 3)
            mem_surf = self.font.render(f"App RAM: {memory:.3f} GB", True, (255, 255, 0))
            map_size_surf = self.font.render(f"Map: {self.map_width:,} x {self.map_height:,} tiles", True, (255, 255, 0))
            profile_surf = self.font.render(f"Update: {self.update_time*1000:.1f}ms Render: {self.render_time*1000:.1f}ms", True, (255, 255, 0))
            self.screen.blit(fps_surf, (5, 5))
            self.screen.blit(mem_surf, (5, 35))
            self.screen.blit(map_size_surf, (5, 65))
            self.screen.blit(profile_surf, (5, 95))
            self.render_time = time.time() - render_start

            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    game = SingleplayerGame(screen)
    game.run()
    pygame.quit()
    sys.exit()