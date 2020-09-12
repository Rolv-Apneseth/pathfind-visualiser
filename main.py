import pygame

# Custom module imports
import board
import algorithms
from buttons import Button

# COLOURS
BUTTON1 = (0, 0, 0)  # Black
BUTTON2 = (255, 255, 255)  # White
BUTTON3 = (162, 162, 162)  # Silver
BG_LINES = (255, 255, 255)  # White
BG = (108, 0, 108)   # Purple
TEXT_COLOUR = (0, 0, 0)  # Black

# FONTS
pygame.font.init()
title_font = pygame.font.SysFont("arial", 40, bold=True)
button_font = pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont("arial", 20, bold=True)
tiny_font = pygame.font.SysFont("arial", 15)
tiny_bold_font = pygame.font.SysFont("arial", 15, bold=True)


# Extra Draw UI Functions -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def draw_main_background(window, size):
    window.fill(BG)
    pygame.draw.rect(window, BG_LINES, (0,
                                        size // 10 - size // 15,
                                        size,
                                        size // 15
                                        ))
    pygame.draw.rect(window, BG_LINES, (size // 10 - size // 15,
                                        0,
                                        size // 15,
                                        size
                                        ))


def draw_key(window, size):
    # Background
    bg_colour = BG_LINES

    pygame.draw.rect(window, bg_colour, (size * 13 // 60,
                                         size * 40 // 60,
                                         size * 2 // 10,
                                         size * 3 // 10
                                         ))

    # Labels definitions
    start_label = tiny_font.render("Start node", 1, TEXT_COLOUR)
    end_label = tiny_font.render("End node", 1, TEXT_COLOUR)
    barrier_label = tiny_font.render("Untraversable", 1, TEXT_COLOUR)
    open_label = tiny_font.render("Traversable", 1, TEXT_COLOUR)
    closed_label = tiny_font.render("Already traversed", 1, TEXT_COLOUR)
    path_label = tiny_font.render("Ideal path", 1, TEXT_COLOUR)
    # Label placement
    window.blit(start_label, (size * 4 // 15, size * 41 // 60))
    window.blit(end_label, (size * 4 // 15, size * 44 // 60))
    window.blit(barrier_label, (size * 4 // 15, size * 47 // 60))
    window.blit(open_label, (size * 4 // 15, size * 50 // 60))
    window.blit(closed_label, (size * 4 // 15, size * 53 // 60))
    window.blit(path_label, (size * 4 // 15, size * 56 // 60))
    # SQUARES
    # start
    pygame.draw.rect(window, board.START, (size * 14 // 60,
                                           size * 41 // 60,
                                           size // 50,
                                           size // 50
                                           ))
    # end
    pygame.draw.rect(window, board.END, (size * 14 // 60,
                                         size * 44 // 60,
                                         size // 50,
                                         size // 50
                                         ))
    # barrier
    pygame.draw.rect(window, board.BARRIER, (size * 14 // 60,
                                             size * 47 // 60,
                                             size // 50,
                                             size // 50
                                             ))
    # open
    pygame.draw.rect(window, board.OPEN, (size * 14 // 60,
                                          size * 50 // 60,
                                          size // 50,
                                          size // 50
                                          ))
    # closed
    pygame.draw.rect(window, board.CLOSED, (size * 14 // 60,
                                            size * 53 // 60,
                                            size // 50,
                                            size // 50
                                            ))
    # path
    pygame.draw.rect(window, board.PATH, (size * 14 // 60,
                                          size * 56 // 60,
                                          size // 50,
                                          size // 50
                                          ))


def draw_controls(window, size):
    # Background
    bg_colour = BG_LINES

    pygame.draw.rect(window, bg_colour, (size * 36 // 60,
                                         size * 40 // 60,
                                         size * 3 // 10,
                                         size * 3 // 10
                                         ))
    # Labels definitions
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
    # left click
    window.blit(left1_label, (size * 37 // 60, size * 42 // 60))
    window.blit(left2_label, (size * 44 // 60, size * 42 // 60))
    # right click
    window.blit(right1_label, (size * 37 // 60, size * 45 // 60))
    window.blit(right2_label, (size * 44 // 60, size * 45 // 60))
    # c
    window.blit(c1_label, (size * 37 // 60, size * 48 // 60))
    window.blit(c2_label, (size * 44 // 60, size * 48 // 60))
    # spacebar
    window.blit(space1_label, (size * 37 // 60, size * 51 // 60))
    window.blit(space2_label, (size * 44 // 60, size * 51 // 60))
    # escape
    window.blit(escape1_label, (size * 37 // 60, size * 54 // 60))
    window.blit(escape2_label, (size * 44 // 60, size * 54 // 60))


# Main Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def run_algorithms(window, size, rows, algorithm):

    grid = board.make_grid(rows, size)

    start = None
    end = None

    run = True
    # Keeps track of whether algorithm has been started, so user input can be disabled for its duration
    started = False

    while run:
        board.draw_board(window, grid, rows, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            # If algorithm has started, does not allow the user to change nodes
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
                    grid = board.make_grid(rows, size)

            # Starts the a* pathfinding algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not started:
                    # Prevents user from starting the search again while a search is underway
                    started = True
                    # Add neighbours to each node, not including barriers
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    # Lambda function allows function with these perimeters to be calles over and over without having to assign another function
                    # specifically to that

                    # Which algorithm to use:
                    if algorithm == "a*":
                        algorithms.a_star_algorithm(lambda: board.draw_board(window, grid,
                                                                             rows, size), grid, start, end)

                    if algorithm == "breadth first":
                        algorithms.breadth_first_search(lambda: board.draw_board(window, grid,
                                                                                 rows, size), grid, start, end)

                    if algorithm == "depth first":
                        algorithms.depth_first_search(lambda: board.draw_board(window, grid,
                                                                               rows, size), grid, start, end)

                    if algorithm == "dijkstra's":
                        algorithms.dijkstras(lambda: board.draw_board(window, grid,
                                                                      rows, size), grid, start, end)

                    # Reset started variable so that user can again give commands
                    started = False


def main(window, size, rows):
    # Variable to check if the left mouse button has been pressed
    clicked = False

    # Will contain all the buttons, so they can be looped through in a for loop
    buttons = []

    # DEFINE LABELS
    title_label = title_font.render(
        "Choose an algorithm to begin:", 1, TEXT_COLOUR)

    key_label = small_font.render("Key:", 1, TEXT_COLOUR)

    controls_label = small_font.render("Controls:", 1, TEXT_COLOUR)

    # DEFINE BUTTONS
    # A* pathfinding algorithm
    a_star_button = Button(BUTTON1,
                           BUTTON2,
                           size // 2 - size // 8,  # Removing half the width so it's in the middle
                           size * 2 // 10,
                           size // 4,
                           size // 15,
                           lambda: run_algorithms(window, size, rows, "a*"),
                           text='A*',
                           outline=BUTTON3
                           )
    buttons.append(a_star_button)
    # Breadth first search algorithm
    breadth_first_button = Button(BUTTON1,
                                  BUTTON2,
                                  # Removing half the width so it's in the middle, same for the other buttons
                                  size // 2 - size // 6,
                                  size * 3 // 10,
                                  size // 3,
                                  size // 15,
                                  lambda: run_algorithms(
                                      window, size, rows, "breadth first"),
                                  text='Breadth first search',
                                  outline=BUTTON3
                                  )
    buttons.append(breadth_first_button)
    # Depth first search algorithm
    depth_first_button = Button(BUTTON1,
                                BUTTON2,
                                size // 2 - size // 6,
                                size * 4 // 10,
                                size // 3,
                                size // 15,
                                lambda: run_algorithms(
                                    window, size, rows, "depth first"),
                                text='Depth first search',
                                outline=BUTTON3
                                )
    buttons.append(depth_first_button)
    # Dijkstra's shortest path algorithm
    dijkstra_button = Button(BUTTON1,
                             BUTTON2,
                             size // 2 - size // 6,
                             size * 5 // 10,
                             size // 3,
                             size // 15,
                             lambda: run_algorithms(
                                 window, size, rows, "dijkstra's"),
                             text="Dijkstra's algorithm",
                             outline=BUTTON3
                             )
    buttons.append(dijkstra_button)

    run = True
    while run:

        draw_main_background(window, size)
        draw_key(window, size)
        draw_controls(window, size)

        # Labels
        window.blit(title_label, (size // 2 - title_label.get_width() // 2,  # So that the label is placed in the middle of the screen
                                  size // 25
                                  ))
        window.blit(key_label, (size * 2 // 15, size * 10 // 15))
        window.blit(controls_label, (size * 7 // 15, size * 10 // 15))

        # Buttons
        xpos, ypos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(window, button_font, xpos, ypos)

            if button.is_selected(xpos, ypos):
                if clicked:
                    button.on_clicked()
        # Reset the clicked value
        clicked = False

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                clicked = True

        pygame.display.update()


if __name__ == "__main__":
    # Pygame Window
    # Window will always be a square so size used instead of width and height
    SIZE = 800
    ROWS = 50
    WIN = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("Pathfinding Algorithms Visualiser")

    # run_algorithms(WIN, SIZE, ROWS, "a*")
    main(WIN, SIZE, ROWS)
