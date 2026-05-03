import pygame
import random
import time

pygame.init()

ROWS = 6
COLS = 7
CELL_SIZE = 90
HEIGHT = (ROWS + 2) * CELL_SIZE

WIDTH = COLS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

clock = pygame.time.Clock()

BLUE = (30, 60, 200)
BLACK = (20, 20, 20)
RED = (220, 50, 50)
YELLOW = (240, 220, 0)
WHITE = (240, 240, 240)
GRAY = (80, 80, 80)
LIGHT_GRAY = (150, 150, 150)

font = pygame.font.SysFont(None, 32)
big = pygame.font.SysFont(None, 64)

class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, LIGHT_GRAY if hover else GRAY, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)

        label = font.render(self.text, True, WHITE)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class Board:
    def __init__(self):
        self.reset()
        self.win_cells = []

    def reset(self):
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.win_cells = []

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
        self.win_cells = []

        # horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r][c+i] == player for i in range(4)):
                    self.win_cells = [(r, c+i) for i in range(4)]
                    return True

        # vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.grid[r+i][c] == player for i in range(4)):
                    self.win_cells = [(r+i, c) for i in range(4)]
                    return True

        # diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.grid[r+i][c+i] == player for i in range(4)):
                    self.win_cells = [(r+i, c+i) for i in range(4)]
                    return True

        # diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r-i][c+i] == player for i in range(4)):
                    self.win_cells = [(r-i, c+i) for i in range(4)]
                    return True

        return False

    def draw(self):
        for r in range(ROWS):
            for c in range(COLS):
                x = c * CELL_SIZE
                y = r * CELL_SIZE + 100

                pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, BLACK, (x+45, y+45), 35)

                val = self.grid[r][c]
                if val == 1:
                    pygame.draw.circle(screen, RED, (x+45, y+45), 32)
                elif val == 2:
                    pygame.draw.circle(screen, YELLOW, (x+45, y+45), 32)

        for r, c in self.win_cells:
            x = c * CELL_SIZE + 45
            y = r * CELL_SIZE + 145
            pygame.draw.circle(screen, WHITE, (x, y), 40, 3)


class Game:
    def __init__(self):
        self.state = "menu"

        self.board = Board()
        self.turn = 1
        self.selected_col = 0

        self.mode = None
        self.vs_mode = None
        self.cpu_diff = None

        self.game_over = False
        self.winner = None

        self.cpu_timer = 0

    def reset(self):
        self.board.reset()
        self.turn = 1
        self.selected_col = 0
        self.game_over = False
        self.winner = None

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1

    def cpu_move(self):
        valid = [c for c in range(COLS) if not self.board.full(c)]

        if self.cpu_diff == "easy":
            return random.choice(valid)

        if self.cpu_diff == "intermediate":
            return random.choice(valid[:3])

        if self.cpu_diff == "advanced":
            return valid[3] if len(valid) > 3 else random.choice(valid)

    def move(self, col):
        if self.board.full(col) or self.game_over:
            return

        self.board.drop(col, self.turn)

        if self.board.check_win(self.turn):
            self.game_over = True
            self.winner = self.turn
            return

        if self.board.is_draw():
            self.game_over = True
            self.winner = "draw"

        self.switch_turn()
        self.cpu_timer = 0

    def update(self):
        if self.vs_mode == "cpu" and self.turn == 2 and not self.game_over:
            self.cpu_timer += 1
            if self.cpu_timer > 30:
                col = self.cpu_move()
                self.move(col)
                self.cpu_timer = 0

    def draw_game(self):
        screen.fill(BLACK)

        self.board.draw()

        x = self.selected_col * CELL_SIZE
        color = RED if self.turn == 1 else YELLOW

        pygame.draw.polygon(screen, color, [
            (x+45, 80),
            (x+20, 50),
            (x+70, 50)
        ])

        back = font.render("BACK", True, WHITE)
        screen.blit(back, (10, 10))

        clear = font.render("CLEAR", True, WHITE)
        screen.blit(clear, (WIDTH - 100, 10))

        if self.game_over:
            text = "DRAW" if self.winner == "draw" else f"PLAYER {self.winner} WINS"
            t = big.render(text, True, WHITE)
            screen.blit(t, t.get_rect(center=(WIDTH//2, 40)))

    def main():
        game = Game()

        play_btn = Button("PLAY", 250, 200, 200, 60)
        exit_btn = Button("EXIT", 250, 300, 200, 60)


        classic_btn = Button("CLASSIC", 250, 200, 200, 60)
        timed_btn = Button("TIMED", 250, 300, 200, 60)

        pvp_btn = Button("VS PLAYER", 250, 200, 200, 60)
        cpu_btn = Button("VS CPU", 250, 300, 200, 60)

        easy_btn = Button("EASY", 250, 200, 200, 60)
        med_btn = Button("INTERMEDIATE", 250, 300, 200, 60)
        hard_btn = Button("ADVANCED", 250, 400, 200, 60)

        running = True

        while running:
            clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False


    
        