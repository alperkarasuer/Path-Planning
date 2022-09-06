import pygame
from consts import *
from board import Board, Cell, np
from astar import astar


def drawTheGrid():
    # Draws a black coloured rectangle if the cell on given position of
    # grid array is a wall, otherwise draws a white coloured rectangle
    for row in range(boardSize):
        for column in range(boardSize):
            # Color is white by default
            color = colorWhite

            # If the cell is a wall, color is grey
            if board.grid[row][column].status() == 'Wall':
                color = colorGrey

            # Color is red if the cell is start or end cell (top left and bottom right corners)
            if board.grid[row][column].status() == 'Start' or board.grid[row][column].status() == 'End':
                color = colorRed

            if board.grid[row][column].status() == 'Path':
                color = colorGreen

            # Draw
            pygame.draw.rect(screen,
                             color,
                             [(cellMargin + cellWidth) * column + cellMargin,
                              (cellMargin + cellHeight) * row + cellMargin,
                              cellWidth,
                              cellHeight])


# Start a board of size N
cellInfo = (cellWidth, cellHeight, cellMargin)
board = Board(boardSize, cellInfo)

# Initialize pygame
pygame.init()

# Set title of screen
pygame.display.set_caption("Shortest Path")
screen = pygame.display.set_mode(windowSize)

# Loop until the user clicks the close button.
running = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Set the screen background
screen.fill(colorBlack)
drawTheGrid()
pygame.display.flip()

# Initial setup of the game, random cells or draw using mouse or both.
while True:
    initEvent = pygame.event.wait()

    # If the user clicked on the close button
    if initEvent.type == pygame.QUIT:
        running = False
        break

    # If the user presses "Enter", "s", "e" or "r" keys
    if initEvent.type == pygame.KEYDOWN:
        # When "Enter" key is pressed, proceed with the solution
        if initEvent.key == pygame.K_RETURN:
            # Generate a matrix from current state of board
            maze = board.generate_matrix()

            # Determine start and end cells, if they are not specified use upper left and lower right corners
            try:
                start = (np.where(maze == 2)[0][0], np.where(maze == 2)[1][0]) # Checks whether a start cell exists
            except IndexError:
                start = (0, 0)

            try:
                end = (np.where(maze == 3)[0][0], np.where(maze == 3)[1][0]) # Checks whether an end cell exists
            except IndexError:
                end = (boardSize - 1, boardSize - 1)

            # Paint the start and end cells to red
            board.grid[start[0]][start[1]].set_start()
            board.grid[end[0]][end[1]].set_end()

            drawTheGrid()
            pygame.display.flip()

            # Set the values of the start and end cells to 0 on the matrix so that they are not seen as walls
            maze[start[0]][start[1]] = 0
            maze[end[0]][end[1]] = 0

            path = astar(maze, start, end)

            # Function returns tuple if path is found, otherwise returns None so check for that
            if type(path) != type(None):
                break

            if type(path) == type(None):
                print("No path found")
                continue

        # Press R to randomly generate cell status, no path is guaranteed to exist
        if initEvent.key == pygame.K_r:
            Cell.clear_all()
            Cell.randomGenerate()
            drawTheGrid()
            pygame.display.flip()

        # When pressed S, the cell that cursor is on will be start cell
        if initEvent.key == pygame.K_s:
            clickPosition = pygame.mouse.get_pos()
            whichCell = board.clickWhere(clickPosition)

            # Making sure the cursor is on a cell by checking its type since borders return None
            if isinstance(whichCell, tuple):
                Cell.clear_start()
                board.grid[whichCell[0]][whichCell[1]].set_start()
                drawTheGrid()
                pygame.display.flip()

        # When pressed E, the cell that cursor is on will be end cell
        if initEvent.key == pygame.K_e:
            clickPosition = pygame.mouse.get_pos()
            whichCell = board.clickWhere(clickPosition)

            if isinstance(whichCell, tuple):
                Cell.clear_end()
                board.grid[whichCell[0]][whichCell[1]].set_end()
                drawTheGrid()
                pygame.display.flip()

    # Click on cells to change their status from free to wall or vice versa
    if initEvent.type == pygame.MOUSEBUTTONDOWN:
        clickPosition = pygame.mouse.get_pos()
        whichCell = board.clickWhere(clickPosition)

        if isinstance(whichCell, tuple):
            if board.grid[whichCell[0]][whichCell[1]].status() == 'Wall':
                board.grid[whichCell[0]][whichCell[1]].set_free()
            else:
                board.grid[whichCell[0]][whichCell[1]].set_wall()
            drawTheGrid()
            pygame.display.flip()


runCount = 1
# -------- Main Program Loop ----------- Runs when pressed Enter
while running:

    # Paint the cells to green if they are included in the shortest path
    for i in path:
        if board.grid[i[0]][i[1]].status() != 'Start' and board.grid[i[0]][i[1]].status() != 'End':
            board.grid[i[0]][i[1]].set_path()

            drawTheGrid()
            clock.tick(clockSpeed)
            pygame.display.flip()


    # Main loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            running = False  # Flag that we are done so we exit this loop


# Quit the program
pygame.quit()
