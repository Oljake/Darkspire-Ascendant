import pygame
import numpy as np
import threading
import queue
import psutil
from singleplayer.loading_status import LoadingStatus


class ImageLoader:
    def __init__(self):
        self.cache = {}

    def load(self, path, tile_size=None):
        """Load and optionally scale image, caching the result."""
        cache_key = (path, tile_size) if tile_size else path
        if cache_key not in self.cache:
            image = pygame.image.load(path).convert_alpha()
            if tile_size:
                image = pygame.transform.scale(image, (tile_size, tile_size))
            self.cache[cache_key] = image
        return self.cache[cache_key]


class TileSet:
    def __init__(self, loader, map_data, tile_size, width, height):
        self.map_data = map_data
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Load and scale images to match original behavior
        self.tileset = loader.load('images/Tilesets/tileset.png').convert()
        self.water = loader.load('images/Water/Water_0.png', tile_size).convert()
        self.ground = loader.load('images/Ground/Ground_19.png', tile_size).convert()

        # Scale tileset to match original scaling
        self.tileset = pygame.transform.scale(
            self.tileset,
            (self.tileset.get_width() * tile_size // 32,
             self.tileset.get_height() * tile_size // 32)
        )
        self.tileset_width, self.tileset_height = self.tileset.get_size()
        self.max_col = self.tileset_width // tile_size - 1
        self.max_row = self.tileset_height // tile_size - 1

        # Cache for autotile results
        self.autotile_cache = {}

        # Precompute all tiles
        self.tile_cache = {}
        for row in range(self.max_row + 1):
            for col in range(self.max_col + 1):
                rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                self.tile_cache[(col, row)] = self.tileset.subsurface(rect)

        # Precompute autotiling for entire map
        self.autotile_map = self.autotile_map()


    def get_tile(self, col, row):
        """Extract a specific tile from the tileset."""
        col = min(max(col, 0), self.max_col)
        row = min(max(row, 0), self.max_row)
        rect = pygame.Rect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
        return self.tileset.subsurface(rect)

    def check_water_sides(self, r, c):
        """Check neighboring tiles for water."""

        def get(rr, cc):
            return 1 if 0 <= rr < self.height and 0 <= cc < self.width and self.map_data[rr, cc] == 1 else 0

        return get(r - 1, c), get(r + 1, c), get(r, c - 1), get(r, c + 1)

    def get_autotile(self, r, c):
        """Return appropriate tile based on neighboring water tiles with caching."""
        cache_key = (r, c)
        if cache_key in self.autotile_cache:
            return self.autotile_cache[cache_key]

        t, b, l, r_ = self.check_water_sides(r, c)
        if t and b and l and r_:
            tile = self.get_tile(6, 1)
        elif b and l and r_:
            tile = self.get_tile(3, 2)
        elif t and l and r_:
            tile = self.get_tile(3, 0)
        elif t and b and r_:
            tile = self.get_tile(6, 0)
        elif t and b and l:
            tile = self.get_tile(4, 0)
        elif b and r_:
            tile = self.get_tile(2, 2)
        elif b and l:
            tile = self.get_tile(0, 2)
        elif t and l:
            tile = self.get_tile(0, 0)
        elif t and r_:
            tile = self.get_tile(2, 0)
        elif l and r_:
            tile = self.get_tile(3, 1)
        elif t and b:
            tile = self.get_tile(5, 0)
        elif r_:
            tile = self.get_tile(2, 1)
        elif l:
            tile = self.get_tile(0, 1)
        elif b:
            tile = self.get_tile(1, 2)
        elif t:
            tile = self.get_tile(1, 0)
        else:
            tile = self.ground

        self.autotile_cache[cache_key] = tile
        return tile

    def autotile_map(self):
        """Precompute autotiling for the entire map."""
        autotile_map = np.zeros((self.height, self.width), dtype=object)
        for y in range(self.height):
            for x in range(self.width):
                autotile_map[y, x] = self.get_autotile(y, x)
        return autotile_map

    def get_tile_image(self, x, y, tile):
        """Return the tile image using precomputed autotiling."""
        if tile == 1:
            return self.water
        return self.autotile_map[y, x]


class MapGenerator(threading.Thread):
    def __init__(self, width, height, chunk_size, player_pos, progress_queue):
        super().__init__()
        self.width = width
        self.height = height
        self.chunk_size = max(64, min(chunk_size, 512))  # Constrain chunk size
        self.player_pos = player_pos
        self.progress_queue = progress_queue
        self.map_data = None
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            # Pre-allocate map data
            self.map_data = np.zeros((self.height, self.width), dtype=np.uint8)

            # Generate map in chunks
            rng = np.random.default_rng()
            total_chunks = ((self.width + self.chunk_size - 1) // self.chunk_size) * (
                    (self.height + self.chunk_size - 1) // self.chunk_size
            )
            processed_chunks = 0
            update_interval = max(1, total_chunks // 20)

            for cy in range(0, self.height, self.chunk_size):
                for cx in range(0, self.width, self.chunk_size):
                    if self._stop_event.is_set():
                        return
                    chunk_y_end = min(cy + self.chunk_size, self.height)
                    chunk_x_end = min(cx + self.chunk_size, self.width)
                    chunk = (rng.random((chunk_y_end - cy, chunk_x_end - cx)) < 0.3).astype(np.uint8)
                    self.map_data[cy:chunk_y_end, cx:chunk_x_end] = chunk
                    processed_chunks += 1
                    if processed_chunks % update_interval == 0 or processed_chunks == total_chunks:
                        self.progress_queue.put(processed_chunks / total_chunks)

            # Set boundaries to water
            self.map_data[[0, -1], :] = 1
            self.map_data[:, [0, -1]] = 1

            # Clear area around player
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
        """Start map generation with memory check."""
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        required_memory = (self.width * self.height * 1) / (1024 ** 3)
        if available_memory < required_memory * 1.5:
            raise MemoryError(
                f"Insufficient memory: {required_memory:.2f} GB required, {available_memory:.2f} GB available"
            )

        self.generator = MapGenerator(
            self.width, self.height, self.chunk_size, self.player_pos, self.progress_queue
        )
        self.generator.start()

    def stop_generation(self):
        """Safely stop map generation."""
        if self.generator and self.generator.is_alive():
            self.generator.stop()
            self.generator.join()
            self.generator = None

    def get_generation_progress(self):
        """Retrieve map generation progress."""
        try:
            progress = self.progress_queue.get_nowait()
            if isinstance(progress, tuple) and progress[0] == "error":
                raise RuntimeError(progress[1])
            if progress == 1.0:
                self.map_data = self.generator.map_data
                LoadingStatus.set_status("Precomputing tiles...")
                self.tileset = TileSet(self.loader, self.map_data, self.tile_size, self.width, self.height)
                self.stop_generation()
            return progress
        except queue.Empty:
            return 0.0 if self.map_data is None else 1.0

    def get_tile_image(self, x, y, tile):
        """Return tile image with fallback."""
        if self.map_data is None or self.tileset is None:
            return self.loader.load('images/Ground/Ground_19.png', self.tile_size)
        return self.tileset.get_tile_image(x, y, tile)