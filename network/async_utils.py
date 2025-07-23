import asyncio, threading
from network.server import GameServer
from network.config import PORT


def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    try:
        loop.run_forever()
    except:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.run_until_complete(loop.shutdown_default_executor())
        loop.close()


def start_server():
    loop = asyncio.new_event_loop()
    threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True).start()
    server = GameServer()
    asyncio.run_coroutine_threadsafe(server.run_server(), loop)
    return loop, server
