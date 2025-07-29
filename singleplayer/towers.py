import numpy as np


class Tower:
    def __init__(self, x, y):
        self.x = x  # x-coordinate of the bottom tile
        self.y = y  # y-coordinate of the bottom tile


class TowerManager:
    def __init__(self, map_data, num_towers=5):
        self.towers = []
        self.map_data = map_data
        self.num_towers = num_towers

    def place_towers(self, width, height):
        rng = np.random.default_rng()

        for _ in range(self.num_towers):
            # Ensure the tower (1x3) and radius-3 circle fit within map boundaries
            # Bottom tile is at (tx, ty), so ty needs to account for tower extending upward
            tx = rng.integers(3, width - 3)  # 3-tile buffer for circle in x
            ty = rng.integers(5, height - 3)  # 3-tile buffer for circle, +2 for tower height upward

            # Clear a circular area with radius 3 tiles around the bottom tile (tx, ty)
            for dy in range(-3, 4):  # Check tiles within ±3 in y-direction
                for dx in range(-3, 4):  # Check tiles within ±3 in x-direction
                    x, y = tx + dx, ty + dy  # Center clearing on (tx, ty)
                    # Check if the tile is within a radius of 3 (Euclidean distance)
                    if (dx ** 2 + dy ** 2) <= 9:  # Radius 3 squared
                        if 0 <= x < width and 0 <= y < height:
                            self.map_data[y, x] = 0  # Force to ground tile

            # Place the 1x3 tower with bottom tile at (tx, ty)
            for dy in range(-2, 1):  # Tower occupies (tx, ty-2), (tx, ty-1), (tx, ty)
                y = ty + dy
                if 0 <= y < height:  # Ensure within bounds
                    if dy == -1:
                        self.map_data[y, tx] = 10  # Bottom tile at ty marked as 10

            self.towers.append(Tower(tx, ty))  # Store bottom tile coordinates