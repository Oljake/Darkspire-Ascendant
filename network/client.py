import pygame, asyncio, threading, sys
from network.config import PORT

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
        self.chat_messages = []
        self.lobby_status = []
        self.input_text = ""
        self.input_active = False
        self.loop = asyncio.new_event_loop()
        self.font = pygame.font.SysFont(None, 24)
        self.button_font = pygame.font.SysFont(None, 36)
        self.is_host = is_host
        self.server_loop = server_loop
        self.server = server
        self.paused = False
        self.pause_options = ["Resume", "Close Server"] if is_host else ["Resume", "Disconnect"]
        self.pause_rects = [pygame.Rect(200, 200 + i * 60, 200, 40) for i in range(len(self.pause_options))]
        self.ready_rect = pygame.Rect(400, 450, 150, 50)
        self.leave_rect = pygame.Rect(400, 510, 150, 50)
        self.is_connecting = True  # New flag for connection status
        pygame.key.set_repeat(500, 50)  # Enable key repeat: 500ms delay, 50ms interval
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
        if not self.is_connecting:  # Only allow toggling ready when connected
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
                self.is_connecting = False  # Connection established

            while True:
                data = await self.reader.readline()
                if not data:
                    break
                msg = data.decode().strip()
                if msg == "START_GAME":
                    self.game_started = True
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
            # Display connecting message
            connecting_surf = self.font.render("Joining server...", True, (255, 255, 255))
            connecting_rect = connecting_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(connecting_surf, connecting_rect)
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
                status_color = (0, 255, 0) if status.lower() == "ready" else (255, 0, 0)  # Case-insensitive comparison
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

        # Handle lobby events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_connecting:
                    continue  # Skip all mouse events while connecting
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
        self.screen.fill((30, 30, 30, 128))
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(self.pause_options):
            color = (0, 200, 0) if self.pause_rects[i].collidepoint(mouse_pos) else (255, 255, 255)
            surf = self.font.render(option, True, color)
            self.screen.blit(surf, (200, 200 + i * 60))

    def run_game(self):
        speed = 5
        clock = pygame.time.Clock()
        while self.running and self.game_started:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.paused:
                    for i, rect in enumerate(self.pause_rects):
                        if rect.collidepoint(mouse_pos):
                            if i == 0:  # Resume
                                self.paused = False
                            elif i == 1:  # Disconnect (guest) or Close Server (host)
                                self.close()
                                return

            if not self.paused:
                keys = pygame.key.get_pressed()
                dx = dy = 0
                if keys[pygame.K_LEFT]:
                    dx = -speed
                if keys[pygame.K_RIGHT]:
                    dx = speed
                if keys[pygame.K_UP]:
                    dy = -speed
                if keys[pygame.K_DOWN]:
                    dy = speed

                if dx != 0 or dy != 0:
                    asyncio.run_coroutine_threadsafe(self._send(f"MOVE|{dx}|{dy}"), self.loop)

                self.screen.fill((30, 30, 30))
                for user, (x, y) in self.positions.items():
                    color = (0, 200, 0) if user == self.username else (150, 150, 150)
                    pygame.draw.rect(self.screen, color, (x, y, 40, 40))
                    if user != self.username:
                        name_surf = self.font.render(user, True, (255, 255, 255))
                        self.screen.blit(name_surf, (x, y - 20))

                fps = int(clock.get_fps())
                fps_surf = self.font.render(f"FPS: {fps}", True, (255, 255, 0))
                self.screen.blit(fps_surf, (5, 5))
            else:
                self.draw_pause_menu()

            pygame.display.flip()
            clock.tick(60)
