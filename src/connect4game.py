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

        color = LIGHT_GRAY if self.rect.collidepoint(mouse) else GRAY
        pygame.draw.rect(screen, color, self.rect)

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
                return row
        return None

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

        pygame.draw.rect(
            screen,
            WHITE,
            (
                selected_col * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
                ROWS * CELL_SIZE
            ),
            3
        )

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
                    (
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2 + 100
                    ),
                    CELL_SIZE // 2 - 5
                )

    
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == 1:
                    pygame.draw.circle(
                        screen,
                        RED,
                        (
                            col * CELL_SIZE + CELL_SIZE // 2,
                            row * CELL_SIZE + CELL_SIZE // 2 + 100
                        ),
                        CELL_SIZE // 2 - 5
                    )
                elif self.grid[row][col] == 2:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (
                            col * CELL_SIZE + CELL_SIZE // 2,
                            row * CELL_SIZE + CELL_SIZE // 2 + 100
                        ),
                        CELL_SIZE // 2 - 5
                    )


class Game:
    def __init__(self):
        self.reset()
        self.state = "menu"

        self.game_mode = None # classic / timed
        self.vs_mode = None   # pvp / cpu
        self.cpu_difficulty = None
        
        self.timer = 10
        self.last_time = time.time()

    def reset(self):
        self.board = Board()
        self.turn = 1
        self.selected_col = 0
        self.game_over = False


        self.falling = None
        
    
    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1
    
    def start_drop(self, col):
        if self.board.is_full(col) or self.game_over:
            return
        
        self.board.drop_piece(col, self.turn)

        if self.board.check_win(self.turn):
            self.game_over = True  

        self.switch_turn()

    def cpu_move(self):
        valid = [c for c in range(COLS) if not self.board.is_full(c)]

        for c in valid:
            temp = [row[:] for row in self.board.grid]
            for r in reversed(range(ROWS)):
                if temp[r][c] == 0:
                    temp[r][c] = 2
                    break
            temp_board = Board()
            temp_board.grid = temp
            if temp_board.check_win(2):
                return c
       
        for c in valid:
            temp = [row[:] for row in self.board.grid]

            for r in reversed(range(ROWS)):
                if temp[r][c] == 0:
                    temp[r][c] = 1
                    break

            if self.board.check_win(1):
                return c
            
    def update_timer(self):
        if self.mode == "timed" and not self.game_over:
            if time.time() - self.last_time >= 1:
                self.timer -= 1
                self.last_time = time.time()

            if self.timer <= 0:
                self.start_drop(self.selected_col)
                self.timer = 10
    
    def make_move(self, col):
        if self.board.is_full(col):
            return

        color = RED  if self.turn == 1 else YELLOW

        pygame.draw.polygon(screen, color, [
            (self.selected_col * CELL_SIZE + CELL_SIZE // 2, 20),
            (self.selected_col * CELL_SIZE + 20, 60),
            (self.selected_col * CELL_SIZE + CELL_SIZE - 20, 60)           
        ])

        text = f"Player {self.turn}" if not self.game_over else "Game Over"
        label = font.render(text, True, WHITE)
        screen.blit(label, label.get_rect(center=(WIDTH//2, 60))) 

        if self.game_mode == "timed":
            t = font.render(f"Time: {self.timer}", True, WHITE)
            screen.blit(t, (10, 10))

    
        if self.cpu_difficulty == "easy":
            return random.randint(0, COLS - 1)

        elif self.cpu_difficulty == "medium":
            valid = [c for c in range(COLS) if not self.board.is_full(c)]
            return random.choice(valid)

        elif self.cpu_difficulty == "hard":
            for c in [3, 2, 4, 1, 5, 0, 6]:
                if not self.board.is_full(c):
                    return c
        return 0

    def update(self):
        self.update_timer()
        if self.vs_mode == "cpu" and self.turn == 2 and not self.game_over:
            pygame.time.delay(300)

            col = self.cpu_move()

            if not self.board.is_full(col):
                self.board.drop_piece(col, 2)

                if self.board.check_win(2):
                    self.game_over = True

                self.switch_turn()
                self.timer = 10
    
   
        valid = [c for c in range(COLS) if not self.board.is_full(c)]
        return random.choice(valid)
    
    def draw_ui(self, screen, font):
        color = RED if self.turn == 1 else YELLOW

        pygame.draw.polygon(screen, color, [
            (self.selected_col * CELL_SIZE + CELL_SIZE // 2, 20),
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = Game()

    play_btn = Button("Play", 250, 200, 200, 50)
    tutorial_btn = Button("Tutorial", 250, 270, 200, 50)
    exit_btn = Button("Exit", 250, 340, 200, 50)

    classic_btn = Button("Classic Mode", 250, 200, 200, 50)
    timed_btn = Button("Timed Mode", 250, 280, 200, 50)

    pvp_btn = Button("Player vs Player", 250, 200, 200, 50)
    cpu_btn = Button("Player vs CPU", 250, 280, 200, 50)

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
                        game.state + "select_vs"
            
            elif game.state == "select_vs":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pvp_btn.clicked(event.pos):
                        game.vs_mode = "pvp"
                        game.reset()
                        game.state = "game"
                    if cpu_btn.clicked(event.pos):
                       game.vs_mode = "cpu"
                       game.state = "select_cpu"

            elif game.state == "game":
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LEFT:
                         game.selected_col = max(0, game.selected_col - 1)
                     if event.key == pygame.K_RIGHT:
                         game.selected_col = min(COLS - 1, game.selected_col + 1)
                     if event.key == pygame.K_RETURN:
                         game.make_move(game.selected_col)
                               

            if game.state == "menu":
                screen.fill(BLACK)
                play_btn.draw(screen)
                tutorial_btn.draw(screen)
                exit_btn.draw(screen)

            elif game.state == "select_mode":
                screen.fill(BLACK)
                classic_btn.draw(screen)
                timed_btn.draw(screen)

            elif game.state == "select_vs":
                screen.fill(BLACK)
                pvp_btn.draw(screen)
                cpu_btn.draw(screen)

            elif game.state == "select_mode":
                screen.fill(BLACK)
                easy_btn.draw(screen)
                medium_btn.draw(screen)
                hard_btn.draw(screen)

                
            if game.falling:
                c = game.falling["col"]
                y = game.falling["y"]
                color = RED if game.falling["player"] == 1 else YELLOW
                pygame.draw.circle(
                    screen,
                    color,
                    (c * CELL_SIZE + CELL_SIZE // 2, y),
                    CELL_SIZE // 2 - 5
                )
                   

                if event.key == pygame.K_LEFT:
                    game.selected_col = max(0, game.selected_col - 1)

                elif event.key == pygame.K_RIGHT:
                    game.selected_col = min(COLS - 1, game.selected_col + 1)

                elif event.key == pygame.K_RETURN and not game.game_over:
                    col = game.selected_col

                    if not game.board.is_full(col):
                        game.board.drop_piece(col, game.turn)

                        if game.board.check_win(game.turn):
                            game.game_over = True

                        game.switch_turn()

                elif event.key == pygame.K_r:
                    game = Game()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                col = event.pos[0] // CELL_SIZE

                if not game.board.is_full(col):
                    game.board.drop_piece(col, game.turn)

                    if game.board.check_win(game.turn):
                        game.game_over = True

                    game.switch_turn()

        game.update()

        game.draw_ui(screen, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()