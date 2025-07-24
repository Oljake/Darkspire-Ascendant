import numpy as np
import pygame
from singleplayer.loading_status import LoadingStatus
import psutil
import threading
import queue

class Map:
    def __init__(self, width, height, tile_size, player_pos):
        self.width, self.height, self.tile_size = width, height, tile_size
        self.player_pos = player_pos
        self.map_data = None
        self.loading_stage = 0
        self.chunk_size = 1000  # Reduced chunk size for better memory efficiency
        self.total_chunks = (width // self.chunk_size + (1 if width % self.chunk_size else 0)) * (
            height // self.chunk_size + (1 if height % self.chunk_size else 0)
        )
        self.progress_queue = queue.Queue()
        # Cache tile images
        self.tile_images = {
            0: pygame.Surface((self.tile_size, self.tile_size)),  # Ground
            1: pygame.Surface((self.tile_size, self.tile_size))   # Wall
        }
        self.tile_images[0].fill((100, 100, 100))  # Gray for ground
        self.tile_images[1].fill((200, 200, 200))  # Light gray for walls

    def load_step(self):
        # Estimate memory for a single chunk instead of the entire map
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        required_memory = (self.chunk_size * self.chunk_size * 1) / (8 * 1024 ** 3)  # np.bool_ uses 1 bit
        if available_memory < required_memory * 1.5:
            raise MemoryError(f"Insufficient memory: {required_memory:.2f} GB required, {available_memory:.2f} GB available")

        if self.loading_stage == 0:
            LoadingStatus.set_status("Generating ground...")
            for progress in self._gen_ground():
                yield progress
        elif self.loading_stage == 1:
            LoadingStatus.set_status("Generating walls...")
            threading.Thread(target=self._gen_walls_threaded, daemon=True).start()
            while True:
                try:
                    progress = self.progress_queue.get(timeout=0.1)
                    yield progress
                    if progress >= 1.0:
                        break
                except queue.Empty:
                    yield self.progress_queue.qsize() / self.total_chunks
        else:
            return False
        self.loading_stage += 1
        return True

    def get_tile_image(self, x, y, tile):
        # Return cached tile image
        return self.tile_images[tile]

    def _gen_ground(self):
        print("Generating ground...")
        # Initialize map_data lazily, chunk by chunk
        if self.map_data is None:
            self.map_data = np.zeros((self.height, self.width), dtype=np.bool_)
        chunk_count = 0
        for y in range(0, self.height, self.chunk_size):
            for x in range(0, self.width, self.chunk_size):
                y_end = min(y + self.chunk_size, self.height)
                x_end = min(x + self.chunk_size, self.width)
                self.map_data[y:y_end, x:x_end] = False  # Ground (0)
                chunk_count += 1
                yield chunk_count / self.total_chunks
        yield 1.0

    def _gen_walls_threaded(self):
        print("Generating walls...")
        rng = np.random.default_rng()
        chunk_count = 0
        for y in range(0, self.height, self.chunk_size):
            for x in range(0, self.width, self.chunk_size):
                y_end = min(y + self.chunk_size, self.height)
                x_end = min(x + self.chunk_size, self.width)
                chunk_height, chunk_width = y_end - y, x_end - x
                random_walls = rng.random((chunk_height, chunk_width)) < 0.2
                self.map_data[y:y_end, x:x_end] = np.where(random_walls, True, self.map_data[y:y_end, x:x_end])
                if y == 0:
                    self.map_data[y, x:x_end] = True  # Top wall
                if y_end == self.height:
                    self.map_data[y_end-1, x:x_end] = True  # Bottom wall
                if x == 0:
                    self.map_data[y:y_end, x] = True  # Left wall
                if x_end == self.width:
                    self.map_data[y:y_end, x_end-1] = True  # Right wall
                chunk_count += 1
                self.progress_queue.put(chunk_count / self.total_chunks)
        px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
        y_start = max(0, py - 1)
        y_end = min(self.height, py + 2)
        x_start = max(0, px - 1)
        x_end = min(self.width, px + 2)
        self.map_data[y_start:y_end, x_start:x_end] = False  # Clear area around player
        self.progress_queue.put(1.0)