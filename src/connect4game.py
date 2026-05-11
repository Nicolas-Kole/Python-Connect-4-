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
title_font = pygame.font.SysFont(None, 72)
menu_font = pygame.font.SysFont(None, 48)

class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, BLACK, self.rect, border_radius=8)
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
                return True
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

        self.turn_start_time = time.time()
        self.turn_limit = 5
        self.confetti = []

    def simulate_drop(self, grid, col, player): 
        temp = [row[:] for row in grid]

        for r in reversed(range(ROWS)):
            if temp[r][col] == 0:
                temp[r][col] = player
                break
        return temp
    
    def check_win_grid(self, grid, player):
        for r in range(ROWS):
           for c in range(COLS - 3):
               if all(grid[r][c+i] == player for i in range(4)):
                    return True
       
        for c in range(COLS):
           for r in range(ROWS -3):
               if all(grid[r+i][c] == player for i in range(4)):
                   return True
        
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(grid[r+i][c+i] == player for i in range(4)):
                    return True 
        
        for r in range(3, ROWS):
             for c in range(COLS - 3):
                if all(grid[r-i][c+i] == player for i in range(4)):
                    return True
        return False
               

    def reset(self):
        self.board.reset()
        self.turn = 1
        self.selected_col = 0
        self.game_over = False
        self.winner = None
        self.turn_start_time = time.time()

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1
        self.turn_start_time = time.time()


    def cpu_move(self):
        valid = [c for c in range(COLS) if not self.board.full(c)]

        if self.cpu_diff == "easy":
            return random.choice(valid)
        def simulate_drop(col, player):
            temp_grid = [row[:] for row in self.board.grid]
            for r in reversed(range(ROWS)):
                if temp_grid[r][col] == 0:
                    temp_grid[r][col] = player
                    break
            return temp_grid
        
                
        if self.cpu_diff == "intermediate":
            for col in valid:
                temp = simulate_drop(col, 2)
                if self.check_win_grid(temp, 2):
                    return col
            
            for col in valid:
                temp = simulate_drop(col, 1)
                if self.check_win_grid(temp, 1):
                    return col

            return random.choice(valid) 
                    

        if self.cpu_diff == "advanced":
            for col in valid:
                temp = simulate_drop(col, 2)

                if self.check_win_grid(temp, 2):
                    return col

            for col in valid:
                temp = self.simulate_drop(self.board.grid, col, 1)

                if self.check_win_grid(temp, 1):
                    return col     
            
            best_score = -999
            best_cols = []
            move_scores = []

            for col in valid:
                temp = self.simulate_drop(self.board.grid, col, 2)

                score = 0

                if col == 3:
                    score += 2
                elif col in [2,4]:
                    score += 1
                
                for r in range(ROWS):
                    if temp[r][col] == 2:
                        score += r
                
                for r in range(ROWS):
                    for c in range(COLS):
                        if temp[r][c] == 2:
                            if c < COLS - 1 and temp[r][c+1] == 2:
                                score += 3

                            if c < COLS - 2:
                                if temp[r][c + 1] == 2 and temp[r][c + 2] == 2:
                                    score += 8


                            if  r < ROWS - 1 and temp[r+1][c] == 2:
                                score += 3  

                            if r < ROWS - 2:
                                if temp[r + 1][c] == 2 and temp[r + 2][c] == 2:
                                    score += 8

                            if r < ROWS - 1 and c < COLS - 1:
                                if temp[r + 1][c + 1] == 2:
                                    score += 4  

                            if r > 0 and c < COLS - 1:
                                if temp[r - 1][c + 1] == 2:
                                    score += 4

                danger = 0

                for player_col in range(COLS):
                    if not self.board.full(player_col):
                        future = self.simulate_drop(temp, player_col, 1)
                        if self.check_win_grid(future, 1):
                            danger += 15
                score -= danger

                score += random.randint(0, 3)

                move_scores.append((score, col))

                if score > best_score:
                    best_score = score
                    best_cols = [col]
                
                elif score == best_score:
                    best_cols.append(col)
            
            
            move_scores.sort(key=lambda x: x[0], reverse=True)
            top_moves = move_scores[:3]
            
            best_score = move_scores[0][0]
            top_moves = []
            for score, col in move_scores:
                if score >= best_score - 3:
                    top_moves.append((score, col))
            
            return random.choice(top_moves)[1]

    def move(self, col):
        if self.board.full(col) or self.game_over:
            return
        

        self.board.drop(col, self.turn)

        if self.board.check_win(self.turn):
            self.game_over = True
            self.winner = self.turn
            self.create_confetti()
            return

        if self.board.is_draw():
            self.game_over = True
            self.winner = "draw"

        self.switch_turn()

    def create_confetti(self):
         self.confetti = []
         if self.winner == 1:
            color = RED
         elif self.winner == 2:
             color = YELLOW
         else:
            return
         
         for _ in range(120):
             
             piece = {
                 "x": random.randint(0, WIDTH),
                 "y": random.randint(-HEIGHT, 0),
                 "w": random.randint(6, 14),
                 "h": random.randint(10, 18),
                 "speed": random.uniform(2, 6),
                 "drift": random.uniform(-2, 2),
                 "rotation": random.randint(0, 360),
                 "color": color

             }
             self.confetti.append(piece)


          



        self.cpu_timer = 0


    def update(self):
        if self.vs_mode == "cpu" and self.turn == 2 and not self.game_over:
            self.cpu_timer += 1
            if self.cpu_timer > 30:
                col = self.cpu_move()
                self.move(col)
                self.cpu_timer = 0
        if self.mode == "timed" and not self.game_over:
            elapsed = time.time() - self.turn_start_time

            if elapsed >= self.turn_limit:
                valid_cols = [c for c in range(COLS) if not self.board.full(c)]

                if not valid_cols:
                    return

                if not self.board.full(self.selected_col):
                    self.move(self.selected_col)
                else:
                    valid_cols = [c for c in range(COLS) if not self.board.full(c)]

                    if valid_cols:
                        fallback_col = random.choice(valid_cols)
                        self.selected_col = fallback_col
                        self.move(fallback_col)


    def draw_game(self):
        screen.fill(BLACK)

        self.board.draw()

        x = self.selected_col * CELL_SIZE
        color = RED if self.turn == 1 else YELLOW
        pygame.draw.polygon(screen, color, [(x+45, 80), (x+20, 50), (x+70, 50)])

        self.back_rect = pygame.Rect(10, 10, 80, 30)
        pygame.draw.rect(screen, GRAY, self.back_rect, border_radius=6)
        screen.blit(font.render("BACK", True, WHITE), (15, 12))


        if  self.mode == "timed" and not self.game_over:
            remaining = max(0, int(self.turn_limit - (time.time() - self.turn_start_time)))
            timer_text = font.render(f"Time: {remaining}", True, WHITE)
            screen.blit(timer_text, (WIDTH//2 - 50, 20))


        if self.game_over:
            if self.winner == "draw":
                text = "DRAW"
                color = WHITE

            elif self.winner == 1:
                color = RED
                text = "PLAYER 1 WINS"
            elif self.winner == 2:
                if self.vs_mode == "cpu":
                    text = "CPU WINS"
                else:
                    text = "PLAYER 2 WINS"
                color = YELLOW
           
            t = big.render(text, True, color)
            screen.blit(t, t.get_rect(center=(WIDTH//2, 40)))

        return self.back_rect

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

    back_btn = Button("BACK", 10, 10, 100, 40)

    running = True

    while running:
        clock.tick(60)

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                if game.state == "menu":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if play_btn.clicked(e.pos):
                            game.state = "mode"
                        if exit_btn.clicked(e.pos):
                            running = False
                
                elif game.state == "mode":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                       if classic_btn.clicked(e.pos):
                           game.mode = "classic"
                           game.state = "vs"
                       elif timed_btn.clicked(e.pos):
                           game.mode = "timed"
                           game.state = "vs"
                       elif back_btn.clicked(e.pos):
                           game.state = "menu"
                           

                elif game.state == "vs":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if pvp_btn.clicked(e.pos):
                            game.vs_mode = "pvp"
                            game.reset()
                            game.state = "game"
                        elif cpu_btn.clicked(e.pos):
                            game.vs_mode = "cpu"
                            game.state = "cpu"
                        elif back_btn.clicked(e.pos):
                            game.state = "mode"

                elif game.state == "cpu":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        
                        if easy_btn.clicked(e.pos):
                            game.cpu_diff = "easy"
                            game.reset()
                            game.vs_mode = "cpu"
                            game.state = "game"
                        
                        elif med_btn.clicked(e.pos):
                            game.cpu_diff = "intermediate"
                            game.reset()
                            game.vs_mode = "cpu"
                            game.state = "game"
                        
                        elif hard_btn.clicked(e.pos):
                            game.cpu_diff = "advanced"
                            game.reset()
                            game.vs_mode = "cpu"
                            game.state = "game"
                        
                        elif back_btn.clicked(e.pos): 
                            game.state = "vs"
                    
                elif game.state == "game":
                        if e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_LEFT:
                                game.selected_col = max(0, game.selected_col - 1)
                            elif e.key == pygame.K_RIGHT:
                                game.selected_col = min(COLS - 1, game.selected_col + 1)
                            elif e.key == pygame.K_RETURN:
                                game.move(game.selected_col) 

                        if e.type == pygame.MOUSEBUTTONDOWN:
                            if game.back_rect.collidepoint(e.pos):
                                game.state = "menu"
                            else:
                                col = e.pos[0] // CELL_SIZE
                                if 0 <= col < COLS:
                                    game.move(col)

                            if game.back_rect.collidepoint(e.pos):
                                game.state = "menu"
                            
                    
        screen.fill(BLACK)

        if game.state == "menu":
            play_btn.draw()
            exit_btn.draw()

        elif game.state == "mode":
            back_btn.draw()
            classic_btn.draw()
            timed_btn.draw()

        elif game.state == "vs":
            back_btn.draw()
            pvp_btn.draw()
            cpu_btn.draw()

        elif game.state == "cpu":
            back_btn.draw()
            easy_btn.draw()
            med_btn.draw()
            hard_btn.draw()

        elif game.state == "game":
            game.update()
            game.draw_game()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
     main()

