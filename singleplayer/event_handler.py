import pygame


class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            # --- Keyboard Events ---
            elif event.type == pygame.KEYDOWN:
                if self.game.showing_upgrade_screen:
                    if event.key == pygame.K_1:
                        self.game.player_card_system.apply_upgrade(0)
                        self.game.showing_upgrade_screen = False
                    elif event.key == pygame.K_2:
                        self.game.player_card_system.apply_upgrade(1)
                        self.game.showing_upgrade_screen = False
                    elif event.key == pygame.K_3:
                        self.game.player_card_system.apply_upgrade(2)
                        self.game.showing_upgrade_screen = False
                    return  # Skip other keys while upgrade screen is active

                # --- Normal game input ---
                if event.key == pygame.K_ESCAPE:
                    self.game.paused = not self.game.paused
                elif event.key == pygame.K_LALT:
                    self.game.noclip = not self.game.noclip
                elif event.key == pygame.K_u:
                    self.game.showing_upgrade_screen = True
                    self.game.player_card_system.generate_options()

            # --- Mouse Events ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.game.showing_upgrade_screen:
                        clicked = self.game.player_card_system.handle_click(event.pos)
                        if clicked:
                            self.game.showing_upgrade_screen = False
                            return

                    if self.game.paused:
                        action = self.game.pause_menu.handle_click(event.pos)
                        if action == "Resume":
                            self.game.paused = False
                        elif action == "Settings":
                            self.game.paused = False
                        elif action == "Quit to Menu":
                            self.game.running = False
                        elif action == "Quit to Desktop":
                            self.game.cleanup()
                            return
                    else:
                        tile_info = self.get_tile_under_click(event.pos)
                        if tile_info:
                            sx, sy, tx, ty, value = tile_info
                            print(f"Click at screen ({sx}, {sy}) → tile ({tx}, {ty}) with value {value}")

    def get_tile_under_click(self, screen_pos):
        """Return screen pos, world tile coords, and tile value."""
        mx, my = screen_pos  # screen (window) coordinates
        camera_x, camera_y = self.game.camera.get_offset(self.game.player.get_pos())

        world_x = mx + camera_x
        world_y = my + camera_y

        tile_x = world_x // self.game.tile_size
        tile_y = world_y // self.game.tile_size

        if 0 <= tile_x < self.game.map.width and 0 <= tile_y < self.game.map.height:
            tile_value = self.game.map.map_data[tile_y, tile_x]
            return mx, my, tile_x, tile_y, tile_value

        return None
