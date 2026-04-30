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

    def check_win(self, player):
    
        # horizontal 
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r][c+i] == player for i in range(4)):
                    return True

        # vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.grid[r+i][c] == player for i in range(4)):
                    return True

        # diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.grid[r+i][c+i] == player for i in range(4)):
                    return True

        # diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r-i][c+i] == player for i in range(4)):
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

    def cpu_move(self):
        if self.cpu_difficulty == "easy":
            return random.randint(0, COLS - 1)

        elif self.cpu_difficulty == "medium":
            valid = [c for c in range(COLS) if not self.board.is_full(c)]
            return random.choice(valid)

        elif self.cpu_difficulty == "hard":
            for c in [3,2,4,1,5,0,6]:
                if not self.board.is_full(c):
                    return c
    
    def update(self):
        if self.mode == "cpu" and self.turn == 2 and not self.game_over:
            pygame.time.delay(300)
            col = self.cpu_move()
        if not self.board.is_full(col):
                self.board.drop_piece(col, 2)

                if self.board.check_win(2):
                    self.game_over = True

                self.switch_turn()

    def draw_ui(self, screen, font):
        color = RED if self.turn == 1 else YELLOW

        pygame.draw.polygon(screen, color, [
            (self.selected_col * CELL_SIZE + CELL_SIZE//2, 20),
            (self.selected_col * CELL_SIZE + 20, 60),
            (self.selected_col * CELL_SIZE + CELL_SIZE - 20, 60)
        ])

        if not self.game_over:
            text = f"Player {self.turn}'s Turn"
        else:
            text = f"Player {2 if self.turn == 1 else 1} Wins!"
        label = font.render(text, True, WHITE)
        screen.blit(label, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = Game()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    game.selected_col = max(0, game.selected_col - 1)

                if event.key == pygame.K_RIGHT:
                    game.selected_col = min(COLS - 1, game.selected_col + 1)

                if event.key == pygame.K_RETURN and not game.game_over:
                    col = game.selected_col

                    if not game.board.is_full(col):
                        game.board.drop_piece(col, game.turn)

                        if game.board.check_win(game.turn):
                            game.game_over = True

                        game.switch_turn()

                if event.key == pygame.K_r:
                    game = Game() 

                if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                    x = event.pos[0]
                    col = x // CELL_SIZE

                if not game.board.is_full(col):
                    game.board.drop_piece(col, game.turn)

                    if game.board.check_win(game.turn):
                        game.game_over = True
                    game.switch_turn()

                    

