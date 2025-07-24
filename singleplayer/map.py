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
        self.chunk_size = 5000
        self.total_chunks = (width // self.chunk_size + (1 if width % self.chunk_size else 0)) * (
            height // self.chunk_size + (1 if height % self.chunk_size else 0)
        )
        self.progress_queue = queue.Queue()

    def load_step(self):
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        required_memory = (self.width * self.height * 1) / (1024 ** 3)
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
        img = pygame.Surface((self.tile_size, self.tile_size))
        if tile == 0:
            img.fill((100, 100, 100))
        elif tile == 1:
            img.fill((200, 200, 200))
        return img

    def _gen_ground(self):
        print("Generating ground...")
        self.map_data = np.zeros((self.height, self.width), dtype=np.int8)
        chunk_count = 0
        for y in range(0, self.height, self.chunk_size):
            for x in range(0, self.width, self.chunk_size):
                y_end = min(y + self.chunk_size, self.height)
                x_end = min(x + self.chunk_size, self.width)
                self.map_data[y:y_end, x:x_end] = 0
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
                self.map_data[y:y_end, x:x_end] = np.where(random_walls, 1, self.map_data[y:y_end, x:x_end])
                if y == 0:
                    self.map_data[y, x:x_end] = 1
                if y_end == self.height:
                    self.map_data[y_end-1, x:x_end] = 1
                if x == 0:
                    self.map_data[y:y_end, x] = 1
                if x_end == self.width:
                    self.map_data[y:y_end, x_end-1] = 1
                chunk_count += 1
                self.progress_queue.put(chunk_count / self.total_chunks)
        px, py = self.player_pos[0] // self.tile_size, self.player_pos[1] // self.tile_size
        y_start = max(0, py - 1)
        y_end = min(self.height, py + 2)
        x_start = max(0, px - 1)
        x_end = min(self.width, px + 2)
        self.map_data[y_start:y_end, x_start:x_end] = 0
        self.progress_queue.put(1.0)