import asyncio, socket, requests
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

    async def start_countdown(self):
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
        self.positions[writer] = (300, 200)

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
                        nx = max(0, min(560, x + dx))
                        ny = max(0, min(360, y + dy))
                        self.positions[writer] = (nx, ny)
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

    async def periodic_broadcast_positions(self):
        while True:
            if self.game_started:
                await self.broadcast_positions()
            await asyncio.sleep(0.05)

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
