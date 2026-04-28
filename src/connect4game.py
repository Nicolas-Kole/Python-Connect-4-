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
  
