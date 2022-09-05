import pygame
import numpy as np
import random
from consts import *


def drawTheGrid():
    # Draws a black coloured rectangle if the cell on given position of
    # grid array is a wall, otherwise draws a white coloured rectangle
    for row in range(boardSize):
        for column in range(boardSize):
            # Color is white by default
            color = colorWhite

            # If the cell is a wall, color is grey
            if board.grid[row][column].is_wall():
                color = colorGrey

            # Color is red if the cell is start or end cell (top left and bottom right corners)
            if board.grid[row][column].status == 'Start' or board.grid[row][column].status == 'End':
                color = colorRed

            # Draw
            pygame.draw.rect(screen,
                             color,
                             [(cellMargin + cellWidth) * column + cellMargin,
                              (cellMargin + cellHeight) * row + cellMargin,
                              cellWidth,
                              cellHeight])


class Cell(object):
    cellObjs = []  # List of all cell objects created

    def __init__(self, cell_pos, game_info):
        """
        Cell has the ability to be wall or free cell, status can be
        checked with functions. Initial status is free.
        """
        Cell.cellObjs.append(self)
        self.width = game_info[0]
        self.height = game_info[1]
        self.margin = game_info[2]
        self.rowPos = cell_pos[0]
        self.colPos = cell_pos[1]
        self.status = 'Free'
        self.screenPos = [[(self.colPos + 1) * self.margin + self.colPos * self.width,
                           (self.colPos + 1) * self.margin + (self.colPos + 1) * self.width],
                          [(self.rowPos + 1) * self.margin + self.rowPos * self.height,
                           (self.rowPos + 1) * self.margin + (self.rowPos + 1) * self.height]]

    # Randomly generate walls
    @classmethod
    def randomGenerate(cls):
        for obj in cls.cellObjs:
            if random.uniform(0, 1) > 0.5:
                obj.set_wall()

    # Reset all cells to free
    @classmethod
    def clear_all(cls):
        for obj in cls.cellObjs:
            if obj.status != 'Start' and obj.status != 'End':
                obj.status = 'Free'

    # Called when setting a new start cell to ensure there is only a single start cell
    @classmethod
    def clear_start(cls):
        for obj in cls.cellObjs:
            if obj.status == 'Start':
                obj.status = 'Free'

    # Called when setting a new end cell to ensure there is only a single end cell
    @classmethod
    def clear_end(cls):
        for obj in cls.cellObjs:
            if obj.status == 'End':
                obj.status = 'Free'

    def set_wall(self):
        if self.status != 'Start' and self.status != 'End':
            self.status = 'Wall'

    def set_free(self):
        if self.status != 'Start' and self.status != 'End':
            self.status = 'Free'

    def set_start(self):
        self.status = 'Start'

    def set_end(self):
        self.status = 'End'

    def is_wall(self):
        return True if self.status == 'Wall' else False


class Board:
    # Initialize a N by N board
    def __init__(self, grid_size):
        # Empty grid array
        self.gridSize = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype = bool)
        self.boardInfo = (cellWidth, cellHeight, cellMargin)
        self.grid = [[Cell([row_cells, column_cells], self.boardInfo) for column_cells in range(self.gridSize)] for
                     row_cells in range(self.gridSize)]
        self._rows = grid_size
        self._columns = grid_size

    def clickWhere(self, click_pos):
        # Find the cell that contains the clicked position
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                x_hi = board.grid[i][j].screenPos[0][1]
                x_lo = board.grid[i][j].screenPos[0][0]
                y_lo = board.grid[i][j].screenPos[1][0]
                y_hi = board.grid[i][j].screenPos[1][1]

                if (click_pos[0] in range(x_lo, x_hi)) and (click_pos[1] in range(y_lo, y_hi)):
                    clicked_cell = (i, j)
                    return clicked_cell
        return None

    def generate_matrix(self):
        # Generate a matrix from the board grid
        matrix = np.zeros((self.gridSize, self.gridSize), dtype = int)
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if board.grid[i][j].is_wall():
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0
        return matrix



# Start a board of size N
board = Board(boardSize)

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
            if board.grid[whichCell[0]][whichCell[1]].is_wall():
                board.grid[whichCell[0]][whichCell[1]].set_free()
            else:
                board.grid[whichCell[0]][whichCell[1]].set_wall()
            drawTheGrid()
            pygame.display.flip()

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
