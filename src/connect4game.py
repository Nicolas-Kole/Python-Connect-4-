import pygame
import random 

ROWS = 6
COLS = 7
CELL_SIZE = 80

WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

class Board:
   
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def drop_piece(self, col, player):
        for row in reversed(range(ROWS)):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                return row
        return None

    def is_full(self, col):
        return self.grid[0][col] !=0

    def check_win(self,player):
        for r in range(ROWS):
            for c in range(COLS -3):
                   if all(self.grid[r][c+i] == player for i in range(4)):
                    return True

        for r in range(3, ROWS):
              for c in range(COLS - 3):
                if all(self.grid[r-i][c+i] == player for i in range(4)):
                    return True

        for r in range(3, ROWS):
              for c in range(COLS - 3):
                if all(self.grid[r-i][c+i] == player for i in range(4)):
                    return True

        for r in range(ROWS - 3):
              for c in range(COLS - 3):
                if all(self.grid[r+i][c+i] == player for i in range(4)):
                    return True
            
        return False

