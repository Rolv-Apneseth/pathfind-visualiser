import pygame

# Custom module imports
from pathfind_visualiser import algorithms, board, maze
from pathfind_visualiser.buttons import Button
from pathfind_visualiser.dropdown import Dropdown

# MEASUREMENTS
# Window will always be a square
SIZE = 825
# Default number of rows, will be changed in game
ROWS = 25

# COLOURS
BUTTON1 = (0, 0, 0)
BUTTON2 = (255, 255, 255)
BUTTON3 = (162, 162, 162)
BG = (150, 150, 150)
# Same as BG but change this for different frame colours
BG2 = (150, 150, 150)
OUTLINE_COLOUR = (0, 0, 0)
TEXT_COLOUR = (0, 0, 0)

# FONTS
pygame.font.init()
title_font = pygame.font.SysFont("arial", 40, bold=True)
button_font = pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont("arial", 20, bold=True)
tiny_font = pygame.font.SysFont("arial", 15)
tiny_bold_font = pygame.font.SysFont("arial", 15, bold=True)


# Extra Draw UI Functions #####################################################
def outline_rect(window, size, x, y, width, height):
    """
    Draws a black rectangle, slightly bigger than the measurements passed in.

    Use this as a background for another rectangle to give it an outline. (Just
    give the measurements for that rectangle).
    """

    outline_colour = OUTLINE_COLOUR

    # Outline width
    extra_size = size // 400

    pygame.draw.rect(
        window,
        outline_colour,
        (
            x - extra_size,
            y - extra_size,
            width + extra_size * 2,
            height + extra_size * 2,
        ),
    )


def draw_background(window, size, x, y, width, height):
    """Draws a frame to contain other ui elements. Has a thin black border."""
    bg_colour = BG2
    # Draws outline around background
    outline_rect(window, size, x, y, width, height)
    # Draws background surface
    pygame.draw.rect(window, bg_colour, (x, y, width, height))


