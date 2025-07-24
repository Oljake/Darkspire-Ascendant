from singleplayer.map import Tile

class Collision:
    def __init__(self, game_map, pw, ph):
        self.m, self.pw, self.ph = game_map, pw, ph

    def setup(self):
        pass

    def check(self, new_x, new_y):
        left = new_x // self.m.tile_size
        right = (new_x + self.pw - 1) // self.m.tile_size
        top = new_y // self.m.tile_size
        bottom = (new_y + self.ph - 1) // self.m.tile_size
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                if 0 <= x < self.m.width and 0 <= y < self.m.height:
                    if self.m.get_tile(x, y) == Tile.WALL:  # Use Tile.WALL
                        return True
        return False