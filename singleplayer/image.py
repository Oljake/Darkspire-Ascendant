import pygame


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
