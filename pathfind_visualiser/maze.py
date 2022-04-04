import random


# Helper functions #####################################################
def make_node_barrier(node):
    """Turns a node into a hard barrier."""

    node.make_barrier()
    node.is_hard_barrier = True
    return node


def node_reset(node):
    """Resets a node, making it default colour and not a hard barrier."""

    node.reset()
    node.is_hard_barrier = False


def generate_blank_path(grid):
    """Makes an empty path dictionary."""

    return {node: None for row in grid for node in row}


def make_wall(grid, start, direction, path):
    """Generates a wall in a given direction from a starting node."""

    # Will contain all the nodes changed (so one can be made open again using
    # make_opening)
    wall = []

    node = start
    # Loop ends as soon as the next node in line is a barrier
    while node:
        # Must keep updating neighbours because barriers are getting added
        node.update_neighbours(grid)
        # Saving the current to a different variable
        prev_node = node
        # Checks next node in given direction
        node = direction(grid, prev_node)

        # Make previous node barrier and add to walls list
        prev_node.update_neighbours(grid)
        make_node_barrier(prev_node)
        wall.append(prev_node)

        # Update path if node is valid, or break the loop if it has been visited before
        if node:
            if path[node]:
                break
            path[node] = prev_node

    if start in wall:
        wall.remove(start)
    return wall


def make_opening(wall):
    """Takes an array of nodes which make up a wall and opens a random node."""

    node_reset(random.choice(wall))


# MOVEMENT
# Functions to select next node in a certain direction, if that node is valid
def l_node(grid, node):
    """Selects node to the left if available."""

    if node.row - 2 >= 0 and not grid[node.row - 1][node.col].is_hard_barrier:
        return grid[node.row - 1][node.col]
    return False


def r_node(grid, node):
    """Selects node to the right if available."""

    if (
        node.row + 2 <= len(grid[node.row])
        and not grid[node.row + 1][node.col].is_hard_barrier
    ):
        return grid[node.row + 1][node.col]
    return False


def u_node(grid, node):
    """Selects node above given node if available."""

    if node.col - 2 >= 0 and not grid[node.row][node.col - 1].is_hard_barrier:
        return grid[node.row][node.col - 1]
    return False


def d_node(grid, node):
    """Selects node below given node if available."""

    if node.col + 2 <= len(grid) and not grid[node.row][node.col + 1].is_hard_barrier:
        return grid[node.row][node.col + 1]
    return False


# List containing the movement helper functions to make them easy to iterate over
directions = [r_node, d_node, l_node, u_node]


# Maze type functions #####################################################
def completely_random(grid):
    """
    Generates a completely random maze, where every node has a 1 in 4 chance of
    becoming a barrier.
    """

    for row in grid:
        for node in row:
            if random.random() <= 0.25:
                make_node_barrier(node)
    return grid


def basic_swirl(grid):
    """
    Generates a simple swirl type maze.

    'Wall Adder' algorithm as it adds walls to an empty grid.
    """

    # Defines which nodes have been visited, used in one_direction function
    # Needs to be defined here so it can be checked on through different calls of
    # the one_direction function
    path = generate_blank_path(grid)

    def one_direction(grid, direction, start):
        """
        Uses a given movement function to keep moving in a specific direction
        until it hits a barrier.
        """

        node = start
        # Arbitrary path value just so the start node does not become a barrier
        path[start] = 1

        # Loop ends as soon as the next node in line is a barrier
        while node:
            # Must keep updating neighbours because barriers are getting added
            node.update_neighbours(grid)
            # Saving the current to a different variable
            prev_node = node
            # Checks next node in given direction
            node = direction(grid, node)
            path[node] = prev_node

            # If next node is not valid:
            if not node:
                # If previous node was the start node, break as no other direction
                # can therefore be taken
                if prev_node == start:
                    return False
                # Otherwise, return the previous node
                return prev_node

            # Make the neighbours of the previous node barriers, if they are not
            # yet visited and are not the current node
            for neighbour in prev_node.neighbours:
                if neighbour is not node and not path[neighbour]:
                    make_node_barrier(neighbour)

    # Always starts at top left corner
    start = grid[1][1]
    current = start
    # Loop breaks as soon as the one direction function returns False
    while current:
        # Iterates over movement functions and breaks loop if any of them return false
        for direction in directions:
            previous = current
            current = one_direction(grid, direction, previous)
            if not current:
                break

    return grid


def imperfect(grid):
    """
    My first attempt at a proper maze generating algorithm, this algorithm creates
    an imperfect maze (because some small chunks of the maze can be left
    inacessible).

    It works by adding horizontal and vertical walls of barrier nodes to the grid
    around a random start node then removing a single barrier from each wall.
    """

    # Defines which nodes have been visited/changed
    path = generate_blank_path(grid)

    # Keeps a List of what nodes are left to search
    available_nodes = [node for row in grid for node in row]
    # Gives the nodes a random order
    random.shuffle(available_nodes)

    def choose_node(grid):
        """Chooses a random, unvisited node for a wall to be drawn from."""

        while available_nodes:
            node = available_nodes.pop()
            node.update_neighbours(grid)
            if (
                not path[node]
                and not node.row % 2
                and not node.col % 2
                and not node.is_hard_barrier
                and len(node.neighbours) > 3
                and not node.is_hard_barrier
            ):
                return node
        return None

    # Loop ends as soon as there is no node left to go over (from choose_node)
    while True:
        start = choose_node(grid)
        if not start:
            break

        # Makes wall in each direction from the start node and opens a single node
        # on each wall
        for direction in directions:
            wall = make_wall(grid, start, direction, path)
            if not wall:
                continue
            make_opening(wall)

    return grid


def simple_maze(grid):
    """
    This algorithm was inspired by binary tree maze generation, but since the
    walls/barrierrs on this program are full cells rather than space between
    adjacent cells I had to play around with it and came up with this to take
    its place.

    It makes every odd row and column node into a barrier, then loops through the
    unaffected nodes and resets 2 adjacent barrier nodes at random.
    """

    # Goes through odd rows and columns and makes all of those nodes barriers
    for i, row in enumerate(grid):
        if not i % 2:
            for node in row:
                make_node_barrier(node)
        else:
            for j, node in enumerate(row):
                if not j % 2:
                    make_node_barrier(node)

    # Goes  through all the even rows and columns (currently open nodes surrounded
    # by barrier nodes) and chooses, at random, 2 adjacent barrier nodes and
    # resets them
    for i, row in enumerate(grid):
        if i % 2:
            for j, node in enumerate(row):
                if j % 2:
                    # Loops twice to select 2 nodes
                    for _ in range(2):
                        # Nodes chosen from directions: up, down
                        node = random.choice(
                            [
                                grid[i][j - 1],
                                grid[i][j + 1],
                                grid[i + 1][j],
                                grid[i - 1][j],
                            ]
                        )
                        node_reset(node)
    return grid
