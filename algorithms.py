from queue import PriorityQueue, Queue, LifoQueue
import pygame


# Algorithm Helper Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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


def open_node(end, neighbour):
    """Sets a node to open if it is not the end node."""

    if neighbour != end:
        neighbour.make_open()


def close_node(start, current):
    """Sets a node to closed if it is not the start node."""

    if current != start:
        current.make_closed()


# A* ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def a_star_algorithm(draw, grid, start, end):
    """
    Searches through nodes guided by a heuristic function which predicts the distance to the end node and prioritises which node to search based on this.
    This is usually the fastest algorithm, but this is beacuse it knows where the end point is (heuristic function) so it can search in the right direction.
    """

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
                    # Sets neighbour node to open
                    open_node(end, neighbour)
        # Update the display
        draw()

        # Closes the node after it has been looped through, but note it can be added back in and opened if another path to it is found
        close_node(start, current)

    return False


# Breadth first search -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def breadth_first_search(draw, grid, start, end):
    """Searches every possible path from node to node starting at the start node and returns the shortest."""

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
                # Sets neighbour node to open
                open_node(end, neighbour)
                path[neighbour] = current

        # Update the display
        draw()

        # Closes the node after it has been looped through
        close_node(start, current)

    return False


# Depth first search -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def depth_first_search(draw, grid, start, end):
    """
    Searches every possible path from the starting node and returns a route.

    Depth first search will be extremely innacurate at giving short paths in open mazes.
    This is because it searches nodes in order of top, right, bottom, left so it will always
    expand go to the left if possible (LIFO), often returning very longwinded routes to get to the end node.
    """

    # Queue allows nodes to be searched in a certain order
    # Operates on a FIFO basis
    open_set = LifoQueue()
    open_set.put(start)

    # Keeps track of node prior in the path to a certain node
    path = {}
    # Keeps track of whether a node has been visited already
    visited = {}

    # Add all nodes to path and visited so they can be used in if statements without throwing a key error
    for row in grid:
        for node in row:
            path[node] = None
            visited[node] = False

    # While loop runs until the end point is found or there are no nodes left to search
    while not open_set.empty():
        # Necessary as a new loop has been opened
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Gets first item in the queue which will always be the last node added (LIFO)
        current = open_set.get()
        visited[current] = True

        if current == end:
            reconstruct_final_path(path, current, draw, start, end)
            return True

        for neighbour in current.neighbours:
            # Neighbour is only added to queue if it has not yet been visited
            if visited[neighbour]:
                continue
            # If statement so start node's colour does not get altered
            if not neighbour == start:
                open_set.put(neighbour)
                # Sets neighbour node to open
                open_node(end, neighbour)
                path[neighbour] = current

        # Update the display
        draw()

        # Closes the node after it has been looped through
        close_node(start, current)

    return False


# Dijkstra's shortest path algorithm -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dijkstras(draw, grid, start, end):
    """Will appear extremely similar to breadth first search, but it is built to handle edges between nodes of different weights and uses a priority queue based on these weights."""

    # Will allow the algorithm to prioritise nodes with lower distance scores but since all edges have weight 1, visually this won't make much of a difference
    open_set = PriorityQueue()

    # Position of item added to the queue, required for the priority queue
    count = 0

    # Minimum distance to get to each node
    distance_score = {}
    # Contains each node's previous node in it's shortest path
    path = {}
    # Keeps track of which nodes have already been visited
    visited = {}

    # Add all nodes to path and visited so they can be used in if statements without throwing a key error
    # Give all nodes an infinite distance score so that any path that reaches them is shorter
    for row in grid:
        for node in row:
            path[node] = None
            distance_score[node] = float("inf")
            visited[node] = False

    # Set distance score of start node to 0 and add it to the open set
    distance_score[start] = 0
    open_set.put((distance_score[start], count, start))

    # Loop will end when the end node is reached or when there are no nodes left to search
    while not open_set.empty():
        # Gets node with lowest distance score and sets it to visited
        current = open_set.get()[2]
        visited[current] = True

        # Path is constructed as soon as the end node is reached
        # If the distance score was to be used, the distance to the end node would also have to be added
        if current == end:
            reconstruct_final_path(path, current, draw, start, end)
            return True

        # Loops through neighbours of the current node, which will always be valid neighbours (because of class function update_neighbours)
        for neighbour in current.neighbours:
            # If neighbour has been visited, skip
            if visited[neighbour]:
                continue

            # +1 because in this graph, the distance between all nodes is equivalent to 1 i.e. all edges have the same weight
            # If the edges had different weights, this is where the weight to that specific node would be taken into account
            if distance_score[current] + 1 < distance_score[neighbour]:
                # Update shortest path to that node
                distance_score[neighbour] = distance_score[current] + 1
                # Update count, again only for the priority queue functionality
                count += 1
                # Add neighbour to queue
                open_set.put((distance_score[neighbour], count, neighbour))
                # Update path for neighbour
                path[neighbour] = current
                # Sets neighbour node to open
                open_node(end, neighbour)

        # Update the display
        draw()

        # Closes the node after it has been looped through
        close_node(start, current)

    return False


# Greedy best-first search -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def best_first(draw, grid, start, end):
    """Uses the manhattan distance heuristic function like the a* algorithm, but does not take into account distance already travelled."""

    # Will allow the algorithm to prioritise nodes with lower distance scores but since all edges have weight 1, visually this won't make much of a difference
    open_set = PriorityQueue()
    # Position of item added to the queue, required for the priority queue
    count = 0

    # Distance to the end node (manhattan)
    distance_score = {}
    # Contains each node's previous node in it's shortest path. Also used to keep track of which nodes have been visited
    path = {}

    # Add all nodes to path so they can be used in if statements without throwing a key error
    # Give all nodes a distance score calculated with the heuristic function
    for row in grid:
        for node in row:
            path[node] = None
            distance_score[node] = heur(node.get_position(),
                                        end.get_position()
                                        )

    # Add start node to the open set
    open_set.put((distance_score[start], count, start))

    # Loop will end when the end node is reached or when there are no nodes left to search
    while not open_set.empty():
        # Gets node with lowest distance score
        current = open_set.get()[2]

        # Path is constructed as soon as the end node is reached
        if current == end:
            reconstruct_final_path(path, current, draw, start, end)
            return True

        # Loops through neighbours of the current node, which will always be valid neighbours (because of class function update_neighbours)
        for neighbour in current.neighbours:
            # If neighbour has been visited, skip
            if path[neighbour]:
                continue

            # Update path to neighbour
            path[neighbour] = current
            # Update count, again only for the priority queue functionality
            count += 1
            # Add neighbour to queue
            open_set.put((distance_score[neighbour], count, neighbour))
            # Sets neighbour node to open
            open_node(end, neighbour)

        # Update the display
        draw()

        # Closes the node after it has been looped through
        close_node(start, current)

    return False
