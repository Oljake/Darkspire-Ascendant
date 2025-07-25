import pygame
import numpy as np
import threading
import queue
import psutil


class ImageLoader:
    def __init__(self):
        self.cache = {}

    def load(self, path):
        if path not in self.cache:
            self.cache[path] = pygame.image.load(path).convert_alpha()
        return self.cache[path]


class TileSet:
    def __init__(self, loader, map_data, tile_size, width, height):
        self.map_data = map_data
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tileset = loader.load('images/Tilesets/tileset.png')
        self.water = loader.load('images/Water/Water_0.png')
        self.ground = loader.load('images/Ground/Ground_19.png')

        # Scale images to match game tile size
        self.tileset = pygame.transform.scale(self.tileset, (
            self.tileset.get_width() * tile_size // 32,
            self.tileset.get_height() * tile_size // 32
        ))
        self.water = pygame.transform.scale(self.water, (tile_size, tile_size))
        self.ground = pygame.transform.scale(self.ground, (tile_size, tile_size))

        self.tileset_width, self.tileset_height = self.tileset.get_size()
        self.max_col = self.tileset_width // tile_size - 1
        self.max_row = self.tileset_height // tile_size - 1

    def get_tile(self, col, row):
        col = min(max(col, 0), self.max_col)
        row = min(max(row, 0), self.max_row)
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        return self.tileset.subsurface(rect)

    def check_water_sides(self, r, c):
        get = lambda rr, cc: 1 if 0 <= rr < self.height and 0 <= cc < self.width and self.map_data[rr, cc] == 1 else 0
        top = get(r - 1, c)
        bottom = get(r + 1, c)
        left = get(r, c - 1)
        right = get(r, c + 1)
        return top, bottom, left, right

    def get_autotile(self, r, c):
        t, b, l, r_ = self.check_water_sides(r, c)

        if t and b and l and r_: return self.get_tile(6, 1)
        if b and l and r_: return self.get_tile(3, 2)
        if t and l and r_: return self.get_tile(3, 0)
        if t and b and r_: return self.get_tile(6, 0)
        if t and b and l: return self.get_tile(4, 0)
        if b and r_: return self.get_tile(2, 2)
        if b and l: return self.get_tile(0, 2)
        if t and l: return self.get_tile(0, 0)
        if t and r_: return self.get_tile(2, 0)
        if l and r_: return self.get_tile(3, 1)
        if t and b: return self.get_tile(5, 0)
        if r_: return self.get_tile(2, 1)
        if l: return self.get_tile(0, 1)
        if b: return self.get_tile(1, 2)
        if t: return self.get_tile(1, 0)

        return self.ground

    def get_tile_image(self, x, y, tile):
        if tile == 1:
            return self.water
        else:
            if any(n == 1 for n in self.check_water_sides(y, x)):
                return self.get_autotile(y, x)
            return self.ground


class MapGenerator(threading.Thread):
    def __init__(self, width, height, chunk_size, player_pos, progress_queue):
        super().__init__()
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.player_pos = player_pos
        self.progress_queue = progress_queue
        self.map_data = np.zeros((self.height, self.width), dtype=np.uint8)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            # Generate random map: 0 = ground, 1 = water
            rng = np.random.default_rng()
            wall_mask = rng.random((self.height, self.width)) < 0.3  # 30% chance of water
            self.map_data = wall_mask.astype(np.uint8)

            # Process in chunks for memory efficiency
            total_chunks = (self.width // self.chunk_size + 1) * (self.height // self.chunk_size + 1)
            processed_chunks = 0
            update_interval = 16

            for cy in range(0, self.height, self.chunk_size):
                for cx in range(0, self.width, self.chunk_size):
                    if self._stop_event.is_set():
                        return
                    chunk_y_end = min(cy + self.chunk_size, self.height)
                    chunk_x_end = min(cx + self.chunk_size, self.width)
                    processed_chunks += 1
                    if processed_chunks % update_interval == 0 or processed_chunks == total_chunks:
                        self.progress_queue.put(processed_chunks / total_chunks)

            # Set map boundaries to water (1)
            self.map_data[0, :] = 1
            self.map_data[-1, :] = 1
            self.map_data[:, 0] = 1
            self.map_data[:, -1] = 1

            # Clear area around player (set to ground, 0)
            px, py = self.player_pos[0] // 100, self.player_pos[1] // 100
            y_start, y_end = max(0, py - 1), min(self.height, py + 2)
            x_start, x_end = max(0, px - 1), min(self.width, px + 2)
            self.map_data[y_start:y_end, x_start:x_end] = 0

            self.progress_queue.put(1.0)
        except Exception as e:
            self.progress_queue.put(("error", str(e)))


class Map:
    def __init__(self, width, height, tile_size, player_pos):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.player_pos = player_pos
        self.map_data = None
        self.chunk_size = 256
        self.progress_queue = queue.Queue()
        self.generator = None
        self.loader = ImageLoader()
        self.tileset = None

    def start_generation(self):
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        required_memory = (self.width * self.height * 1) / (1024 ** 3)
        if available_memory < required_memory * 1.5:
            raise MemoryError(
                f"Insufficient memory: {required_memory:.2f} GB required, {available_memory:.2f} GB available"
            )

        self.generator = MapGenerator(
            self.width, self.height,
            self.chunk_size, self.player_pos,
            self.progress_queue
        )
        self.generator.start()

    def stop_generation(self):
        if self.generator and self.generator.is_alive():
            self.generator.stop()
            self.generator.join()

    def get_generation_progress(self):
        try:
            progress = self.progress_queue.get_nowait()
            if isinstance(progress, tuple) and progress[0] == "error":
                raise RuntimeError(progress[1])
            if progress == 1.0:
                self.map_data = self.generator.map_data
                self.tileset = TileSet(self.loader, self.map_data, self.tile_size, self.width, self.height)
                self.generator.join()
                self.generator = None
            return progress
        except queue.Empty:
            return 0.0 if self.map_data is None else 1.0

    def get_tile_image(self, x, y, tile):
        if self.map_data is None or self.tileset is None:
            return self.loader.load('images/Ground/Ground_19.png')  # Fallback to ground
        return self.tileset.get_tile_image(x, y, tile)
