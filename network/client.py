import pygame
import asyncio
import threading
import sys
from network.config import PORT
from ui.tile_image_loader import TileImageLoader
import random


class ClientApp:
    def __init__(self, ip, username, screen, is_host=False, server_loop=None, server=None):
        self.screen = screen
        self.ip = ip
        self.username = username
        self.reader = None
        self.writer = None
        self.ready = False
        self.positions = {}
        self.running = True
        self.game_started = False
        self.is_loading = False
        self.chat_messages = []
        self.lobby_status = []
        self.input_text = ""
        self.input_active = False
        self.loop = asyncio.new_event_loop()
        self.font = pygame.font.SysFont(None, 24)
        self.button_font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.fps_font = pygame.font.SysFont("Arial", 18)
        self.is_host = is_host
        self.server_loop = server_loop
        self.server = server
        self.paused = False
        self.pause_options = ["Resume", "Close Server"] if is_host else ["Resume", "Disconnect"]
        self.pause_rects = [pygame.Rect(200, 200 + i * 60, 200, 40) for i in range(len(self.pause_options))]
        self.ready_rect = pygame.Rect(400, 450, 150, 50)
        self.leave_rect = pygame.Rect(400, 510, 150, 50)
        self.cancel_rect = pygame.Rect(400, 510, 150, 50)
        self.is_connecting = True
        self.tile_size = 100
        self.player_width = 30
        self.player_height = 50

        self.image_loader = TileImageLoader(self.tile_size, self.screen)
        self.ground_images = self.image_loader.load_series("Ground", "Ground_{}.png", 20)
        self.wall_images = self.image_loader.load_series("Maze_wall", "Maze_wall_{}.png", 10)
        self.tile_image_indices = {}

        pygame.key.set_repeat(500, 50)
        threading.Thread(target=self.start_client, daemon=True).start()

    async def _send(self, msg):
        if self.writer:
            try:
                self.writer.write((msg + '\n').encode())
                await self.writer.drain()
            except:
                pass

    def send_message(self, msg):
        if msg:
            self.chat_messages.append(f"{self.username}: {msg}")
            if len(self.chat_messages) > 15:
                self.chat_messages.pop(0)
            asyncio.run_coroutine_threadsafe(self._send(msg), self.loop)

    def toggle_ready(self):
        if not self.is_connecting:
            self.ready = not self.ready
            asyncio.run_coroutine_threadsafe(self._send("/ready"), self.loop)

    def close(self):
        self.running = False
        if self.writer:
            try:
                self.writer.close()
                asyncio.run_coroutine_threadsafe(self.writer.wait_closed(), self.loop).result(timeout=2)
            except:
                pass
            self.writer = None

        if self.is_host and self.server_loop and self.server:
            try:
                asyncio.run_coroutine_threadsafe(self.server.shutdown(), self.server_loop).result(timeout=2)
            except:
                pass
            if self.server_loop.is_running():
                self.server_loop.call_soon_threadsafe(self.server_loop.stop)
            self.server_loop = None
            self.server = None

    def start_client(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self.client_loop())
        finally:
            try:
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                self.loop.run_until_complete(self.loop.shutdown_default_executor())
            except:
                pass
            if not self.loop.is_closed():
                self.loop.close()

    async def client_loop(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.ip, PORT)
            data = await self.reader.readline()
            if data.decode().strip() == "ENTER_USERNAME":
                self.writer.write((self.username + "\n").encode())
                await self.writer.drain()
                self.is_connecting = False

            while True:
                data = await self.reader.readline()
                if not data:
                    break
                msg = data.decode().strip()
                if msg == "START_GAME":
                    self.game_started = True
                    self.is_loading = False
                elif msg == "LOADING_GAME":
                    self.is_loading = True
                elif msg == "LOBBY_STATUS":
                    lobby_status = []
                    while True:
                        line = await self.reader.readline()
                        if not line or line == b'\n':
                            break
                        line_decoded = line.decode().strip()
                        if not line_decoded:
                            break
                        parts = line_decoded.split('|')
                        if len(parts) == 2:
                            username, status = parts
                            lobby_status.append((username, status))
                    self.lobby_status = lobby_status
                elif msg == "POSITIONS":
                    positions = {}
                    while True:
                        line = await self.reader.readline()
                        if not line or line == b'\n':
                            break
                        line_decoded = line.decode().strip()
                        if not line_decoded:
                            break
                        parts = line_decoded.split('|')
                        if len(parts) == 3:
                            username, x, y = parts
                            positions[username] = (int(x), int(y))
                    self.positions = positions
                elif msg.startswith("MAP|"):
                    try:
                        _, width, height = msg.split('|')
                        self.map_width = int(width)
                        self.map_height = int(height)
                        self.map = []
                        for _ in range(self.map_height):
                            line = await self.reader.readline()
                            row = [int(c) for c in line.decode().strip()]
                            self.map.append(row)
                    except:
                        self.chat_messages.append("Error receiving map")
                elif msg in ("HOST_LEFT", "SERVER_SHUTDOWN"):
                    self.chat_messages.append("Server disconnected. Returning to menu.")
                    self.running = False
                    break
                else:
                    self.chat_messages.append(msg)
                    if len(self.chat_messages) > 15:
                        self.chat_messages.pop(0)
        except Exception as e:
            self.chat_messages.append(f"Connection error: {e}")
        finally:
            self.chat_messages.append("Disconnected from server")
            if self.writer:
                self.writer.close()
                try:
                    await self.writer.wait_closed()
                except:
                    pass
            self.writer = None

    def draw_lobby(self):
        self.screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        if self.is_connecting:
            connecting_surf = self.font.render("Joining server...", True, (255, 255, 255))
            connecting_rect = connecting_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(connecting_surf, connecting_rect)

            # Draw cancel button
            is_cancel_hovered = self.cancel_rect.collidepoint(mouse_pos)
            cancel_bg_color = (100, 0, 0) if is_cancel_hovered else (50, 50, 50)
            cancel_text_color = (255, 255, 255) if is_cancel_hovered else (200, 200, 200)
            pygame.draw.rect(self.screen, cancel_bg_color, self.cancel_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), self.cancel_rect, 2, border_radius=10)
            cancel_surf = self.button_font.render("Cancel", True, cancel_text_color)
            cancel_text_rect = cancel_surf.get_rect(center=self.cancel_rect.center)
            self.screen.blit(cancel_surf, cancel_text_rect)

        elif self.is_loading:
            # Display loading screen
            loading_surf = self.font.render("Loading game...", True, (255, 255, 255))
            loading_rect = loading_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(loading_surf, loading_rect)
        else:
            # Draw chat log (left side)
            y = 10
            for msg in self.chat_messages:
                surf = self.font.render(msg, True, (255, 255, 255))
                self.screen.blit(surf, (10, y))
                y += 25

            # Draw player list (right side)
            y = 10
            title_surf = self.font.render("Players:", True, (255, 255, 255))
            self.screen.blit(title_surf, (350, y))
            y += 30
            for username, status in self.lobby_status:
                status_color = (0, 255, 0) if status.lower() == "ready" else (255, 0, 0)
                surf = self.font.render(f"{username}: {status}", True, status_color)
                self.screen.blit(surf, (350, y))
                y += 25

            # Draw chat input
            input_rect = pygame.Rect(10, 550, 300, 30)
            input_border_color = (0, 255, 0) if self.input_active else (255, 255, 255)
            pygame.draw.rect(self.screen, input_border_color, input_rect, 2, border_radius=5)
            input_surf = self.font.render(f"Chat: {self.input_text}", True, (255, 255, 255))
            input_text_rect = input_surf.get_rect(topleft=(20, 560))
            self.screen.blit(input_surf, input_text_rect)

            # Draw Ready/Unready button
            is_ready_hovered = self.ready_rect.collidepoint(mouse_pos)
            ready_bg_color = (0, 100, 0) if is_ready_hovered else (50, 50, 50)
            ready_text_color = (255, 255, 255) if is_ready_hovered else (200, 200, 200)
            pygame.draw.rect(self.screen, ready_bg_color, self.ready_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), self.ready_rect, 2, border_radius=10)
            ready_text = "Unready" if self.ready else "Ready"
            ready_surf = self.button_font.render(ready_text, True, ready_text_color)
            ready_text_rect = ready_surf.get_rect(center=self.ready_rect.center)
            self.screen.blit(ready_surf, ready_text_rect)

            # Draw Leave Lobby button
            is_leave_hovered = self.leave_rect.collidepoint(mouse_pos)
            leave_bg_color = (100, 0, 0) if is_leave_hovered else (50, 50, 50)
            leave_text_color = (255, 255, 255) if is_leave_hovered else (200, 200, 200)
            pygame.draw.rect(self.screen, leave_bg_color, self.leave_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), self.leave_rect, 2, border_radius=10)
            leave_surf = self.button_font.render("Leave Lobby", True, leave_text_color)
            leave_text_rect = leave_surf.get_rect(center=self.leave_rect.center)
            self.screen.blit(leave_surf, leave_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_connecting:
                    if self.cancel_rect.collidepoint(mouse_pos):
                        self.close()
                        self.running = False
                elif self.is_loading:
                    continue
                else:
                    if self.ready_rect.collidepoint(mouse_pos):
                        self.toggle_ready()
                    elif self.leave_rect.collidepoint(mouse_pos):
                        self.close()
                        self.running = False
                    elif input_rect.collidepoint(mouse_pos):
                        self.input_active = True
                    else:
                        self.input_active = False

            elif event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN and self.input_text:
                    self.send_message(self.input_text)
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.unicode.isprintable():
                    self.input_text += event.unicode

    def draw_pause_menu(self):
        # Create a new surface for the pause menu with per-pixel alpha
        pause_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        # Fill with half-transparent background (alpha=128 for ~50% opacity)
        pause_surface.fill((30, 30, 30, 128))

        # Draw pause menu options
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(self.pause_options):
            rect = self.pause_rects[i]
            color = (0, 200, 0) if rect.collidepoint(mouse_pos) else (255, 255, 255)
            surf = self.button_font.render(option, True, color)
            text_rect = surf.get_rect(center=rect.center)
            # Draw button background
            pygame.draw.rect(pause_surface, (50, 50, 50, 200), rect, border_radius=10)
            pygame.draw.rect(pause_surface, (255, 255, 255, 255), rect, 2, border_radius=10)
            pause_surface.blit(surf, text_rect)

        # Blit the pause surface onto the main screen
        self.screen.blit(pause_surface, (0, 0))

    def get_camera_offset(self):
        px, py = self.positions.get(self.username, (750, 750))
        cx = max(0, min(px - self.screen.get_width() // 2 + self.player_width // 2, self.map_width * self.tile_size - self.screen.get_width()))
        cy = max(0, min(py - self.screen.get_height() // 2 + self.player_height // 2, self.map_height * self.tile_size - self.screen.get_height()))
        return cx, cy

    def run_game(self):
        speed = 5
        self.tile_image_indices.clear()
        while self.running and self.game_started:
            dt = self.clock.tick()  # unlimited FPS, returns ms since last call
            fps = int(self.clock.get_fps())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.paused:
                    for i, rect in enumerate(self.pause_rects):
                        if rect.collidepoint(pygame.mouse.get_pos()):
                            if i == 0:  # Resume
                                self.paused = False
                            elif i == 1:  # Close Server or Disconnect
                                self.close()
                                return

            # Draw game elements
            cx, cy = self.get_camera_offset()
            self.screen.fill((30, 30, 30))

            # Draw map tiles
            start_x = max(cx // self.tile_size, 0)
            end_x = min((cx + self.screen.get_width()) // self.tile_size + 1, self.map_width)
            start_y = max(cy // self.tile_size, 0)
            end_y = min((cy + self.screen.get_height()) // self.tile_size + 1, self.map_height)

            tile_blits = []
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile = self.map[y][x]
                    key = (x, y, tile)
                    if key not in self.tile_image_indices:
                        imgs = self.wall_images if tile == 1 else self.ground_images
                        self.tile_image_indices[key] = random.randrange(len(imgs))
                    idx = self.tile_image_indices[key]
                    imgs = self.wall_images if tile == 1 else self.ground_images
                    img = imgs[idx]
                    sx, sy = x * self.tile_size - cx, y * self.tile_size - cy
                    tile_blits.append((img, (sx, sy)))
            self.screen.blits(tile_blits)

            # Draw players
            for user, (x, y) in self.positions.items():
                sx, sy = x - cx, y - cy
                if -self.player_width < sx < self.screen.get_width() and -self.player_height < sy < self.screen.get_height():
                    color = (0, 0, 255) if user == self.username else (255, 0, 0)
                    pygame.draw.rect(self.screen, color, pygame.Rect(sx, sy, self.player_width, self.player_height))

            # Update movement only if not paused
            if not self.paused:
                self.accum_time = getattr(self, 'accum_time', 0) + dt
                while self.accum_time >= 1000 / 60:
                    keys = pygame.key.get_pressed()
                    dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
                    dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed
                    if dx or dy:
                        asyncio.run_coroutine_threadsafe(self._send(f"MOVE|{dx}|{dy}"), self.loop)
                    self.accum_time -= 1000 / 60

            # Draw pause menu if paused (after game elements to preserve background)
            if self.paused:
                self.draw_pause_menu()

            # Draw FPS counter
            fps_surf = self.fps_font.render(f"FPS: {fps}", True, (255, 255, 0))
            self.screen.blit(fps_surf, (5, 5))
            pygame.display.flip()
