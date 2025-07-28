import pygame
from singleplayer.main import SingleplayerGame  # Adjust path as needed

# Resolution presets (same as before)
RES_480P = (640, 480)
RES_576P = (720, 576)
RES_720P = (1280, 720)
RES_1080P = (1920, 1080)
RES_1440P = (2560, 1440)
RES_4K = (3840, 2160)

BASE_RES_HEIGHT = 1080
BASE_TILE_SIZE = 128

def clamp_resolution(requested_res, max_res):
    """Clamp requested resolution to max native resolution."""
    width = min(requested_res[0], max_res[0])
    height = min(requested_res[1], max_res[1])
    return (width, height)

def main():
    pygame.init()

    # Get native display resolution (monitor max)
    display_info = pygame.display.Info()
    native_res = (display_info.current_w, display_info.current_h)
    print(f"[Init] Native display resolution detected: {native_res}")

    # Requested resolution (set this)
    requested_res = RES_1080P  # example, user wants 4K

    # Clamp resolution to native max
    final_res = clamp_resolution(requested_res, native_res)
    print(f"[Init] Using resolution: {final_res}")

    screen = pygame.display.set_mode(final_res)
    pygame.display.set_caption("Singleplayer Game")

    # Calculate tile size based on vertical scale of final resolution
    scale_factor = final_res[1] / BASE_RES_HEIGHT
    tile_size = int(BASE_TILE_SIZE * scale_factor)

    print(f"[Init] Calculated tile size: {tile_size}")

    game = SingleplayerGame(screen, tile_size)
    game.run()
    game.cleanup()

if __name__ == "__main__":
    main()
