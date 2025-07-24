import numpy as np
import pygame
import os
from enum import IntEnum
from singleplayer.loading_status import LoadingStatus
import psutil
from ui.tile_image_loader import TileImageLoader

class Tile(IntEnum):
    GROUND = 0
    WALL = 1

class Map:
    def __init__(self, width, height, tile_size, player_pos, seed=42, screen=None):
        self.width, self.height, self.tile_size = width, height, tile_size
        self.player_pos = player_pos
        self.seed = seed
        self.chunk_size = 128
        self.chunk_cache = {}  # (chunk_x, chunk_y) -> (tiles, indices)
        self.cache_limit = 8  # ~256 KB (8 × 32 KB)
        self.chunk_dir = "chunks"
        os.makedirs(self.chunk_dir, exist_ok=True)

        self.image_loader = TileImageLoader(tile_size, screen)
        self.ground_images = self.image_loader.load_series("Ground", "Ground_{}.png", 20)
        self.wall_images = self.image_loader.load_series("Maze_wall", "Maze_wall_{}.png", 10)

        self.visible_tile_cache = {}  # (x, y) -> image

        self.loading_stage = 0
        self.total_chunks = (width // self.chunk_size + (1 if width % self.chunk_size else 0)) * (
            height // self.chunk_size + (1 if height % self.chunk_size else 0)
        )

    def load_step(self):
        if self.loading_stage == 0:
            LoadingStatus.set_status("Loading initial chunks...")
            px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
            cx, cy = px // self.chunk_size, py // self.chunk_size
            for i, (dy, dx) in enumerate([(dy, dx) for dy in range(-1, 2) for dx in range(-1, 2)]):
                self.get_chunk(cx + dx, cy + dy)
                yield (i + 1) / 9
            self.loading_stage += 1
            yield 1.0
        return False

    def get_chunk(self, chunk_x, chunk_y):
        chunk_key = (chunk_x, chunk_y)
        if chunk_key in self.chunk_cache:
            return self.chunk_cache[chunk_key]

        chunk_file = os.path.join(self.chunk_dir, f"chunk_{chunk_x}_{chunk_y}.npy")
        indices_file = os.path.join(self.chunk_dir, f"chunk_indices_{chunk_x}_{chunk_y}.npy")
        if os.path.exists(chunk_file) and os.path.exists(indices_file):
            tiles = np.load(chunk_file)
            indices = np.load(indices_file)
        else:
            tiles, indices = self._generate_chunk(chunk_x, chunk_y)
            np.save(chunk_file, tiles)
            np.save(indices_file, indices)

        self.chunk_cache[chunk_key] = (tiles, indices)

        if len(self.chunk_cache) > self.cache_limit:
            px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
            cx, cy = px // self.chunk_size, py // self.chunk_size
            distances = [(k, (k[0] - cx) ** 2 + (k[1] - cy) ** 2) for k in self.chunk_cache]
            farthest = max(distances, key=lambda x: x[1])[0]
            del self.chunk_cache[farthest]

        return tiles, indices

    def _generate_chunk(self, chunk_x, chunk_y):
        rng = np.random.default_rng(self.seed + chunk_x * 10000 + chunk_y)
        tiles = np.zeros((self.chunk_size, self.chunk_size), dtype=np.uint8)
        indices = np.zeros((self.chunk_size, self.chunk_size), dtype=np.uint8)
        random_walls = rng.random((self.chunk_size, self.chunk_size)) < 0.2
        tiles[random_walls] = Tile.WALL.value
        indices[random_walls] = rng.integers(0, len(self.wall_images), size=(self.chunk_size, self.chunk_size))[random_walls]
        indices[~random_walls] = rng.integers(0, len(self.ground_images), size=(self.chunk_size, self.chunk_size))[~random_walls]

        if chunk_y == 0:
            tiles[0, :] = Tile.WALL.value
            indices[0, :] = rng.integers(0, len(self.wall_images), size=self.chunk_size)
        if chunk_y == (self.height // self.chunk_size):
            tiles[-1, :] = Tile.WALL.value
            indices[-1, :] = rng.integers(0, len(self.wall_images), size=self.chunk_size)
        if chunk_x == 0:
            tiles[:, 0] = Tile.WALL.value
            indices[:, 0] = rng.integers(0, len(self.wall_images), size=self.chunk_size)
        if chunk_x == (self.width // self.chunk_size):
            tiles[:, -1] = Tile.WALL.value
            indices[:, -1] = rng.integers(0, len(self.wall_images), size=self.chunk_size)

        px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
        px_chunk, py_chunk = px // self.chunk_size, py // self.chunk_size
        if chunk_x == px_chunk and chunk_y == py_chunk:
            local_px = px % self.chunk_size
            local_py = py % self.chunk_size
            y_start = max(0, local_py - 1)
            y_end = min(self.chunk_size, local_py + 2)
            x_start = max(0, local_px - 1)
            x_end = min(self.chunk_size, local_px + 2)
            tiles[y_start:y_end, x_start:x_end] = Tile.GROUND.value
            indices[y_start:y_end, x_start:x_end] = rng.integers(0, len(self.ground_images), size=(y_end - y_start, x_end - x_start))

        return tiles, indices

    def get_tile(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return Tile.WALL
        chunk_x, chunk_y = x // self.chunk_size, y // self.chunk_size
        local_x, local_y = x % self.chunk_size, y % self.chunk_size
        tiles, _ = self.get_chunk(chunk_x, chunk_y)
        return Tile(tiles[local_y, local_x])

    def get_tile_image(self, x, y, tile=None):
        if (x, y) in self.visible_tile_cache:
            return self.visible_tile_cache[(x, y)]

        if tile is None:
            tile = self.get_tile(x, y)
        chunk_x, chunk_y = x // self.chunk_size, y // self.chunk_size
        local_x, local_y = x % self.chunk_size, y % self.chunk_size
        _, indices = self.get_chunk(chunk_x, chunk_y)
        idx = indices[local_y, local_x]
        img = self.ground_images[idx] if tile == Tile.GROUND else self.wall_images[idx]
        self.visible_tile_cache[(x, y)] = img
        return img

    def clear_visible_cache(self):
        self.visible_tile_cache.clear()
