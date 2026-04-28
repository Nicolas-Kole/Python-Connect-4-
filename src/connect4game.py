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

    
    
    def draw(self, screen, font):
        screen.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(screen, BLUE,
                                 (col * CELL_SIZE, row * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, BLACK,
                                   (col * CELL_SIZE + CELL_SIZE // 2,
                                    row * CELL_SIZE + CELL_SIZE // 2 + 100),
                                   CELL_SIZE // 2 - 5)

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == 1:
                    pygame.draw.circle(screen, RED,
                                       (col * CELL_SIZE + CELL_SIZE // 2,
                                        row * CELL_SIZE + CELL_SIZE // 2 + 100),
                                       CELL_SIZE // 2 - 5)
                elif self.grid[row][col] == 2:
                    pygame.draw.circle(screen, YELLOW,
                                       (col * CELL_SIZE + CELL_SIZE // 2,
                                        row * CELL_SIZE + CELL_SIZE // 2 + 100),
                                       CELL_SIZE // 2 - 5)

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 1  
        self.selected_col = 0
        self.game_over = False
        self.mode = "pvp" 
        self.cpu_difficulty = "easy"

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1 


