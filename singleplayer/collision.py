class Collision:
    def __init__(self, game_map, player_width, player_height):
        self.map = game_map
        self.player_width = player_width
        self.player_height = player_height
        self.tile_size = game_map.tile_size if game_map else 100

    def update_map(self, new_map):
        """Update the map reference when the map is generated"""
        self.map = new_map
        self.tile_size = new_map.tile_size

    def check(self, new_x, new_y):
        """
        Check if the player would collide with any tiles at the new position
        Returns True if collision would occur, False otherwise
        """
        if not hasattr(self.map, 'map_data') or self.map.map_data is None:
            return False

        # Convert player position to tile coordinates
        left = int(new_x // self.tile_size)
        right = int((new_x + self.player_width - 1) // self.tile_size)
        top = int(new_y // self.tile_size)
        bottom = int((new_y + self.player_height - 1) // self.tile_size)

        # Ensure we stay within map bounds
        left = max(0, left)
        right = min(self.map.width - 1, right)
        top = max(0, top)
        bottom = min(self.map.height - 1, bottom)

        # Check each tile in the player's area
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if self.map.map_data[y, x] in [1, 10]:  # 1 Wall, 10 Tower
                    return True
        return False