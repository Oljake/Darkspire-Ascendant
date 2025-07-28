import random
import copy
import sys
sys.setrecursionlimit(100_000_000)  # Increase limit to 10,000

# Define tile adjacency rules based on input
# Format: {tile_id: {'left': [allowed], 'top': [allowed], 'right': [allowed], 'bottom': [allowed]}}
TILE_RULES = {
    0: {'left': [2, 7, 12, 13], 'top': [10, 11, 12, 13], 'right': [1, 2, 9], 'bottom': [5, 10, 9]},
    1: {'left': [0, 1, 8], 'top': [10, 11, 12, 13], 'right': [1, 2, 9], 'bottom': [6, 3, 4, 11]},
    2: {'left': [1, 0, 8], 'top': [10, 11, 12, 13], 'right': [0, 5, 10, 13], 'bottom': [7, 12, 8]},
    3: {'left': [5, 4, 9, 6], 'top': [6, 1, 8, 9], 'right': [11, 12, 4], 'bottom': [7, 12, 8]},
    4: {'left': [10, 11, 3], 'top': [6, 1, 8, 9], 'right': [7, 3, 8, 6], 'bottom': [5, 10, 9]},
    5: {'left': [2, 7, 12, 13], 'top': [5, 0, 4], 'right': [6, 7, 3, 8], 'bottom': [5, 10, 9]},
    6: {'left': [5, 4, 9, 6], 'top': [1, 8, 9, 6], 'right': [7, 3, 8, 6], 'bottom': [11, 3, 4, 6]},
    7: {'left': [6, 4, 9, 5], 'top': [7, 2, 3], 'right': [0, 5, 10, 13], 'bottom': [7, 12, 8]},
    8: {'left': [5, 4, 9, 6], 'top': [7, 2, 3], 'right': [1, 2, 9], 'bottom': [11, 3, 4, 6]},
    9: {'left': [0, 1, 8], 'top': [5, 0, 4], 'right': [7, 3, 8, 6], 'bottom': [11, 3, 4, 6]},
    10: {'left': [2, 7, 12, 13], 'top': [5, 0, 4], 'right': [11, 12, 4], 'bottom': [0, 1, 2, 13]},
    11: {'left': [10, 11, 3], 'top': [1, 8, 9, 6], 'right': [11, 12, 4], 'bottom': [0, 1, 2, 13]},
    12: {'left': [10, 11, 3], 'top': [7, 2, 3], 'right': [0, 5, 10, 13], 'bottom': [0, 1, 2, 13]},
    13: {'left': [2, 7, 12, 13], 'top': [10, 11, 12, 13], 'right': [0, 5, 10, 13], 'bottom': [0, 1, 2, 13]}
}


def get_valid_neighbors(tile_id, direction, grid, x, y, width, height):
    """Return list of valid tile IDs for a given position and direction."""
    if tile_id is None:
        return list(TILE_RULES.keys())  # Any tile is valid if no tile is placed yet
    return TILE_RULES[tile_id][direction]


def is_valid_placement(grid, x, y, tile_id, width, height):
    """Check if placing tile_id at (x, y) satisfies all neighbor constraints."""
    # Check left neighbor
    if x > 0 and grid[y][x - 1] is not None:
        if tile_id not in TILE_RULES[grid[y][x - 1]]['right']:
            return False

    # Check right neighbor
    if x < width - 1 and grid[y][x + 1] is not None:
        if tile_id not in TILE_RULES[grid[y][x + 1]]['left']:
            return False

    # Check top neighbor
    if y > 0 and grid[y - 1][x] is not None:
        if tile_id not in TILE_RULES[grid[y - 1][x]]['bottom']:
            return False

    # Check bottom neighbor
    if y < height - 1 and grid[y + 1][x] is not None:
        if tile_id not in TILE_RULES[grid[y + 1][x]]['top']:
            return False

    return True


def generate_map(width, height, max_attempts=100):
    """Generate a tile map of given width and height."""
    # Initialize grid with None
    grid = [[None for _ in range(width)] for _ in range(height)]


    def try_place_tile(x, y, attempt):
        if attempt > max_attempts:
            return False


        # If we've reached the end of the grid, we're done
        if x >= width:
            x = 0
            y += 1
        if y >= height:
            return True

        # Get possible tiles based on neighbors
        possible_tiles = set(TILE_RULES.keys())
        if x > 0 and grid[y][x - 1] is not None:
            possible_tiles &= set(TILE_RULES[grid[y][x - 1]]['right'])
        if x < width - 1 and grid[y][x + 1] is not None:
            possible_tiles &= set(TILE_RULES[grid[y][x + 1]]['left'])
        if y > 0 and grid[y - 1][x] is not None:
            possible_tiles &= set(TILE_RULES[grid[y - 1][x]]['bottom'])
        if y < height - 1 and grid[y + 1][x] is not None:
            possible_tiles &= set(TILE_RULES[grid[y + 1][x]]['top'])

        if not possible_tiles:
            return False

        # Try each possible tile
        possible_tiles = list(possible_tiles)
        random.shuffle(possible_tiles)

        for tile_id in possible_tiles:
            grid[y][x] = tile_id
            if is_valid_placement(grid, x, y, tile_id, width, height):
                # Move to next position
                if try_place_tile(x + 1, y, 0):
                    return True
            grid[y][x] = None

        return False

    # Start generation
    if try_place_tile(0, 0, 0):
        return grid
    else:
        return None  # Failed to generate map


def print_map(grid):
    """Print the generated map."""
    if grid is None:
        print("Failed to generate map.")
        return
    for row in grid:
        print(' '.join(str(tile).rjust(2) for tile in row))


def main():
    width, height = 10000, 10000
    print(f"Generating {width}x{height} map...")
    map_grid = generate_map(width, height, max_attempts=100_000)
    print_map(map_grid)

if __name__ == "__main__":
    main()


