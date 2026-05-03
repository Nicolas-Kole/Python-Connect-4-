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
        self.text = text

    def draw(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())

        pygame.draw.rect(
            screen,
            LIGHT_GRAY if hover else GRAY,
            self.rect,
            border_radius=8
        )

        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)

        t = font.render(self.text, True, WHITE)
        screen.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Board:
    def __init__(self):
        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.win_cells = []

    def reset(self):
        self.grid = [[0]*COLS for _ in range(ROWS)] 
    
    def drop(self, col, player):
        for r in reversed(range(ROWS)):
            if self.grid[r][col] == 0:
                self.grid[r][col] = player
                return 
    

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

    def draw(self, p1_col, p2_col):
        for r in range(ROWS):
            for c in range(COLS):
                x = c * CELL_SIZE
                y = r * CELL_SIZE + 100

                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, BLACK, (x+45, y+45), 35)

                if self.grid[r][c] == 1:
                    pygame.draw.circle(screen, p1_col, (x+45, y+45), 32)
                elif self.grid[r][c] == 2:
                    pygame.draw.circle(screen, p2_col, (x+45, y+45), 32)

            
class Game: 
    def __init__(self):
        self.state = "menu"

        self.board = Board() 
        self.turn = 1
        self.selected_col = 0

        self.mode = None
        self.vs_mode = None
        self.cpu_diff = None

        self.color_index = 0
        self.color_turn = 1   # 1 = Player 1, 2 = Player 2
        self.state = "menu"
        self.p1_color = None
        self.p2_color = None

        self.game_over = False
        self.winner = None
        
        self.cpu_timer = 0
        self.limit = 600
        self.menu_open = False

    def reset(self):
        self.board.reset()
        self.turn = 1
        self.selected_col = 0
        self.menu_open = False

    def cpu_move(self):
        valid = [c for c in range(COLS) if not self.board.full(c)]
        
        if self.cpu_diff == "easy":
            return random.choice(valid)

        if self.cpu_diff == "intermediate":
            return valid[0] 
        
        if self.cpu_diff == "advanced":
            return random.choice(valid[:2]) 

    def move(self, col):
        if self.board.full(col) or self.game_over:
            return

        row = self.board.drop(col, self.turn)

        if row is None:
            return
        
        if self.board.check_win(self.turn):
            self.game_over = True
            self.winner = self.turn
            return


        self.turn = 2 if self.turn == 1 else 1
        self.timer = 0

    def update(self):
        if self.vs_mode == "cpu" and self.turn == 2 and not self.game_over:
            self.timer += 1
            if self.timer > 40:
                self.move(self.cpu_move())

        if self.mode == "timed" and not self.game_over:
            self.timer += 1
            if self.timer > self.limit:
                self.move(self.selected_col)

    def  draw_color_select(self):
        screen.fill(BLACK) 
        title = big.render(f"Select Color - Player {self.color_turn}", True, WHITE)
        screen.blit(title, (120, 60))

        cols = 6
        size = 80
        start_x = 120
        start_y = 150

        for i, (name, col) in enumerate(COLORS):
            x = start_x + (i % cols) * (size + 10)
            y = start_y + (i // cols) * (size + 10)

            rect = pygame.Rect(x, y, size, size)

            selected = (i == self.color_index)

        pygame.draw.rect(
            screen,
            LIGHT_GRAY if selected else GRAY,
            rect,
            border_radius=8
        )
        
        if col:
            pygame.draw.circle(screen, col, rect.center, 22)
        else:
            pygame.draw.circle(screen, (200,200,200), rect.center, 22)

        label = font.render(name, True, WHITE)
        screen.blit(label, (x, y + 60))


    def draw_banner(self):
        if not self.game_over:
            return
        if self.winner == "draw":
            pygame.draw.rect(screen, self.p1_color, (0,0,WIDTH//2,80))
            pygame.draw.rect(screen, self.p2_color, (WIDTH//2,0,WIDTH//2,80))
            text = "DRAW"
        else:
            col = self.p1_color if self.winner == 1 else self.p2_color
            pygame.draw.rect(screen, col, (0,0,WIDTH,80))
            text = f"PLAYER {self.winner} WINS"

        t = big.render(text, True, WHITE)
        screen.blit(t, t.get_rect(center=(WIDTH//2,40)))

    def draw_pause(self):
        if not self.menu_open:
            return
        
        pygame.draw.rect(screen, BLACK, (150,150,400,300))
        pygame.draw.rect(screen, WHITE, (150,150,400,300),2)

        t = big.render("PAUSED", True, WHITE)
        screen.blit(t, (220,180))


    def update_cpu(self):
        if self.vs_mode == "cpu" and self.turn == 2 and not self.game_over:
            self.cpu_timer += 1

            if self.cpu_timer > 30:
                col = self.cpu_move()
                if col is not None:
                    self.move(col)
                self.cpu_timer = 0
                
 
    def draw_game(self):
        screen.fill(BLACK)

        x = self.selected_col * CELL_SIZE
        col_color = self.p1_color if self.turn == 1 else self.p2_color
        pygame.draw.rect(screen, WHITE, (x,100,CELL_SIZE,HEIGHT),2)

        self.board.draw()
        self.draw_banner()
        self.draw_pause()

        pygame.draw.polygon(screen, col_color, [
            (x+45,110),
            (x+20,80),
            (x+70,80)
        ])


def get_color(self, index):
    name, col = COLORS[index]

    if name == "Random":
        options = [c[1] for c in COLORS if c[1] and c[1] != self.p1_color]
        return random.choice(options)
    
    return col

def select_color(self):
    color = self.get_color(self.color_index)

    # Player 1 picks
    if self.color_turn == 1:
        self.p1_color = color
        self.color_turn = 2
        self.color_index = 0

    # Player 2 picks
    else:
        if color == self.p1_color:
            return  # prevent duplicate colors

        self.p2_color = color
        self.state = "game" 

def color(self):
    return self.p1 if self.turn==1 else self.p2

def move(self):
    if self.board.full(self.col): return
    self.board.drop(self.col,self.turn)

    if self.board.check(self.turn):
        self.over=True
        self.winner=self.turn
        return
    
    if all(self.board.full(c) for c in range(COLS)):
        self.over=True
        self.winner="draw"
        return
    
    self.turn=2 if self.turn==1 else 1
    self.timer=0

def update(self):
    if self.vs=="cpu" and self.turn==2 and not self.over:
        self.timer+=1
        if self.timer>40:
            self.col=self.cpu_move()
            self.move()
    
    if self.mode=="timed":
        self.timer+=1
        if self.timer>self.limit:
            self.move()


def main():
    game = Game()

    play = Button("Play", 250, 200, 200, 60)
    tutorial = Button("Tutorial", 250, 280, 200, 60)
    exit_btn = Button("Exit", 250, 360, 200, 60)

    running = True

    while running:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if game.state == "color_select":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        game.color_index = max(0, game.color_index - 1)
           
                    if e.key == pygame.K_RIGHT:
                        game.color_index = min(len(COLORS) - 1, game.color_index + 1)

                    if e.key == pygame.K_UP:
                        game.color_index = max(0, game.color_index - 6)

                    if e.key == pygame.K_DOWN:
                        game.color_index = min(len(COLORS) - 1, game.color_index + 6)

                    if e.key == pygame.K_RETURN:
                        game.select_color()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = e.pos

                    cols = 6
                    size = 80
                    start_x = 120
                    start_y = 150

                    for i in range(len(COLORS)):
                        x = start_x + (i % cols) * (size + 10)
                        y = start_y + (i // cols) * (size + 10)

                        rect = pygame.Rect(x, y, size, size)

                        if rect.collidepoint(mx, my):
                            game.color_index = i
                            game.select_color()

                if game.state == "menu":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if play.clicked(e.pos):
                            game.state = "game"
                        if tutorial.clicked(e.pos):
                            game.state = "tutorial"
                        if exit_btn.clicked(e.pos):
                            running = False
                if game.state == "game":
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_LEFT:
                            game.selected_col = max(0, game.selected_col - 1)
                        if e.key == pygame.K_RIGHT:
                            game.selected_col = min(COLS - 1, game.selected_col + 1)
                        if e.key == pygame.K_RETURN:
                             game.move(game.selected_col)         

        screen.fill(BLACK)

        if game.state == "menu":
            play.draw()
            tutorial.draw()
            exit_btn.draw()

        elif game.state == "game":
            game.update_cpu()
            game.draw_game()

        elif game.state == "tutorial":
            t = big.render("TUTORIAL PLACEHOLDER", True, WHITE)
            screen.blit(t, (100, 200))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()