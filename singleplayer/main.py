import pygame
import sys

# Internal modules
from singleplayer.camera import Camera
from singleplayer.map import Map
from singleplayer.collision import Collision
from singleplayer.pause_menu import PauseMenu
from singleplayer.player import Player
from singleplayer.loading_status import LoadingStatus
from singleplayer.event_handler import EventHandler
from singleplayer.renderer import Renderer
from singleplayer.loading_screen import LoadingScreen


class SingleplayerGame:
    def __init__(self, screen, tile_size):
        # --- Core game setup ---
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # Timing for fixed-step updates (60 updates/sec)
        self.fixed_dt = 1000 / 60
        self.accum_time = 0

        # --- Map and world configuration ---
        self.tile_size = tile_size
        self.map_width = 100
        self.map_height = 100

        # --- Player configuration ---
        self.player_width = 40
        self.player_height = 50
        self.player_speed = 20
        self.noclip = False  # Enables movement through collisions (if True)
        self.positions = {
            "player": (
                self.map_width * self.tile_size // 2,
                self.map_height * self.tile_size // 2
            )
        }

        # --- Game State Flags ---
        self.paused = False
        self.running = True
        self.loading = True

        # --- System and logic modules ---
        self.event_handler = EventHandler(self)
        self.loading_screen = LoadingScreen(screen, self.font)
        self.renderer = Renderer(self)

        # --- World objects ---
        self.map = Map(self.map_width, self.map_height, self.tile_size, self.positions["player"])
        self.collision = Collision(self.map, self.player_width, self.player_height)
        self.camera = Camera(screen, self.map, self.player_width, self.player_height)
        self.player = Player(
            self.positions["player"][0],
            self.positions["player"][1],
            self.player_width,
            self.player_height,
            self.player_speed
        )
        self.pause_menu = PauseMenu(screen)

        # --- Begin asynchronous map generation ---
        self.map.start_generation()
        LoadingStatus.set_status("Generating world...")

    def run(self):
        """Main game loop."""
        last_progress = 0.0

        while self.running:
            # Delta time for frame
            dt = self.clock.tick()

            # Handle input and system events
            self.event_handler.handle_events()

            # --- Loading phase ---
            if self.loading:
                raw_progress = self.map.get_generation_progress()

                # When loading is complete, finish setup
                if raw_progress == 1.0:
                    self.loading = False
                    self.collision.update_map(self.map)
                    last_progress = 1.0
                elif isinstance(raw_progress, float):
                    last_progress = raw_progress
                else:
                    # Fallback slow-fill progress
                    last_progress = min(last_progress + 0.003, 0.99)

                self.loading_screen.draw(last_progress)
                continue

            # --- Game update (physics, input) ---
            if not self.paused:
                self.accum_time += dt
                while self.accum_time >= self.fixed_dt:
                    keys = pygame.key.get_pressed()
                    self.player.move(keys, self.collision, self.noclip)
                    self.accum_time -= self.fixed_dt

            # --- Rendering ---
            self.renderer.render()

    def cleanup(self):
        """Gracefully shut down the game."""
        self.map.stop_generation()
        pygame.quit()
        sys.exit()


