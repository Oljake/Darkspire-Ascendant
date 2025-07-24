import numpy as np
import pygame
import os
from enum import IntEnum
from singleplayer.loading_status import LoadingStatus
import psutil

# Define tile types as Enum
class Tile(IntEnum):
    GROUND = 0
    WALL = 1

class Map:
    def __init__(self, width, height, tile_size, player_pos, seed=42):
        self.width, self.height, self.tile_size = width, height, tile_size
        self.player_pos = player_pos
        self.seed = seed
        self.chunk_size = 128  # Optimized for FPS
        self.chunk_cache = {}
        self.cache_limit = 16  # ~256 KB total (16 * 16 KB)
        self.chunk_dir = "chunks"
        os.makedirs(self.chunk_dir, exist_ok=True)

        # Cache tile images using Tile enum
        self.tile_images = {
            Tile.GROUND: pygame.Surface((self.tile_size, self.tile_size)),  # Ground
            Tile.WALL: pygame.Surface((self.tile_size, self.tile_size))     # Wall
        }
        self.tile_images[Tile.GROUND].fill((100, 100, 100))  # Gray
        self.tile_images[Tile.WALL].fill((200, 200, 200))    # Light gray

        self.loading_stage = 0
        self.total_chunks = (width // self.chunk_size + (1 if width % self.chunk_size else 0)) * (
            height // self.chunk_size + (1 if height % self.chunk_size else 0)
        )

    def load_step(self):
        if self.loading_stage == 0:
            LoadingStatus.set_status("Loading initial chunks...")
            px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
            cx, cy = px // self.chunk_size, py // self.chunk_size
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    self.get_chunk(cx + dx, cy + dy)
            self.loading_stage += 1
            yield 1.0
        return False

    def get_chunk(self, chunk_x, chunk_y):
        chunk_key = (chunk_x, chunk_y)
        if chunk_key in self.chunk_cache:
            return self.chunk_cache[chunk_key]

        chunk_file = os.path.join(self.chunk_dir, f"chunk_{chunk_x}_{chunk_y}.npy")
        if os.path.exists(chunk_file):
            chunk = np.load(chunk_file)
        else:
            chunk = self._generate_chunk(chunk_x, chunk_y)
            np.save(chunk_file, chunk)

        self.chunk_cache[chunk_key] = chunk
        if len(self.chunk_cache) > self.cache_limit:
            px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
            cx, cy = px // self.chunk_size, py // self.chunk_size
            distances = [(k, (k[0] - cx) ** 2 + (k[1] - cy) ** 2) for k in self.chunk_cache]
            farthest = max(distances, key=lambda x: x[1])[0]
            del self.chunk_cache[farthest]

        return chunk

    def _generate_chunk(self, chunk_x, chunk_y):
        rng = np.random.default_rng(self.seed + chunk_x * 10000 + chunk_y)
        chunk = np.zeros((self.chunk_size, self.chunk_size), dtype=np.uint8)
        random_walls = rng.random((self.chunk_size, self.chunk_size)) < 0.2
        chunk[random_walls] = Tile.WALL.value

        if chunk_y == 0:
            chunk[0, :] = Tile.WALL.value
        if chunk_y == (self.height // self.chunk_size):
            chunk[-1, :] = Tile.WALL.value
        if chunk_x == 0:
            chunk[:, 0] = Tile.WALL.value
        if chunk_x == (self.width // self.chunk_size):
            chunk[:, -1] = Tile.WALL.value

        px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
        px_chunk, py_chunk = px // self.chunk_size, py // self.chunk_size
        if chunk_x == px_chunk and chunk_y == py_chunk:
            local_px = px % self.chunk_size
            local_py = py % self.chunk_size
            y_start = max(0, local_py - 1)
            y_end = min(self.chunk_size, local_py + 2)
            x_start = max(0, local_px - 1)
            x_end = min(self.chunk_size, local_px + 2)
            chunk[y_start:y_end, x_start:x_end] = Tile.GROUND.value

        return chunk

    def get_tile(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return Tile.WALL
        chunk_x, chunk_y = x // self.chunk_size, y // self.chunk_size
        local_x, local_y = x % self.chunk_size, y % self.chunk_size
        chunk = self.get_chunk(chunk_x, chunk_y)
        return Tile(chunk[local_y, local_x])

    def get_tile_image(self, x, y, tile=None):
        if tile is None:
            tile = self.get_tile(x, y)
        return self.tile_images[tile]