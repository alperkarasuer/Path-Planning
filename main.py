import pygame
from consts import *
from board import Board, Cell, np
from astar import astar, Node


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

    if initEvent.type == pygame.QUIT:
        running = False
        break

    if initEvent.type == pygame.KEYDOWN:
        if initEvent.key == pygame.K_RETURN:
            break

        # Press R to randomly generate cell status
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


# Generate a matrix from current state of board
maze = board.generate_matrix()

# Determine start and end cells
start = (np.where(maze == 2)[0][0], np.where(maze == 2)[1][0])
end = (np.where(maze == 3)[0][0], np.where(maze == 3)[1][0])

# Set the values of the start and end cells to 0 so that they are not seen as walls
maze[start[0]][start[1]] = 0
maze[end[0]][end[1]] = 0


path = astar(maze, start, end)
print(path)



# -------- Main Program Loop ----------- Runs when pressed Enter
while running:

    # Draw the grid
    drawTheGrid()

    # Limit frames per second
    clock.tick(clockSpeed)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Main loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            running = False  # Flag that we are done so we exit this loop

# Quit the program
pygame.quit()
