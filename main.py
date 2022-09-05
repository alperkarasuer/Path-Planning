import pygame
import numpy as np
import random
from consts import *

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

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
        self._status = 'Free'
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
            if obj._status != 'Start' and obj._status != 'End':
                obj._status = 'Free'

    # Called when setting a new start cell to ensure there is only a single start cell
    @classmethod
    def clear_start(cls):
        for obj in cls.cellObjs:
            if obj._status == 'Start':
                obj._status = 'Free'

    # Called when setting a new end cell to ensure there is only a single end cell
    @classmethod
    def clear_end(cls):
        for obj in cls.cellObjs:
            if obj._status == 'End':
                obj._status = 'Free'

    def set_wall(self):
        if self._status != 'Start' and self._status != 'End':
            self._status = 'Wall'

    def set_free(self):
        if self._status != 'Start' and self._status != 'End':
            self._status = 'Free'

    def set_start(self):
        self._status = 'Start'

    def set_end(self):
        self._status = 'End'

    def status(self):
        return self._status


class Board:
    # Initialize a N by N board
    def __init__(self, grid_size):
        # Empty grid array
        self.gridSize = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype = bool)
        self.boardInfo = (cellWidth, cellHeight, cellMargin)
        self.grid = [[Cell([row_cells, column_cells], self.boardInfo) for column_cells in range(self.gridSize)] for
                     row_cells in range(self.gridSize)]

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
        # Generate a status matrix from the board grid (1 for wall, 0 for free)
        matrix = np.zeros((self.gridSize, self.gridSize), dtype = int)
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if board.grid[i][j].status() == 'Wall':
                    matrix[i][j] = 1
                elif board.grid[i][j].status() == 'Start':
                    matrix[i][j] = 2
                elif board.grid[i][j].status() == 'End':
                    matrix[i][j] = 3
                else:
                    matrix[i][j] = 0
        return matrix

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


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
