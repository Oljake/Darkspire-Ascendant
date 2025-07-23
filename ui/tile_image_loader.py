import pygame
import os
import sys
from typing import Dict

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class TileImageLoader:
    def __init__(self, tile_size: int, screen: pygame.Surface):
        self.tile_size = tile_size
        self.screen = screen
        self.cache: Dict[str, pygame.Surface] = {}

    def load(self, folder: str, filename_pattern: str, index: int) -> pygame.Surface:
        key = f"{folder}_{index}"
        if key in self.cache:
            return self.cache[key]

        filename = filename_pattern.format(index)
        path = resource_path(os.path.join("images", folder, filename))
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Image not found: {path}")

        img = pygame.image.load(path).convert_alpha()  # Load with alpha

        # Optimize image for display (convert with alpha)
        optimized_img = img.convert_alpha()

        # Resize once with smoothscale
        scaled_img = pygame.transform.smoothscale(optimized_img, (self.tile_size, self.tile_size))

        self.cache[key] = scaled_img
        return scaled_img

    def load_series(self, folder: str, filename_pattern: str, count: int) -> list:
        return [self.load(folder, filename_pattern, i) for i in range(count)]