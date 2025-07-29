import pygame

class ImageLoader:
    def __init__(self):
        self.cache = {}

    def load(self, path, size=None):
        """Load and optionally scale image to (width, height), caching the result."""
        cache_key = (path, size) if size else path
        if cache_key not in self.cache:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            self.cache[cache_key] = image
        return self.cache[cache_key]
