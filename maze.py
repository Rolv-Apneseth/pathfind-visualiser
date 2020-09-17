import random


def completely_random(grid):
    for row in grid:
        for node in row:
            if random.random() <= 0.25:
                node.make_barrier()
                node.is_hard_barrier = True
    return grid
