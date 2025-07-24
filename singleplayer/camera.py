class Camera:
    def __init__(self, screen, game_map, pw, ph):
        self.s, self.m, self.pw, self.ph = screen, game_map, pw, ph

    def get_offset(self, player_pos):
        px, py = player_pos
        cx = max(0, min(px - self.s.get_width()//2 + self.pw//2,
                        self.m.width * self.m.tile_size - self.s.get_width()))
        cy = max(0, min(py - self.s.get_height()//2 + self.ph//2,
                        self.m.height * self.m.tile_size - self.s.get_height()))
        return cx, cy
