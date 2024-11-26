import random
from pprint import pprint
from engine.types import Grid


def preview_grid(grid):
    # pretty print grid values
    for tile in grid.tiles:
        pprint(tile)


def generate_match_pairs(width, height):
    length = width * height
    ids = []

    for i in range(int(length / 2)):
        ids.append(i)
        ids.append(i)
    random.shuffle(ids)
    return ids


def create_grid(width=4, height=4):
    # make a 4x4 match 2 game grid
    # each cell is a card with a value
    grid = Grid(width=width, height=height, tiles=[])

    # create a multi-dimensional array
    ids = generate_match_pairs(width, height)
    for id in range(len(ids)):
        slot_x = id % width
        slot_y = id // width
        grid.tiles.append(
            {
                "id": id,
                "match_id": ids[id],
                "matched": False,
                "slot_x": slot_x,
                "slot_y": slot_y,
            }
        )

    # return the grid as a dictionary
    return grid.model_dump()
