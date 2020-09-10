from queue import PriorityQueue
import pygame


# Algorithm Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def heur(p1, p2):
    """
    Heuristic function, gets a prediction for the distance from the given node to the end node, which is used to
    guide the a* algorithm on which node to search next.
    Uses Manhattan distance, which simply draws an L to the end node.
    """

    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_final_path(path, current, draw):
    """Goes through each node in the path calculated by the algorithm function, and draws out the path on the display."""

    while current in path:
        # path contains nodes as node: node before that node with lowest g_score,
        # so this goes through the nodes backwards from ends with the lowest g_scores
        current = path[current]
        current.make_path()
        draw()


def a_star_algorithm(draw, grid, start, end):
    # Keeps track of when node is inserted to the queue
    count = 0
    # Will be used to ge the minimum element from the queue, based on the f_score
    open_set = PriorityQueue()
    # add start node to open set, count to keep track of when item was inserted to queue
    open_set.put((0, count, start))
    # keeps track of node prior in the path to the current node, updated if a new node with lower g_score is found
    path = {}

    # Current shortest distance to get from the start node to this node
    # Initialised at infinity and updated as the node is reached, so any number is lower than it
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    # G score + predicted distance to the end node, defined by the heuristic function
    # Will be used to determine which node should come next in the priority queue
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heur(start.get_position(), end.get_position())

    # To keep track of which items are in the priority queue
    open_set_hash = {start}

    while not open_set.empty():
        # Necessary as a new loop has been opened
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Node with the lowest f score gets chosen first thanks to the priority queue
        current = open_set.get()[2]
        # To sync list with priority queue
        open_set_hash.remove(current)

        # As soon as the end node is reached, the path is built and the loop ends
        if current == end:
            reconstruct_final_path(path, end, draw)
            # Make start and end nodes change colour back to their original, and not the path colour
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            # all edges have weight 1, so g_score for the node is g_score for previous node + 1
            temp_g_score = g_score[current] + 1

            # Update g_score and f_score if a new shorter path is found
            if temp_g_score < g_score[neighbour]:
                path[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + \
                    heur(neighbour.get_position(), end.get_position())

                # Add neighbour node to open_set_hash and open_set
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        # Update the display
        draw()

        # Closes the node after it has been looped through, but note it can be added back in and opened if another path to it is found
        if current != start:
            current.make_closed()

    return False
