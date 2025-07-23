import asyncio
import platform
from ui.menu import main_menu

if platform.system() == "Emscripten":
    asyncio.ensure_future(main_menu())
else:
    if __name__ == "__main__":
        asyncio.run(main_menu())
