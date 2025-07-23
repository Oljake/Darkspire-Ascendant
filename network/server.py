import asyncio
import socket
import requests
import random
from network.config import PORT, HOST

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "Unavailable"

def is_port_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', port))
        s.close()
        return False
    except OSError:
        return True

class GameServer:
    def __init__(self):
        self.clients = []
        self.usernames = {}
        self.ready_status = {}
        self.positions = {}
        self.game_started = False
        self.host = None
        self.broadcast_task = None
        self.server = None
        self.countdown_task = None
        self.map = None
        self.map_width = 50  # 50 tiles wide
        self.map_height = 50  # 50 tiles high
        self.tile_size = 100  # 100x100 pixels per tile
        self.player_width = 30
        self.player_height = 50

    def generate_map(self):
        # Create a 50x50 grid: 0 = open, 1 = wall
        self.map = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        # Place walls randomly (30% chance)
        for y in range(self.map_height):
            for x in range(self.map_width):
                if random.random() < 0.3:
                    self.map[y][x] = 1
        # Ensure starting position (750, 750) is open (tile at roughly 7,7)
        start_x, start_y = 750 // self.tile_size, 750 // self.tile_size
        self.map[start_y][start_x] = 0
        # Ensure some connectivity by clearing a small area around start
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                ny, nx = start_y + dy, start_x + dx
                if 0 <= ny < self.map_height and 0 <= nx < self.map_width:
                    self.map[ny][nx] = 0

    def is_position_valid(self, x, y):
        # Check if the player's rectangle (30x50) is within map bounds and not in a wall
        if (x < 0 or y < 0 or
            x + self.player_width > self.map_width * self.tile_size or
            y + self.player_height > self.map_height * self.tile_size):
            return False
        # Check all tiles the player rectangle overlaps
        top_left_x = x // self.tile_size
        top_left_y = y // self.tile_size
        bottom_right_x = (x + self.player_width - 1) // self.tile_size
        bottom_right_y = (y + self.player_height - 1) // self.tile_size
        for ty in range(top_left_y, bottom_right_y + 1):
            for tx in range(top_left_x, bottom_right_x + 1):
                if 0 <= ty < self.map_height and 0 <= tx < self.map_width:
                    if self.map[ty][tx] == 1:  # Wall
                        return False
                else:
                    return False
        return True

    async def start_countdown(self):
        # Generate map before starting
        self.generate_map()
        # Broadcast map to clients
        await self.broadcast_map()
        # Send countdown messages
        for i in range(3, 0, -1):
            await self.broadcast(f"SERVER: Starting in {i}...")
            await asyncio.sleep(1)
        await self.broadcast("SERVER: Starting")
        await asyncio.sleep(1)
        # Send loading game signal
        await self.broadcast("LOADING_GAME")
        await asyncio.sleep(2)  # Simulate loading time
        # Start the game
        self.game_started = True
        await self.broadcast("START_GAME")
        await self.broadcast_positions()

    async def handle_client(self, reader, writer):
        if len(self.clients) >= 6 or self.game_started:
            writer.write(b"Server full or game started.\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        addr = writer.get_extra_info('peername')
        writer.write(b"ENTER_USERNAME\n")
        await writer.drain()
        data = await reader.readline()
        username = data.decode().strip() or f"{addr}"
        self.usernames[writer] = username
        self.ready_status[writer] = False
        self.positions[writer] = (750, 750)  # Adjusted for 100x100 tiles

        self.clients.append(writer)
        await self.broadcast(f"SERVER: {username} joined the lobby.\n")
        await self.broadcast_lobby()

        if self.host is None:
            self.host = writer
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                msg = data.decode().strip()

                if msg == "/ready":
                    self.ready_status[writer] = not self.ready_status[writer]
                    status_str = "READY" if self.ready_status[writer] else "NOTREADY"
                    await self.broadcast(f"SERVER: {username} is {status_str}.\n")
                    await self.broadcast_lobby()

                    if not self.ready_status[writer]:
                        # Cancel countdown & notify
                        if self.countdown_task:
                            self.countdown_task.cancel()
                            try:
                                await self.countdown_task
                            except asyncio.CancelledError:
                                pass
                            self.countdown_task = None
                        await self.broadcast("SERVER: Canceled.... player is not ready.\n")
                    elif all(self.ready_status.values()) and len(self.ready_status) > 0 and not self.game_started:
                        if self.countdown_task:
                            self.countdown_task.cancel()
                        self.countdown_task = asyncio.create_task(self.start_countdown())
                    continue

                if msg.startswith("MOVE|"):
                    try:
                        _, dx, dy = msg.split('|')
                        dx, dy = int(dx), int(dy)
                        x, y = self.positions[writer]
                        new_pos = (x, y)

                        if self.game_started:
                            # Try moving in x direction first
                            if dx != 0:
                                nx = x + dx
                                if self.is_position_valid(nx, y):
                                    new_pos = (nx, y)
                            # Then try moving in y direction
                            if dy != 0:
                                ny = new_pos[1] + dy
                                if self.is_position_valid(new_pos[0], ny):
                                    new_pos = (new_pos[0], ny)

                        # Update position if it changed
                        if new_pos != (x, y):
                            self.positions[writer] = new_pos
                            await self.broadcast_positions()
                    except:
                        pass
                    continue

                await self.broadcast(f"{username}: {msg}", sender=writer)
        finally:
            if writer == self.host:
                await self.broadcast("HOST_LEFT\n")
                self.host = None
            if writer in self.clients:
                self.clients.remove(writer)
            if writer in self.usernames:
                del self.usernames[writer]
            if writer in self.ready_status:
                del self.ready_status[writer]
            if writer in self.positions:
                del self.positions[writer]

            await self.broadcast(f"SERVER: {username} left the lobby.\n")
            await self.broadcast_lobby()
            await self.broadcast_positions()
            writer.close()
            await writer.wait_closed()

    async def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.write((message + "\n").encode())
                    await client.drain()
                except:
                    pass

    async def broadcast_lobby(self):
        lobby_status = "LOBBY_STATUS\n"
        for w, ready in self.ready_status.items():
            lobby_status += f"{self.usernames[w]}|{'READY' if ready else 'NOTREADY'}\n"
        lobby_status += "\n"
        for client in self.clients:
            try:
                client.write(lobby_status.encode())
                await client.drain()
            except:
                pass

    async def broadcast_positions(self):
        msg = "POSITIONS\n"
        for w, pos in self.positions.items():
            msg += f"{self.usernames[w]}|{pos[0]}|{pos[1]}\n"
        msg += "\n"
        for client in self.clients:
            try:
                client.write(msg.encode())
                await client.drain()
            except:
                pass

    async def broadcast_map(self):
        msg = f"MAP|{self.map_width}|{self.map_height}\n"
        for row in self.map:
            msg += ''.join(str(cell) for cell in row) + "\n"
        msg += "\n"
        for client in self.clients:
            try:
                client.write(msg.encode())
                await client.drain()
            except:
                pass

    async def periodic_broadcast_positions(self):
        while True:
            if self.game_started:
                await self.broadcast_positions()
            await asyncio.sleep(0.016)  # 60fps

    async def run_server(self):
        self.server = await asyncio.start_server(self.handle_client, HOST, PORT)
        self.broadcast_task = asyncio.create_task(self.periodic_broadcast_positions())
        async with self.server:
            await self.server.serve_forever()

    async def shutdown(self):
        if self.broadcast_task:
            self.broadcast_task.cancel()
            try:
                await self.broadcast_task
            except asyncio.CancelledError:
                pass
        if self.countdown_task:
            self.countdown_task.cancel()
            try:
                await self.countdown_task
            except asyncio.CancelledError:
                pass
        if self.server:
            await self.broadcast("SERVER_SHUTDOWN\n")
            self.server.close()
            try:
                await self.server.wait_closed()
            except:
                pass
        self.clients.clear()
        self.usernames.clear()
        self.ready_status.clear()
        self.positions.clear()
        self.game_started = False
        self.host = None
        self.map = None
