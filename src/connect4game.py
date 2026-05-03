import pygame
import random
import time

pygame.init()

ROWS = 6
COLS = 7
CELL_SIZE = 90
HEIGHT = (ROWS + 2) * CELL_SIZE

WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 2) * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

clock = pygame.time.Clock()

WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
GRAY = (80, 80, 80)
LIGHT_GRAY = (160, 160, 160)

COLORS = [
    ("Red", (220, 50, 50)),
    ("Orange", (255, 140, 0)),
    ("Yellow", (240, 220, 0)),
    ("Green", (40, 200, 80)),
    ("Blue", (50, 120, 255)),
    ("Purple", (160, 60, 200)),
    ("Pink", (255, 105, 180)),
    ("Magenta", (255, 0, 255)),
    ("Dark Gray", (60, 60, 60)),
    ("Brown", (120, 70, 30)),
    ("Cyan", (0, 200, 200)),
    ("Random", None)
]

font = pygame.font.SysFont(None, 32)
big = pygame.font.SysFont(None, 60)

class Button: 
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        


class Board:
    def __init__(self):
        self.grid = [[0]*COLS for _ in range(ROWS)]

    def drop(self, col, player):
        for r in reversed(range(ROWS)):
            if self.grid[r][col] == 0:
                self.grid[r][col] = player
                return r
        return None

    def full(self, col):
        return self.grid[0][col] != 0

    def is_draw(self):
        return all(self.grid[0][c] != 0 for c in range(COLS))

    def check_win(self, player):
        
        # horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r][c + i] == player for i in range(4)):
                    return True
        
        # vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.grid[r + i][c] == player for i in range(4)):
                    return True
        
        # diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.grid[r + i][c + i] == player for i in range(4)):
                    return True
        
         # diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r - i][c + i] == player for i in range(4)):
                    return True

        return False

    def draw(self):
        for r in range(ROWS):
            for c in range(COLS):
                x = c*CELL_SIZE
                y = r*CELL_SIZE+100

                pygame.draw.rect(screen, WHITE, (x,y,CELL_SIZE,CELL_SIZE),2)
                pygame.draw.circle(screen, BLACK,(x+45,y+45),35)

                if self.grid[r][c]:
                    pygame.draw.circle(screen,(200,0,0) if self.grid[r][c]==1 else (240,220,0),
                        (x+45,y+45),32)
        
        for r,c in self.win_cells:
            pygame.draw.circle(screen, (255,255,255),
                (c*CELL_SIZE+45, r*CELL_SIZE+145), 10)