import random


# Helper functions ----------------------------------------------------------------------------------------------------------------------------------
def make_node_barrier(node):
    """Turns a node into a hard barrier."""

    node.make_barrier()
    node.is_hard_barrier = True
    return node


def generate_blank_path(grid):
    """Makes an empty path dictionary."""

    return {node: None for row in grid for node in row}

# Maze type functions -----------------------------------------------------------------------------------------------------------------------------


def completely_random(grid):
    """Generates a completely random maze, where every node has a 1 in 4 chance of becoming a barrier."""

    for row in grid:
        for node in row:
            if random.random() <= 0.25:
                make_node_barrier(node)
    return grid


def basic_swirl(grid):
    """Generates a simple swirl type maze."""

    # Defines which nodes have been visited, used in the one_direction function
    path = generate_blank_path(grid)

    # MOVEMENT
    # Functions to select next node in a certain direction, if that node is valid
    def l_node(node):
        """Selects node to the left if available."""

        if node.row - 2 >= 0 and not grid[node.row - 1][node.col].is_hard_barrier:
            return grid[node.row - 1][node.col]
        return False

    def r_node(node):
        """Selects node to the right if available."""

        if node.row + 2 <= len(grid[node.row]) and not grid[node.row + 1][node.col].is_hard_barrier:
            return grid[node.row + 1][node.col]
        return False

    def u_node(node):
        """Selects node above given node if available."""

        if node.col - 2 >= 0 and not grid[node.row][node.col - 1].is_hard_barrier:
            return grid[node.row][node.col - 1]
        return False

    def d_node(node):
        """Selects node below given node if available."""

        if node.col + 2 <= len(grid) and not grid[node.row][node.col + 1].is_hard_barrier:
            return grid[node.row][node.col + 1]
        return False

    # List containing the above functions to make them easy to iterate over
    directions = [r_node, d_node, l_node, u_node]

    def one_direction(grid, direction, start):
        """Uses a given movement function to keep moving in a specific direction until it hits a barrier."""

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
            node = direction(node)
            path[node] = prev_node

            # If next node is not valid:
            if not node:
                # If previous node was the start node, break as no other direction can therefore be taken
                if prev_node == start:
                    return False
                # Otherwise, return the previous node
                return prev_node

            # Make the neighbours of the previous node barriers, if they are not yet visited and are not the current node
            for neighbour in prev_node.neighbours:
                if neighbour is not node and not path[neighbour]:
                    make_node_barrier(neighbour)

    # Always starts at top left corner
    start = grid[1][1]
    current = start
    # Loop breaks as soon as the one direction function returns False
    while current:
        for direction in directions:
            previous = current
            current = one_direction(grid, direction, previous)
            if not current:
                break

    return grid
