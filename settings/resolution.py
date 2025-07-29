import pygame

resolutions = {
    "480p": (640, 480),
    "576p": (720, 576),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "4k": (3840, 2160),
}

BASE_RES_HEIGHT = 1080
BASE_TILE_SIZE = 128


def get_native_resolution():
    """Detect native display resolution."""
    pygame.init()  # Make sure pygame is initialized before calling this
    display_info = pygame.display.Info()
    return (display_info.current_w, display_info.current_h)


def clamp_resolution(requested_res, max_res):
    """Clamp requested resolution to max native resolution."""
    width = min(requested_res[0], max_res[0])
    height = min(requested_res[1], max_res[1])
    return (width, height)


def calculate_tile_size(resolution):
    """Calculate tile size scaled by vertical resolution ratio."""
    scale_factor = resolution[1] / BASE_RES_HEIGHT
    return int(BASE_TILE_SIZE * scale_factor)
