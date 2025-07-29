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
from singleplayer.playercards import PlayerCardSystem  # NEW
from singleplayer.abilities import AbilityHandler


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
        self.player_stats = [100, 5, 20, 10, 1.0]
        self.noclip = False
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
        self.showing_upgrade_screen = False  # NEW

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
            self.player_stats
        )
        self.ability_handler = AbilityHandler(self.player, self.collision)

        # Assign player class as 'mage' and create upgrade system
        self.player.player_class = "Knight"  # You might already have this inside Player
        self.player_card_system = PlayerCardSystem("mage", self.player, self.screen.get_size())  # mage archer knight

        self.pause_menu = PauseMenu(screen)

        # --- Begin asynchronous map generation ---
        self.map.start_generation()
        LoadingStatus.set_status("Generating world...")

    def run(self):
        """Main game loop."""
        last_progress = 0.0

        while self.running:
            dt = self.clock.tick()
            self.event_handler.handle_events()

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

                self.loading_screen.draw(last_progress)
                continue

            if not self.paused and not self.showing_upgrade_screen:
                self.accum_time += dt
                while self.accum_time >= self.fixed_dt:
                    keys = pygame.key.get_pressed()
                    current_time = pygame.time.get_ticks() / 1000  # ← seconds

                    if hasattr(self, "ability_handler"):
                        self.ability_handler.handle_dash(keys, current_time)

                    self.player.move(keys, self.collision, self.noclip)
                    self.accum_time -= self.fixed_dt

            self.renderer.render()

            if self.showing_upgrade_screen:
                self.player_card_system.draw(self.screen)

            current_time = pygame.time.get_ticks() / 1000
            if hasattr(self, "ability_handler"):
                self.ability_handler.draw_cooldown_icons(self.screen, current_time)

            pygame.display.flip()

    def cleanup(self):
        """Gracefully shut down the game."""
        self.map.stop_generation()
        pygame.quit()
        sys.exit()
