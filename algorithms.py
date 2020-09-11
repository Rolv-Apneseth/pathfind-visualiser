from queue import PriorityQueue, Queue
import pygame


# Algorithm Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def reconstruct_final_path(path, current, draw, start, end):
    """Goes through each node in the path calculated by an algorithm function, and draws out the path on the display."""

    while current in path:
        # path contains nodes as node: node before that node,
        # so this goes through the nodes backwards from the end node to the start node
        current = path[current]
        current.make_path()
        draw()
        if current == start:
            break

    # Make start and end nodes change colour back to their original, and not the path colour
    end.make_end()
    start.make_start()


def heur(p1, p2):
    """
    Heuristic function, gets a prediction for the distance from the given node to the end node, which is used to
    guide the a* algorithm on which node to search next.
    Uses Manhattan distance, which simply draws an L to the end node.
    """

    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# A* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def a_star_algorithm(draw, grid, start, end):
    """Searches through nodes guided by a heuristic function which predicts the distance to the end node and prioritises which node to search based on this."""

    # Keeps track of when node is inserted to the queue
    count = 0
    # Will be used to ge the minimum element from the queue, based on the f_score
    open_set = PriorityQueue()
    # add start node to open set, count to keep track of when item was inserted to queue
    open_set.put((0, count, start))
    # keeps track of node prior in the path to a certain node, updated if a new node with lower g_score is found
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
            reconstruct_final_path(path, end, draw, start, end)
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


# Breadth first search --------------------------------------------------------------------------------
def breadth_first_search(draw, grid, start, end):
    """Searches every possible path from the starting node and returns the shortest."""

    # Queue allows nodes to be searched in a certain order
    # Operates on a FIFO basis
    open_set = Queue()
    open_set.put(start)

    # Keeps track of node prior in the path to a certain node
    path = {}
    # Add all nodes to path so they can be used in if statements without throwing a key error
    for row in grid:
        for node in row:
            path[node] = None

    while not open_set.empty():
        # Necessary as a new loop has been opened
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Gets first item in the queue which will always be the item added before all the others (FIFO_)
        current = open_set.get()

        if current == end:
            reconstruct_final_path(path, current, draw, start, end)
            return True

        for neighbour in current.neighbours:
            # Neighbour is only added to queue if it has not yet been visited
            if path[neighbour]:
                continue
            # If statement so start node's colour does not get altered
            if not neighbour == start:
                open_set.put(neighbour)
                neighbour.make_open()
                path[neighbour] = current

        # Update the display
        draw()

        # Closes the node after it has been looped through, but note it can be added back in and opened if another path to it is found
        if not current == start:
            current.make_closed()

    return False
