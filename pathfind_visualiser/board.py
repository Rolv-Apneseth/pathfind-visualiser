import pygame


# COLOURS
DEFAULT = (100, 100, 100)  # silver
BARRIER = (0, 0, 0)  # black
OPEN = (0, 100, 0)  # green
END = (200, 0, 0)  # (0, 0, 255)  # blue
PATH = (255, 255, 0)  # yellow
CLOSED = (128, 0, 128)  # purple
START = (0, 0, 255)  # (255, 165, 0)  # orange
GRIDLINES = (0, 0, 0)  # black


class Node:
    """
    Defines each square that will appear on the gui.

    Contains many helper functions to make the node objects very easy to use.
    State of the node defined by it's colour
    """

    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        # Squares, so height = width
        self.size = size
        # (x, y) is position of top left of square
        self.x = row * size
        self.y = col * size

        self.colour = DEFAULT
        # Will contain nodes which are adjacent and not barriers
        self.neighbours = []
        # Required in the update_neighbours function, to avoid index out of range errors
        self.total_rows = total_rows
        # Hard barriers cannot be changed
        self.is_hard_barrier = False

    # Colour setting and getting functions
    def is_start(self):
        return self.colour == START

    def make_start(self):
        self.colour = START

    def is_closed(self):
        return self.colour == CLOSED

    def make_closed(self):
        self.colour = CLOSED

    def is_open(self):
        return self.colour == OPEN

    def make_open(self):
        self.colour = OPEN

    def is_barrier(self):
        return self.colour == BARRIER

    def make_barrier(self):
        self.colour = BARRIER

    def make_hard_barrier(self):
        self.colour = BARRIER
        self.is_hard_barrier = True

    def is_end(self):
        return self.colour == END

    def make_end(self):
        self.colour = END

    def reset(self):
        self.colour = DEFAULT

    def make_path(self):
        self.colour = PATH

    # Other class functions
    def get_position(self):
        return self.row, self.col

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.size, self.size))

    def update_neighbours(self, grid):
        self.neighbours = []

        # Order is important for depth first search algorithm
        # Checks node to the left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

        # Checks node below
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):
            self.neighbours.append(grid[self.row + 1][self.col])

        # Checks node to the right
        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):
            self.neighbours.append(grid[self.row][self.col + 1])

        # Checks node above
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])


# Board Functions #####################################################
def set_hard_barriers(grid):
    """
    Makes barriers which can't be cleared, which make up the border of the display.
    """

    for node in grid[0]:
        node.make_hard_barrier()

    for node in grid[-1]:
        node.make_hard_barrier()

    for column in grid:
        column[0].make_hard_barrier()
        column[-1].make_hard_barrier()


def make_grid(rows, size):
    """Instantiates all the nodes and stores them in a 2d array."""

    grid = []
    gap = size // rows

    for i in range(rows):
        grid.append([])
        # Same number of columns as rows so rows can be used again
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    set_hard_barriers(grid)

    return grid


def draw_gridlines(window, rows, size):
    """
    Draws gridlines which allows each node to be distinguishable from those around it.
    """

    gap = size // rows
    for i in range(rows):
        pygame.draw.line(window, GRIDLINES, (0, i * gap), (size, i * gap))

        for j in range(rows):
            pygame.draw.line(window, GRIDLINES, (j * gap, 0), (j * gap, size))


def draw_board(window, grid, rows, size):
    """Updates the display, putting the gridlines on top of all the nodes."""

    window.fill(DEFAULT)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_gridlines(window, rows, size)

    pygame.display.update()


def get_clicked_position(pos, rows, size):
    """
    Returns the location of the node which the position is hovering over (top left
    of the square).
    """

    gap = size // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col
