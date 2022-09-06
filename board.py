import numpy as np
from cell import Cell


class Board:
    # Initialize a N by N board
    def __init__(self, grid_size, cell_info):
        # Empty grid array
        self.gridSize = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype = bool)
        self.boardInfo = cell_info
        self.grid = [[Cell([row_cells, column_cells], self.boardInfo) for column_cells in range(self.gridSize)] for
                     row_cells in range(self.gridSize)]

    def clickWhere(self, click_pos):
        # Find the cell that contains the clicked position
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                x_hi = self.grid[i][j].screenPos[0][1]
                x_lo = self.grid[i][j].screenPos[0][0]
                y_lo = self.grid[i][j].screenPos[1][0]
                y_hi = self.grid[i][j].screenPos[1][1]

                if (click_pos[0] in range(x_lo, x_hi)) and (click_pos[1] in range(y_lo, y_hi)):
                    clicked_cell = (i, j)
                    return clicked_cell
        return None

    def generate_matrix(self):
        # Generate a status matrix from the board grid (1 for wall, 0 for free)
        matrix = np.zeros((self.gridSize, self.gridSize), dtype = int)
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.grid[i][j].status() == 'Wall':
                    matrix[i][j] = 1
                elif self.grid[i][j].status() == 'Start':
                    matrix[i][j] = 2
                elif self.grid[i][j].status() == 'End':
                    matrix[i][j] = 3
                else:
                    matrix[i][j] = 0
        return matrix