def draw_instructions(window, size):
    """
    Draw elements onto the gui which give text instructions on how to use the
    program.
    """

    # BACKGROUND
    # Measurements, all label placements will be based off these as well
    x = size // 20
    y = size // 10
    width = size // 2
    height = size * 17 // 40

    draw_background(window, size, x, y, width, height)

    # DEFINE LABELS
    # title
    instructions_label = small_font.render("Instructions", 1, TEXT_COLOUR)

    # Instructions
    line1 = tiny_font.render(
        "1. Look over the controls and key on the right.", 1, TEXT_COLOUR
    )

    line2 = tiny_font.render(
        "2. Choose which pathfinding algorithm you would like to", 1, TEXT_COLOUR
    )
    line3 = tiny_font.render(
        "     visualise down below. This will open another window.", 1, TEXT_COLOUR
    )

    line4 = tiny_font.render(
        "3. Choose a start and end point. This can be done by left", 1, TEXT_COLOUR
    )
    line5 = tiny_font.render(
        "      clicking any 2 nodes. Reset any node with a right click.", 1, TEXT_COLOUR
    )

    line6 = tiny_font.render(
        "4. Any further left clicks will change empty nodes into", 1, TEXT_COLOUR
    )
    line7 = tiny_font.render(
        "      barriers, which cannot be traversed.", 1, TEXT_COLOUR
    )

    line8 = tiny_font.render(
        "5. To visualise the pathfinding algorithm, press the spacebar.", 1, TEXT_COLOUR
    )
    line9 = tiny_font.render(
        "      Once it has finished, you can clear the board with the c", 1, TEXT_COLOUR
    )
    line10 = tiny_font.render(
        "      key, or just move the end or start points and run again.", 1, TEXT_COLOUR
    )
    line11 = tiny_font.render(
        "      Hit the esc key to return to the main menu.", 1, TEXT_COLOUR
    )

    line12 = tiny_font.render(
        "Don't forget to try out different row sizes and mazes too!", 1, TEXT_COLOUR
    )

    # LABEL PLACEMENT
    window.blit(instructions_label, (x + size // 80, y + size // 80))

    window.blit(line1, (x + size // 80, y + size * 4 // 80))

    window.blit(line2, (x + size // 80, y + size * 7 // 80))
    window.blit(line3, (x + size // 80, y + size * 9 // 80))

    window.blit(line4, (x + size // 80, y + size * 12 // 80))
    window.blit(line5, (x + size // 80, y + size * 14 // 80))

    window.blit(line6, (x + size // 80, y + size * 17 // 80))
    window.blit(line7, (x + size // 80, y + size * 19 // 80))

    window.blit(line8, (x + size // 80, y + size * 22 // 80))
    window.blit(line9, (x + size // 80, y + size * 24 // 80))
    window.blit(line10, (x + size // 80, y + size * 26 // 80))
    window.blit(line11, (x + size // 80, y + size * 28 // 80))

    window.blit(line12, (x + size // 80, y + size * 31 // 80))


def draw_key(window, size):
    """
    Draws elements onto the gui which show the user what each colour node means
    within the program.
    """

    # BACKGROUND
    # Measurements, all label placements will be based off these as well
    x = size * 37 // 60
    y = size * 6 // 60
    width = size * 7 // 20
    height = size * 4 // 20

    draw_background(window, size, x, y, width, height)

    # DEFINE LABELS
    key_label = small_font.render("Key", 1, TEXT_COLOUR)
    start_label = tiny_font.render("Start node", 1, TEXT_COLOUR)
    end_label = tiny_font.render("End node", 1, TEXT_COLOUR)
    barrier_label = tiny_font.render("Untraversable", 1, TEXT_COLOUR)
    open_label = tiny_font.render("Traversable", 1, TEXT_COLOUR)
    closed_label = tiny_font.render("Already traversed", 1, TEXT_COLOUR)
    path_label = tiny_font.render("Ideal path", 1, TEXT_COLOUR)
    # LABEL PLACEMENT
    # key
    window.blit(key_label, (x + size // 80, y + size // 80))
    # start
    window.blit(start_label, (x + size * 3 // 80, y + size * 4 // 80))
    # end
    window.blit(end_label, (x + size * 16 // 80, y + size * 4 // 80))
    # barrier
    window.blit(barrier_label, (x + size * 3 // 80, y + size * 8 // 80))
    # path
    window.blit(path_label, (x + size * 16 // 80, y + size * 8 // 80))
    # open
    window.blit(open_label, (x + size * 3 // 80, y + size * 12 // 80))
    # closed
    window.blit(closed_label, (x + size * 16 // 80, y + size * 12 // 80))

    # SQUARES
    # start
    pygame.draw.rect(
        window,
        board.START,
        (x + size // 80, y + size * 4 // 80, size // 50, size // 50),
    )
    # end
    pygame.draw.rect(
        window,
        board.END,
        (x + size * 14 // 80, y + size * 4 // 80, size // 50, size // 50),
    )
    # barrier
    pygame.draw.rect(
        window,
        board.BARRIER,
        (x + size // 80, y + size * 8 // 80, size // 50, size // 50),
    )
    # path
    pygame.draw.rect(
        window,
        board.PATH,
        (x + size * 14 // 80, y + size * 8 // 80, size // 50, size // 50),
    )
    # open
    pygame.draw.rect(
        window,
        board.OPEN,
        (x + size // 80, y + size * 12 // 80, size // 50, size // 50),
    )
    # closed
    pygame.draw.rect(
        window,
        board.CLOSED,
        (x + size * 14 // 80, y + size * 12 // 80, size // 50, size // 50),
    )


def draw_controls(window, size):
    """
    Draws elements onto the gui which show the user what buttons to press to do
    what when the program is running.
    """

    # BACKGROUND
    # Measurements, all label placements will be based off these as well
    x = size * 37 // 60
    y = size * 21 // 60
    width = size * 7 // 20
    height = size * 7 // 40

    draw_background(window, size, x, y, width, height)

    # DEFINE LABELS
    controls_label = small_font.render("Controls", 1, TEXT_COLOUR)

    left1_label = tiny_bold_font.render("Left click:", 1, TEXT_COLOUR)
    left2_label = tiny_font.render("Change node", 1, TEXT_COLOUR)

    right1_label = tiny_bold_font.render("Right click:", 1, TEXT_COLOUR)
    right2_label = tiny_font.render("Reset node", 1, TEXT_COLOUR)

    c1_label = tiny_bold_font.render("C:", 1, TEXT_COLOUR)
    c2_label = tiny_font.render("Reset all nodes", 1, TEXT_COLOUR)

    space1_label = tiny_bold_font.render("Spacebar:", 1, TEXT_COLOUR)
    space2_label = tiny_font.render("Start algorithm", 1, TEXT_COLOUR)

    escape1_label = tiny_bold_font.render("Escape:", 1, TEXT_COLOUR)
    escape2_label = tiny_font.render("Return to menu", 1, TEXT_COLOUR)

    # LABEL PLACEMENT
    # title
    window.blit(controls_label, (x + size // 80, y + size // 80))
    # left click
    window.blit(left1_label, (x + size // 80, y + size * 4 // 80))
    window.blit(left2_label, (x + size * 10 // 80, y + size * 4 // 80))
    # right click
    window.blit(right1_label, (x + size // 80, y + size * 6 // 80))
    window.blit(right2_label, (x + size * 10 // 80, y + size * 6 // 80))
    # c
    window.blit(c1_label, (x + size // 80, y + size * 8 // 80))
    window.blit(c2_label, (x + size * 10 // 80, y + size * 8 // 80))
    # spacebar
    window.blit(space1_label, (x + size // 80, y + size * 10 // 80))
    window.blit(space2_label, (x + size * 10 // 80, y + size * 10 // 80))
    # escape
    window.blit(escape1_label, (x + size // 80, y + size * 12 // 80))
    window.blit(escape2_label, (x + size * 10 // 80, y + size * 12 // 80))


def draw_buttons(window, size, rows, xpos, ypos, clicked, maze_type):
    """
    Displays buttons which will each run the program with a specific algorithm.
    """

    # BACKGROUND
    draw_background(
        window,
        size,
        size // 20,  # x
        size * 25 // 40,  # y
        size // 2,  # width
        size * 29 // 80,  # height
    )

    # DEFINE BUTTONS
    # Will contain all the buttons, so they can be looped through in a for loop
    buttons = []

    # A* pathfinding algorithm
    a_star_button = Button(
        BUTTON1,
        BUTTON2,
        size // 20,
        size * 25 // 40,
        size * 7 // 16,
        size // 15,
        lambda: run_algorithms(window, size, rows, "a*", maze_type),
        text="A* Search Algorithm",
    )
    buttons.append(a_star_button)
    # Breadth first search algorithm
    breadth_first_button = Button(
        BUTTON1,
        BUTTON2,
        size // 20,
        size * 28 // 40,
        size * 7 // 16,
        size // 15,
        lambda: run_algorithms(window, size, rows, "breadth first", maze_type),
        text="Breadth-First Search",
    )
    buttons.append(breadth_first_button)
    # Depth first search algorithm
    depth_first_button = Button(
        BUTTON1,
        BUTTON2,
        size // 20,
        size * 31 // 40,
        size * 7 // 16,
        size // 15,
        lambda: run_algorithms(window, size, rows, "depth first", maze_type),
        text="Depth-First Search",
    )
    buttons.append(depth_first_button)
    # Dijkstra's shortest path algorithm
    dijkstra_button = Button(
        BUTTON1,
        BUTTON2,
        size // 20,
        size * 34 // 40,
        size * 7 // 16,
        size // 15,
        lambda: run_algorithms(window, size, rows, "dijkstra's", maze_type),
        text="Dijkstra's Algorithm",
    )
    buttons.append(dijkstra_button)
    # Greedy best-first search algorithm
    best_first_button = Button(
        BUTTON1,
        BUTTON2,
        size // 20,
        size * 37 // 40,
        size * 7 // 16,
        size // 15,
        lambda: run_algorithms(window, size, rows, "best-first", maze_type),
        text="Greedy Best-First Search",
    )
    buttons.append(best_first_button)

    # Loop through the buttons and execute their function if they are selected and
    # the mouse has been clicked
    for button in buttons:
        button.draw(window, button_font, xpos, ypos)

        if button.is_selected(xpos, ypos):
            if clicked:
                button.on_clicked()


def draw_options(window, size):
    """
    Draws option elements onto the gui (labels for row and maze dropdowns which
    are defined in main()).
    """

    # MEASUREMENTS
    x = size * 37 // 60
    y = size * 25 // 40
    width = size * 7 // 20
    height = size * 29 // 80

    # BACKGROUND
    draw_background(window, size, x, y, width, height)

    # DEFINE LABELS
    options_label = small_font.render("Options", 1, TEXT_COLOUR)

    rows_label = tiny_font.render("Number of rows/columns:", 1, TEXT_COLOUR)
    maze_type_label = tiny_font.render("Type of maze to use:", 1, TEXT_COLOUR)

    # LABEL PLACEMENT
    window.blit(options_label, (x + size // 80, y + size // 80))

    window.blit(rows_label, (x + size // 80, y + size * 5 // 80))
    window.blit(maze_type_label, (x + size // 80, y + size * 10 // 80))


# Main Functions #####################################################
def run_algorithms(window, size, rows, algorithm, maze_type):
    """Runs the maze window, where the chosen algorithm can be executed."""

    grid = board.make_grid(rows, size)

    if maze_type == "Random":
        grid = maze.completely_random(grid)
    if maze_type == "Swirl":
        grid = maze.basic_swirl(grid)
    if maze_type == "Imperfect":
        grid = maze.imperfect(grid)
    if maze_type == "Simple":
        grid = maze.simple_maze(grid)

    start = None
    end = None

    run = True
    # Keeps track of whether algorithm has been started, so user input can be
    # disabled for its duration
    started = False

    while run:
        board.draw_board(window, grid, rows, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            # If algorithm has started, does not allow the user to give commands
            if started:
                continue

            # Changing nodes
            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_position(pos, rows, size)
                node = grid[row][col]
                if not start and node != end and not node.is_hard_barrier:
                    start = node
                    start.make_start()
                elif not end and node != start and not node.is_hard_barrier:
                    end = node
                    end.make_end()
                elif node != end and node != start and not node.is_hard_barrier:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_position(pos, rows, size)
                node = grid[row][col]
                if not node.is_hard_barrier:
                    node.reset()

                    # Reset start and end if they are deleted
                    if node == start:
                        start = None
                    if node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                # Pressing c resets all nodes
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    for row in grid:
                        for node in row:
                            if not node.is_hard_barrier:
                                node.reset()

            # Starts the chosen algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not started:
                    started = True
                    # Update possible neighbours for every node
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    # Which algorithm to use:
                    if algorithm == "a*":
                        algorithms.a_star_algorithm(
                            lambda: board.draw_board(window, grid, rows, size),
                            grid,
                            start,
                            end,
                        )

                    if algorithm == "breadth first":
                        algorithms.breadth_first_search(
                            lambda: board.draw_board(window, grid, rows, size),
                            grid,
                            start,
                            end,
                        )

                    if algorithm == "depth first":
                        algorithms.depth_first_search(
                            lambda: board.draw_board(window, grid, rows, size),
                            grid,
                            start,
                            end,
                        )

                    if algorithm == "dijkstra's":
                        algorithms.dijkstras(
                            lambda: board.draw_board(window, grid, rows, size),
                            grid,
                            start,
                            end,
                        )

                    if algorithm == "best-first":
                        algorithms.best_first(
                            lambda: board.draw_board(window, grid, rows, size),
                            grid,
                            start,
                            end,
                        )

                    started = False


def run_main_menu(window, size, rows):
    """
    Runs the main menu window where the user can customise the maze and execute
    the chosen algorithm.
    """

    # Variable to check if the left mouse button has been pressed - used for
    # buttons and dropdown menus
    clicked = False

    # Variable to set the maze type for the grid
    maze_type = None

    # DEFINE LABELS
    # Title
    choose_label = title_font.render("Algorithms:", 1, TEXT_COLOUR)
    # How to use
    usage_label = title_font.render("How to use:", 1, TEXT_COLOUR)

    # DEFINE DROPDOWNS
    # rows
    rows_drop = Dropdown(
        BUTTON1,
        BUTTON2,
        BUTTON1,
        BUTTON2,
        size * 67 // 80,
        size * 54 // 80,
        size // 10,
        size // 25,
    )

    # No function needed for each option as it only changes a variable so None used
    rows_drop.add_options(("25", None), ("55", None), ("75", None))
    # Local variable to manage whether options list for rows_drop is displayed
    display_rows_options = False

    # maze type
    maze_type_drop = Dropdown(
        BUTTON1,
        BUTTON2,
        BUTTON1,
        BUTTON2,
        size * 67 // 80,
        size * 59 // 80,
        size // 10,
        size // 25,
    )
    maze_type_drop.add_options(
        ("None", None),
        ("Random", None),
        ("Swirl", None),
        ("Imperfect", None),
        ("Simple", None),
    )
    # Local variable to manage whether options list for maze_type_drop is displayed
    display_maze_options = False

    run = True
    while run:
        window.fill(BG)

        draw_instructions(window, size)
        draw_key(window, size)
        draw_controls(window, size)

        # Get mouse position
        xpos, ypos = pygame.mouse.get_pos()

        draw_buttons(window, size, rows, xpos, ypos, clicked, maze_type)
        draw_options(window, size)

        # LABELS
        window.blit(choose_label, (size // 20, size * 22 // 40))
        window.blit(usage_label, (size // 20, size // 40))

        # DROPDOWNS
        # Rows
        rows_drop.draw_main(window, button_font, xpos, ypos)

        # Checks if row options should be displayed
        if (
            rows_drop.is_selected_main(xpos, ypos)
            and clicked
            and not display_rows_options
        ):
            display_rows_options = True
        elif rows_drop.is_selected_main(xpos, ypos) and clicked and display_rows_options:
            display_rows_options = False

        # If a row option is clicked, sets the selected value to the row option
        # clicked and closes the row options dropdown
        if display_rows_options:
            rows_drop.draw_options(window, button_font, xpos, ypos)
            for i, option in enumerate(rows_drop.options):
                if rows_drop.is_selected_option(xpos, ypos, i) and clicked:
                    rows_drop.selected_option = option[0]
                    rows = int(option[0])
                    display_rows_options = False

        # Maze type
        # Not displayed if row options are displayed so they do not overlap
        if not display_rows_options:
            maze_type_drop.draw_main(window, button_font, xpos, ypos)

            # Checks if maze options should be displayed
            if clicked and maze_type_drop.is_selected_main(xpos, ypos):
                display_maze_options = not display_maze_options

            # If a maze option is clicked, sets the selected value to the maze
            # option clicked and closes the maze options dropdown
            if display_maze_options:
                maze_type_drop.draw_options(window, button_font, xpos, ypos)
                for i, option in enumerate(maze_type_drop.options):
                    if maze_type_drop.is_selected_option(xpos, ypos, i) and clicked:
                        maze_type_drop.selected_option = option[0]
                        maze_type = option[0]
                        display_maze_options = False

        clicked = False

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Used in conjunction with mouse position to detect when certain gui
            # elements have been clicked
            if pygame.mouse.get_pressed()[0]:
                clicked = True

        pygame.display.update()


def main():
    WIN = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Pathfinding Algorithms Visualiser")

    run_main_menu(WIN, SIZE, ROWS)


if __name__ == "__main__":
    main()
