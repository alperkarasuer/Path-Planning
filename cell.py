import random

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
