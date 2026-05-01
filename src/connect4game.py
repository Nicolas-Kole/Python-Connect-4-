import pygame
import random
import time

pygame.init()

ROWS = 6
COLS = 7
CELL_SIZE = 80

WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 2) * CELL_SIZE

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
LIGHT_GRAY = (150, 150, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 3) 
        else:
            pygame.draw.rect(screen, GRAY, self.rect)
        
        label = font.render(self.text, True, WHITE)
        screen.blit(label, label.get_rect(center=self.rect.center))
        

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
        
        

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def drop_piece(self, col, player):
        for row in reversed(range(ROWS)):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                return True
        return False

    def is_full(self, col):
        return self.grid[0][col] != 0

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

    def draw(self, screen, selected_col):
        screen.fill(BLACK)

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (col * CELL_SIZE, row * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE)
                )

                pygame.draw.circle(
                    screen,
                    BLACK,
                    (col * CELL_SIZE + CELL_SIZE // 2,
                     row * CELL_SIZE + CELL_SIZE // 2 + 100),
                    CELL_SIZE // 2 - 5
                )

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == 1:
                    color = RED
                elif self.grid[row][col] == 2:
                    color = YELLOW
                else:
                    continue

                pygame.draw.circle(
                    screen,
                    color,
                    (col * CELL_SIZE + CELL_SIZE // 2,
                     row * CELL_SIZE + CELL_SIZE // 2 + 100),
                    CELL_SIZE // 2 - 5
                )

class Game:
    def __init__(self):
        self.state = "menu"
        self.reset()

        self.game_mode = None
        self.vs_mode = None
        self.cpu_difficulty = "easy"

        self.timer = 10
        self.last_time = time.time()

    def reset(self):
        self.board = Board()
        self.turn = 1
        self.selected_col = 0
        self.game_over = False

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1

    def cpu_move(self):
        valid = [c for c in range(COLS) if not self.board.is_full(c)]
        return random.choice(valid) if valid else None

    def update_timer(self):
        if self.game_mode == "timed" and not self.game_over:
            if time.time() - self.last_time >= 1:
                self.timer -= 1
                self.last_time = time.time()

            if self.timer <= 0:
                self.board.drop_piece(self.selected_col, self.turn)
                if self.board.check_win(self.turn):
                    self.game_over = True
                self.switch_turn()
                self.timer = 10

    def update(self):
        self.update_timer()

        if self.vs_mode == "cpu" and self.turn == 2 and not self.game_over:
            pygame.time.delay(250)

            col = self.cpu_move()
            if col is not None:
                self.board.drop_piece(col, 2)

                if self.board.check_win(2):
                    self.game_over = True

                self.switch_turn()
                self.timer = 10

    def draw_ui(self, screen):
        color = RED if self.turn == 1 else YELLOW

        pygame.draw.polygon(screen, color, [
            (self.selected_col * CELL_SIZE + CELL_SIZE // 2, 20),
            (self.selected_col * CELL_SIZE + 20, 60),
            (self.selected_col * CELL_SIZE + CELL_SIZE - 20, 60)
        ])

        if self.game_over:
            text = "Game Over"
        else:
            text = f"Player {self.turn}"

        label = font.render(text, True, WHITE)
        screen.blit(label, (10, 10))

        if self.game_mode == "timed":
            t = font.render(f"Time: {self.timer}", True, WHITE)
            screen.blit(t, (10, 50))

    def make_move(self):
        col = self.selected_col

        if not self.board.is_full(col):
            self.board.drop_piece(col, self.turn)

            if self.board.check_win(self.turn):
                self.game_over = True

            self.switch_turn()
            self.timer = 10

def main():
    game = Game()

    play_btn = Button("Play", 250, 200, 200, 50)
    classic_btn = Button("Classic", 250, 200, 200, 50)
    timed_btn = Button("Timed", 250, 280, 200, 50)
    pvp_btn = Button("PVP", 250, 200, 200, 50)
    cpu_btn = Button("CPU", 250, 280, 200, 50)

    easy_btn = Button("Easy", 250, 200, 200, 50)
    medium_btn = Button("Medium", 250, 270, 200, 50)
    hard_btn = Button("Hard", 250, 340, 200, 50)

    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_btn.clicked(event.pos):
                        game.state = "select_mode"

            elif game.state == "select_mode":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if classic_btn.clicked(event.pos):
                        game.game_mode = "classic"
                        game.state = "select_vs"

                    if timed_btn.clicked(event.pos):
                        game.game_mode = "timed"
                        game.state = "select_vs"

            elif game.state == "select_vs":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_btn.clicked(event.pos):
                        game.vs_mode = "pvp"
                        game.reset()
                        game.state = "game"

                    if cpu_btn.clicked(event.pos):
                        game.vs_mode = "cpu"
                        game.reset()
                        game.state = "game"

            elif game.state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.selected_col = max(0, game.selected_col - 1)

                    if event.key == pygame.K_RIGHT:
                        game.selected_col = min(COLS - 1, game.selected_col + 1)

                    if event.key == pygame.K_RETURN:
                        game.make_move()

       
        screen.fill(BLACK)

        if game.state == "menu":
            play_btn.draw(screen)

        elif game.state == "select_mode":
            classic_btn.draw(screen)
            timed_btn.draw(screen)

        elif game.state == "select_vs":
            pvp_btn.draw(screen)
            cpu_btn.draw(screen)

        elif game.state == "game":
            game.board.draw(screen, game.selected_col)
            game.draw_ui(screen)
            game.update()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()