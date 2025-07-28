import pygame
import numpy as np
from singleplayer.image import ImageLoader


class TileSet:
    def __init__(self, map_data, tile_size, width, height):
        self.loader = ImageLoader()

        self.map_data = map_data
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Load and scale images to match original behavior
        self.tileset = self.loader.load('images/Tilesets/tileset.png').convert()
        self.water = self.loader.load('images/Water/Water_0.png', tile_size).convert()
        self.ground = self.loader.load('images/Ground/Ground_19.png', tile_size).convert()

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