import pygame
import sys
import os
import random
pygame.init()
LOGICAL_WIDTH, LOGICAL_HEIGHT = (pygame.display.Info().current_w//2, pygame.display.Info().current_h//1.2)
FPS = 60

# --- Colors ---
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_MENU_BG = (6, 0, 10)
COLOR_BUTTON = (38, 19, 86)
COLOR_BUTTON_HOVER = (20, 162, 210)
COLOR_BUTTON_CLICK = (56, 28, 128)
COLOR_BUTTON_TEXT = (126, 90, 219)
COLOR_INSTRUCTIONS = (230, 230, 230)
COLOR_TITLE = (255, 255, 255)
COLOR_DISABLED = (100, 100, 100)
COLOR_BACK_BUTTON = (38, 19, 86)
COLOR_BACK_BUTTON_HOVER = (20, 162, 210)

class FallingBall:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, int(screen_width))
        self.y = random.randint(-int(screen_height), 0)
        self.radius = random.randint(5, 15)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        self.speed = random.uniform(1, 3)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self, screen_height):
        return self.y - self.radius > screen_height

# --- Asset Paths ---
if True:
    ASSET_DIR = os.path.dirname(__file__)

OPENING_BACKGROUND_IMG = os.path.join(ASSET_DIR, 'tictactoe logo [Recovered].jpg')
OPENING_MUSIC = os.path.join(ASSET_DIR, 'tictactoe1.1_2.mp3')
CLICK_SOUND = os.path.join(ASSET_DIR, 'beep-6-96243.mp3')
GAME_MUSIC = os.path.join(ASSET_DIR, 'game start.wav')
CIRCLE_IMG = os.path.join(ASSET_DIR, 'circle tictactoe.png')
CROSS_IMG = os.path.join(ASSET_DIR, 'cross tictactoe.png')
WIN_MUSIC = os.path.join(ASSET_DIR, 'win aud.wav')
LOSE_MUSIC = os.path.join(ASSET_DIR, 'loss aud.wav')
icon = pygame.image.load('tictactoe_logo_Recovered_1.png')
pygame.display.set_icon(icon)

BASE_FONT_SIZE_LARGE = int(LOGICAL_HEIGHT * 0.04)
BASE_FONT_SIZE_MEDIUM = int(LOGICAL_HEIGHT * 0.05)
BASE_FONT_SIZE_SMALL = int(LOGICAL_HEIGHT * 0.03)

def get_font(size):
    size = int(max(1, size))
    font_paths = {'persuasi.ttf'}
    for font_name in font_paths:
            full_path = os.path.join(ASSET_DIR, font_name)
            return pygame.font.Font(full_path, size)
# --- Helper Functions ---
def draw_text(screen, text, font, color, center_pos):
    if True:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)
        return text_rect

def draw_curved_rect_button(screen, default_color, hover_color, click_color, rect, border_radius, text, text_color, font, mouse_pos, is_mouse_down):
    current_color = default_color
    on_button = rect.collidepoint(mouse_pos)

    if on_button:
        current_color = hover_color
        if is_mouse_down:
            current_color = click_color

    if True:
        pygame.draw.rect(screen, current_color, rect, border_radius=int(border_radius))
        draw_text(screen, text, font, text_color, rect.center)
    return rect, on_button
# CLass er start
class TicTacToe:
    def __init__(self, screen_surface):
        self.screen = screen_surface
        self.screen_width = LOGICAL_WIDTH
        self.screen_height = LOGICAL_HEIGHT
        self.table_size = int(self.screen_height * 0.8)
        self.table_size = max(300, self.table_size)
        self.cell_size = self.table_size // 3
        self.table_space = max(2, int(self.cell_size * 0.05))
        self.line_width = max(2, int(self.cell_size * 0.03))
        self.strike_width = max(3, int(self.line_width * 1.2)) # Keep for potential future use
        self.board_offset_x = (self.screen_width - self.table_size) // 2
        self.board_offset_y = (self.screen_height - self.table_size) // 2
        self.table = [["-" for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.winner = None
        self.win_details = None # To store winning line info if needed later
        self.taking_move = True
        self.game_running = True
        self.game_over_state = False
        self.score_x = 0
        self.score_o = 0
        self.reset_score_rect = None
        self.back_button_rect = None
        self.background_color = COLOR_BLACK
        self.table_bg_color = (26, 0, 10)
        self.table_line_color = (166, 123, 147)
        self.instructions_color = (255, 255, 255)
        self.game_over_bg_color = (0, 0, 0, 180)
        self.game_over_text_color = (255, 179, 1)
        self.x_color = (230, 50, 50)
        self.o_color = (50, 100, 230)
        self.win_strike_color = (255, 223, 0) # Color definition kept
        self.font_large = get_font(BASE_FONT_SIZE_LARGE)
        self.font_small = get_font(BASE_FONT_SIZE_MEDIUM)
        self.font_score = get_font(BASE_FONT_SIZE_SMALL)
        self.font_back_button = get_font(BASE_FONT_SIZE_SMALL * 0.9)
        self.FPS_CLOCK = pygame.time.Clock()
        self.use_images = False
        self.img_o = None; self.img_x = None
        self.x_render = None; self.o_render = None
        if True:
            img_o_orig = pygame.image.load(CIRCLE_IMG).convert_alpha()
            img_x_orig = pygame.image.load(CROSS_IMG).convert_alpha()
            img_size = (int(self.cell_size * 0.8), int(self.cell_size * 0.8))
            self.img_o = pygame.transform.smoothscale(img_o_orig, img_size)
            self.img_x = pygame.transform.smoothscale(img_x_orig, img_size)
            self.use_images = True

        self.play_again_rect = None
        self.menu_rect = None
        self.draw_table()

    def reset_game(self):
        self.table = [["-" for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.winner = None
        self.win_details = None
        self.taking_move = True
        self.game_over_state = False
        self.play_again_rect = None
        self.menu_rect = None
        self.back_button_rect = None
        if hasattr(self , "_win_music_played"):
            del self._win_music_played

    def draw_table(self):
        self.screen.fill(self.background_color)
        board_rect = pygame.Rect(self.board_offset_x, self.board_offset_y, self.table_size, self.table_size)
        pygame.draw.rect(self.screen, self.table_bg_color, board_rect)
        for i in range(1, 3):
            start_pos_v = (self.board_offset_x + self.cell_size * i, self.board_offset_y + self.table_space)
            end_pos_v = (self.board_offset_x + self.cell_size * i, self.board_offset_y + self.table_size - self.table_space)
            pygame.draw.line(self.screen, self.table_line_color, start_pos_v, end_pos_v, self.line_width)
            start_pos_h = (self.board_offset_x + self.table_space, self.board_offset_y + self.cell_size * i)
            end_pos_h = (self.board_offset_x + self.table_size - self.table_space, self.board_offset_y + self.cell_size * i)
            pygame.draw.line(self.screen, self.table_line_color, start_pos_h, end_pos_h, self.line_width)
        for y, row in enumerate(self.table):
            for x, cell in enumerate(row):
                if cell != "-": self._draw_char(x, y, cell)

    def _change_player(self):
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"
#bohut line ekshathe ehene
    def _get_valid_moves(self):
       return [(r, c) for r, row in enumerate(self.table) for c, cell in enumerate(row) if cell == "-"]
    def _ai_move(self):
        pygame.time.wait(600)

        def is_winner_sim(board , player):
            # Check rows
            for row in board:
                if all(cell == player for cell in row):
                    return True
            # Check columns
            for c in range(3):
                if all(row[c] == player for row in board):
                    return True
            # Check diagonals
            if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
                return True
            return False

        def simulate_move(r , c , player):
            temp_board = [row.copy() for row in self.table]
            temp_board[r][c] = player
            return is_winner_sim(temp_board , player)

        valid_moves = self._get_valid_moves()
        best_move = None

        # 1. Win if possible
        for r , c in valid_moves:
            if simulate_move(r , c , "O"):
                best_move = (r , c)
                break

        # 2. Block opponent
        if not best_move:
            for r , c in valid_moves:
                if simulate_move(r , c , "X"):
                    best_move = (r , c)
                    break

        # 3. Take center
        if not best_move and self.table[1][1] == "-":
            best_move = (1 , 1)

        # 4. Take a corner
        if not best_move:
            for r , c in [(0 , 0) , (0 , 2) , (2 , 0) , (2 , 2)]:
                if self.table[r][c] == "-":
                    best_move = (r , c)
                    break

        # 5. Take any side
        if not best_move:
            for r , c in [(0 , 1) , (1 , 0) , (1 , 2) , (2 , 1)]:
                if self.table[r][c] == "-":
                    best_move = (r , c)
                    break

        # Fallback random (shouldn’t happen)
        if not best_move and valid_moves:
            best_move = random.choice(valid_moves)

        # Make the move
        if best_move:
            row , col = best_move
            click_x = self.board_offset_x + col * self.cell_size + self.cell_size // 2
            click_y = self.board_offset_y + row * self.cell_size + self.cell_size // 2
            self._move((click_x , click_y) , is_ai=True)

        # 3. Take center
        if self.table[1][1] == ' ':
            return (1 , 1)

        # 4. Take a corner
        for r , c in [(0 , 0) , (0 , 2) , (2 , 0) , (2 , 2)]:
            if self.table[r][c] == ' ':
                return (r , c)

        # 5. Take any side
        for r , c in [(0 , 1) , (1 , 0) , (1 , 2) , (2 , 1)]:
            if self.table[r][c] == ' ':
                return (r , c)

        # fallback - no move found
        return None

    def _move(self, pos, is_ai=False):
        relative_x = pos[0] - self.board_offset_x
        relative_y = pos[1] - self.board_offset_y
        if not (0 <= relative_x < self.table_size and 0 <= relative_y < self.table_size):
             if not is_ai: print("Click outside table bounds")
             return
        if True:
            col = int(relative_x // self.cell_size); row = int(relative_y // self.cell_size)
            col = max(0, min(col, 2)); row = max(0, min(row, 2))
            if self.table[row][col] == "-":
                self.table[row][col] = self.player
                self._draw_char(col, row, self.player)
                self._game_check()
                if self.taking_move: self._change_player()
                else: self.game_over_state = True; print(f"Game Over! Winner: {self.winner}")
            else:
                if not is_ai: print("Cell already taken")

    def _draw_char(self, x, y, player):
        cell_top_left_x = self.board_offset_x + x * self.cell_size
        cell_top_left_y = self.board_offset_y + y * self.cell_size
        cell_rect = pygame.Rect(cell_top_left_x, cell_top_left_y, self.cell_size, self.cell_size)
        if self.use_images and self.img_o and self.img_x:
            img = self.img_o if player == "O" else self.img_x
            img_rect = img.get_rect(center=cell_rect.center)
            self.screen.blit(img, img_rect)
        elif self.x_render and self.o_render:
            text_render = self.o_render if player == "O" else self.x_render
            text_rect = text_render.get_rect(center=cell_rect.center)
            self.screen.blit(text_render, text_rect)
        else:
             print(f"Error: Cannot draw player {player} at ({x},{y})")
             pygame.draw.rect(self.screen, (255, 0, 0), cell_rect, 2)

    def _message(self):
        if self.taking_move and not self.game_over_state and self.font_large:
            text = f"Player {self.player}'s Turn"; color = self.instructions_color
            msg_center_x = self.board_offset_x + self.table_size // 2
            msg_center_y = self.board_offset_y - self.font_large.get_height() // 2 - 10
            msg_center_y = max(self.font_large.get_height() // 2 + 5, msg_center_y)
            if True:
                msg_surface = self.font_large.render(text, True, color)
                msg_rect = msg_surface.get_rect(center=(msg_center_x, msg_center_y))
                bg_rect = msg_rect.inflate(10, 6)
                s = pygame.Surface(bg_rect.size, pygame.SRCALPHA); s.fill((0, 0, 0, 150))
                self.screen.blit(s, bg_rect.topleft)
                self.screen.blit(msg_surface, msg_rect.topleft)

    def _game_check(self):
        # Rows
        for r_idx, row in enumerate(self.table):
            if all(cell == self.player for cell in row):
                self.winner = self.player; self.taking_move = False
                self.win_details = (((0, r_idx), (2, r_idx), "hor"))
                return
        # Columns
        for c_idx in range(3):
            col = [self.table[r][c_idx] for r in range(3)]
            if all(cell == self.player for cell in col):
                self.winner = self.player; self.taking_move = False
                self.win_details = (((c_idx, 0), (c_idx, 2), "ver"))
                return
        # Diagonals
        diag1 = [self.table[i][i] for i in range(3)]
        if all(cell == self.player for cell in diag1):
            self.winner = self.player; self.taking_move = False
            self.win_details = (((0, 0), (2, 2), "left-diag"))
            return
        diag2 = [self.table[i][2 - i] for i in range(3)]
        if all(cell == self.player for cell in diag2):
            self.winner = self.player; self.taking_move = False
            self.win_details = (((2, 0), (0, 2), "right-diag"))
            return
        # Draw
        if self.winner is None and all(cell != "-" for row in self.table for cell in row):
            self.taking_move = False; self.winner = "draw"; self.win_details = None

    def _draw_score(self):
        if not self.font_score: return
        score_text = f"Score: X - {self.score_x} | O - {self.score_o}"
        text_color = self.instructions_color
        score_center_x = self.screen_width // 1.8
        score_top_y = self.board_offset_y + self.table_size + int(self.screen_height * 0.02)
        if True:
            score_text_surface = self.font_score.render(score_text, True, text_color)
            score_text_rect = score_text_surface.get_rect(center=(score_center_x, score_top_y + score_text_surface.get_height() // 2))
            score_bg_rect = score_text_rect.inflate(8, 4)
            s = pygame.Surface(score_bg_rect.size, pygame.SRCALPHA); s.fill((0, 0, 0, 150))
            self.screen.blit(s, score_bg_rect.topleft)
            self.screen.blit(score_text_surface, score_text_rect.topleft)
            reset_button_width = self.font_score.size("Reset ")[0]
            reset_button_height = int(score_text_rect.height * 1.2)
            reset_border_radius = int(reset_button_height * 0.6)
            reset_rect_pos_x = score_text_rect.right + 15
            reset_rect_center_y = score_text_rect.centery
            self.reset_score_rect = pygame.Rect(0, 0, reset_button_width, reset_button_height)
            self.reset_score_rect.midleft = (reset_rect_pos_x, reset_rect_center_y)
            mouse_pos = pygame.mouse.get_pos(); left_mouse_down = pygame.mouse.get_pressed()[0]
            draw_curved_rect_button(self.screen, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_CLICK,
                self.reset_score_rect, reset_border_radius, "Reset", COLOR_BUTTON_TEXT, self.font_score,
                mouse_pos, left_mouse_down)


    def _draw_back_button(self):
        if not self.font_back_button: return
        button_text = "<- Menu"; margin = int(LOGICAL_WIDTH * 0.02)
        text_width, text_height = self.font_back_button.size(button_text)
        button_height = int(text_height * 1.8); button_width = int(text_width * 1.4)
        border_radius = int(button_height * 0.8)
        self.back_button_rect = pygame.Rect(margin, margin, button_width, button_height)
        mouse_pos = pygame.mouse.get_pos(); left_mouse_down = pygame.mouse.get_pressed()[0]
        draw_curved_rect_button(self.screen, COLOR_BACK_BUTTON, COLOR_BACK_BUTTON_HOVER, COLOR_BACK_BUTTON,
            self.back_button_rect, border_radius, button_text, COLOR_BUTTON_TEXT, self.font_back_button,
            mouse_pos, left_mouse_down)

    def draw_game_over_screen(self):

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        if not hasattr(self , "_win_music_played"):
            pygame.mixer.music.stop()
            if True:
                if self.winner == "X":
                    pygame.mixer.music.load(WIN_MUSIC)
                elif self.winner == "O":
                    pygame.mixer.music.load(LOSE_MUSIC)
                pygame.mixer.music.play()
                self._win_music_played = True


        overlay.fill(self.game_over_bg_color)
        self.screen.blit(overlay, (0, 0))


        if self.font_large:
             final_text = f"Player {self.winner} Wins!" if self.winner and self.winner != 'draw' else "It's a Draw!"
             draw_text(self.screen, final_text, self.font_large, self.game_over_text_color,
                       (self.screen_width // 2, self.screen_height // 2 - int(self.screen_height * 0.1)))
        # Draw Buttons
        button_height = max(40, int(self.screen_height * 0.07));
        spacing = 30

        button_height = max(40 , int(self.screen_height * 0.07))
        spacing = 30  # spacing between the two buttons

        button_font = get_font(BASE_FONT_SIZE_SMALL * 0.85)
        if button_font:
            mouse_pos = pygame.mouse.get_pos()
            left_mouse_down = pygame.mouse.get_pressed()[0]

            # Measure text sizes
            text_play_again = "Play Again"
            text_menu = "Menu"

            play_again_width , _ = button_font.size(text_play_again)
            menu_width , _ = button_font.size(text_menu)

            pad_x = 40  # horizontal padding inside buttons
            pad_y = 10  # vertical padding (optional)

            play_again_button_width = play_again_width + pad_x
            menu_button_width = menu_width + pad_x
            button_height += pad_y

            pa_center_x = self.screen_width // 1.8 - (play_again_button_width // 2 + spacing)
            menu_center_x = self.screen_width // 1.9 + (menu_button_width // 2 + spacing)
            button_y = self.screen_height // 2 + int(self.screen_height * 0.05)
            border_radius = int(button_height * 0.3)

            self.play_again_rect = pygame.Rect(0 , 0 , play_again_button_width , button_height)
            self.play_again_rect.center = (pa_center_x , button_y)

            self.menu_rect = pygame.Rect(0 , 0 , menu_button_width , button_height)
            self.menu_rect.center = (menu_center_x , button_y)

            draw_curved_rect_button(self.screen , COLOR_BUTTON , COLOR_BUTTON_HOVER , COLOR_BUTTON_CLICK ,
                                    self.play_again_rect , border_radius , text_play_again , COLOR_BUTTON_TEXT ,
                                    button_font , mouse_pos , left_mouse_down)

            draw_curved_rect_button(self.screen , COLOR_BUTTON , COLOR_BUTTON_HOVER , COLOR_BUTTON_CLICK ,
                                    self.menu_rect , border_radius , text_menu , COLOR_BUTTON_TEXT ,
                                    button_font , mouse_pos , left_mouse_down)

    def run_game(self, mode="multiplayer", initial_volume=1.0, current_score_x=0, current_score_o=0):
        self.score_x = current_score_x; self.score_o = current_score_o
        music_playing = False
        if True:
            pygame.mixer.music.load(GAME_MUSIC); pygame.mixer.music.set_volume(initial_volume)
            pygame.mixer.music.play(-1); music_playing = True

        self.reset_game(); self.game_running = True; ai_turn = False
        while self.game_running:
            mouse_pos = pygame.mouse.get_pos(); mouse_down_event = False; mouse_up_event = False
            left_mouse_down_state = pygame.mouse.get_pressed()[0]; should_quit = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: should_quit = True; break
                if event.type == pygame.VIDEORESIZE: pass
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f: pass
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: mouse_down_event = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: mouse_up_event = True
            if should_quit:
                 if music_playing: pygame.mixer.music.stop(); return ("quit", None)
            if mouse_up_event:
                 if not self.game_over_state and self.back_button_rect and self.back_button_rect.collidepoint(mouse_pos):
                      if music_playing: pygame.mixer.music.stop(); return ("menu", None)
                 if self.reset_score_rect and self.reset_score_rect.collidepoint(mouse_pos):
                      if music_playing: pygame.mixer.music.stop(); return ("reset_score", None)
                 if self.game_over_state:
                    if self.play_again_rect and self.play_again_rect.collidepoint(mouse_pos):
                        if music_playing: pygame.mixer.music.stop(); return ("play_again", self.winner)
                    elif self.menu_rect and self.menu_rect.collidepoint(mouse_pos):
                        if music_playing: pygame.mixer.music.stop(); return ("menu", self.winner)
            if self.taking_move:
                if mode == "singleplayer" and self.player == "O":
                    if not ai_turn:
                        ai_turn = True; self.draw_table(); self._message(); self._draw_score(); self._draw_back_button()
                        pygame.display.flip(); self._ai_move(); ai_turn = False
                else:
                    if mouse_down_event:
                         clicked_on_ui = (self.back_button_rect and self.back_button_rect.collidepoint(mouse_pos)) or \
                                         (self.reset_score_rect and self.reset_score_rect.collidepoint(mouse_pos))
                         if not clicked_on_ui: self._move(mouse_pos)
            self.draw_table(); self._message(); self._draw_score()
            if not self.game_over_state: self._draw_back_button()
            if self.game_over_state: self.draw_game_over_screen()
            pygame.display.flip(); self.FPS_CLOCK.tick(FPS)
        if music_playing: pygame.mixer.music.stop()
        return ("menu", self.winner if self.winner else "draw")

def draw_menu_button(screen, rect, text, font, colors, mouse_pos, is_mouse_down, border_radius):
    return draw_curved_rect_button(screen, colors['default'], colors['hover'], colors['click'],
        rect, border_radius, text, colors['text'], font, mouse_pos, is_mouse_down)

def game_menu(screen, click_sound):
    width, height = LOGICAL_WIDTH, LOGICAL_HEIGHT
    font_buttons = get_font(BASE_FONT_SIZE_LARGE)
    button_height = max(50, int(height * 0.1))
    button_width = min(int(button_height * 4.0), int(width * 0.8))
    border_radius = int(button_height * 0.3)
    button_spacing = button_height * 1.3
    button_colors = {
        'default': COLOR_BUTTON,
        'hover': COLOR_BUTTON_HOVER,
        'click': COLOR_BUTTON_CLICK,
        'text': COLOR_BUTTON_TEXT
    }
    button_texts = ["Single Player", "Multi Player", "Settings", "Exit"]
    num_buttons = len(button_texts)
    total_menu_height = (num_buttons * button_height) + ((num_buttons - 1) * (button_spacing - button_height))
    start_y = max(int(height * 0.1), (height - total_menu_height) // 2)

    # Create falling balls for background animation
    falling_balls = [FallingBall(width, height) for _ in range(60)]

    menu_running = True
    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        clicked_up = False
        left_mouse_down = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked_up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pass
            if event.type == pygame.VIDEORESIZE:
                pass

        # Draw animated background
        screen.fill(COLOR_MENU_BG)
        for ball in falling_balls:
            ball.update()
            ball.draw(screen)

        # Maintain ball count
        falling_balls = [ball for ball in falling_balls if not ball.is_off_screen(height)]
        while len(falling_balls) < 60:
            falling_balls.append(FallingBall(width, height))

        # Draw menu buttons
        current_y = start_y
        for text in button_texts:
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.top = current_y
            button_rect.centerx = width // 2
            _, on_button = draw_menu_button(screen, button_rect, text, font_buttons, button_colors, mouse_pos, left_mouse_down, border_radius)
            current_y += button_height + (button_spacing - button_height)

            if clicked_up and on_button:
                if True:
                    click_sound.play()

                action = text.lower().replace(" ", "")
                print(f"Menu: {text} selected")
                if action == "exit":
                    pygame.quit()
                    sys.exit()
                return action
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def settings_screen(screen, click_sound):
    width, height = LOGICAL_WIDTH, LOGICAL_HEIGHT
    font_buttons = get_font(BASE_FONT_SIZE_LARGE)
    button_height = max(50, int(height * 0.1))
    button_width = min(int(button_height * 4.0), int(width * 0.8))
    border_radius = int(button_height * 0.3)
    button_spacing = button_height * 1.3
    button_colors = {
        'default': COLOR_BUTTON,
        'hover': COLOR_BUTTON_HOVER,
        'click': COLOR_BUTTON_CLICK,
        'text': COLOR_BUTTON_TEXT
    }
    button_texts = ["Volume", "Back"]
    num_buttons = len(button_texts)
    total_menu_height = (num_buttons * button_height) + ((num_buttons - 1) * (button_spacing - button_height))
    start_y = max(int(height * 0.1), (height - total_menu_height) // 2)

    # Falling ball background
    falling_balls = [FallingBall(width, height) for _ in range(20)]

    settings_running = True
    while settings_running:
        mouse_pos = pygame.mouse.get_pos()
        clicked_up = False
        left_mouse_down = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked_up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pass
            if event.type == pygame.VIDEORESIZE:
                pass

        # Animate background
        screen.fill(COLOR_MENU_BG)
        for ball in falling_balls:
            ball.update()
            ball.draw(screen)

        falling_balls = [ball for ball in falling_balls if not ball.is_off_screen(height)]
        while len(falling_balls) < 20:
            falling_balls.append(FallingBall(width, height))

        # Draw buttons
        current_y = start_y
        for text in button_texts:
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.top = current_y
            button_rect.centerx = width // 2
            _, on_button = draw_menu_button(screen, button_rect, text, font_buttons, button_colors, mouse_pos, left_mouse_down, border_radius)
            current_y += button_height + (button_spacing - button_height)

            if clicked_up and on_button:
                try:
                    click_sound.play()
                except:
                    pass
                action = text.lower().replace(" ", "")
                print(f"Settings: {text} selected")
                if action == "volume":
                    return "volume"
                elif action == "back":
                    return "menu"

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def volume_settings_screen(screen, click_sound, current_volume):
    width, height = LOGICAL_WIDTH, LOGICAL_HEIGHT
    font_buttons = get_font(BASE_FONT_SIZE_LARGE * 1.1)
    font_info = get_font(BASE_FONT_SIZE_MEDIUM)
    font_back = get_font(BASE_FONT_SIZE_MEDIUM)
    pm_button_size = max(50, int(min(width, height) * 0.12))
    back_button_height = max(40, int(height * 0.08))
    back_button_width = int(back_button_height * 3)
    border_radius = int(pm_button_size * 0.3)
    back_border_radius = int(back_button_height * 0.3)

    button_colors = {
        'default': COLOR_BUTTON,
        'hover': COLOR_BUTTON_HOVER,
        'click': COLOR_BUTTON_CLICK,
        'text': COLOR_BUTTON_TEXT
    }

    new_volume = current_volume
    center_x = width // 2
    center_y = height // 2
    pm_spacing = int(pm_button_size * 1.5)

    minus_rect = pygame.Rect(0, 0, pm_button_size, pm_button_size)
    minus_rect.center = (center_x - pm_spacing // 2, center_y)

    plus_rect = pygame.Rect(0, 0, pm_button_size, pm_button_size)
    plus_rect.center = (center_x + pm_spacing // 2, center_y)

    back_rect = pygame.Rect(0, 0, back_button_width, back_button_height)
    back_rect.center = (center_x, center_y + pm_button_size * 0.8 + back_button_height // 2)

    button_definitions = [
        (minus_rect, "-", font_buttons, border_radius),
        (plus_rect, "+", font_buttons, border_radius),
        (back_rect, "Back", font_back, back_border_radius)
    ]

    volume_display_pos = (center_x, center_y - pm_button_size * 0.8)

    falling_balls = [FallingBall(width, height) for _ in range(60)]

    volume_running = True
    while volume_running:
        mouse_pos = pygame.mouse.get_pos()
        clicked_up = False
        left_mouse_down = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                clicked_up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                pass
            if event.type == pygame.VIDEORESIZE:
                pass

        # ✨ Animate background
        screen.fill(COLOR_MENU_BG)
        for ball in falling_balls:
            ball.update()
            ball.draw(screen)

        falling_balls = [ball for ball in falling_balls if not ball.is_off_screen(height)]
        while len(falling_balls) < 60:
            falling_balls.append(FallingBall(width, height))

        volume_percent = int(new_volume * 100)
        draw_text(screen, f"Volume: {volume_percent}%", font_info, COLOR_WHITE, volume_display_pos)

        for rect, text, font, radius in button_definitions:
            _, on_button = draw_menu_button(screen, rect, text, font, button_colors, mouse_pos, left_mouse_down, radius)

            if clicked_up and on_button:
                try:
                    click_sound.play()
                except:
                    pass
                action = text
                print(f"Volume action: {action}")
                if action == "-":
                    new_volume = max(0.0, round(new_volume - 0.1, 1))
                elif action == "+":
                    new_volume = min(1.0, round(new_volume + 0.1, 1))
                elif action == "Back":
                    return round(new_volume, 2)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def opening_screen(screen, music_path, volume):
    width, height = LOGICAL_WIDTH, LOGICAL_HEIGHT; font_info = get_font(BASE_FONT_SIZE_MEDIUM)
    background_image = None; raw_image = None
    if True:
        raw_image = pygame.image.load(OPENING_BACKGROUND_IMG).convert()
        background_image = pygame.transform.smoothscale(raw_image, (width, height))
    music_playing = False
    if True:
        pygame.mixer.music.load(music_path); pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1); music_playing = True
    instructions_pos = (width // 2, height * 0.75)
    quit_pos = (width // 2, instructions_pos[1] + font_info.get_height() * 1.2)
    opening_running = True
    while opening_running:
        current_physical_width, current_physical_height = pygame.display.get_surface().get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if music_playing: pygame.mixer.music.stop(); pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if music_playing: pygame.mixer.music.fadeout(500); return
                if event.key == pygame.K_ESCAPE:
                    if music_playing: pygame.mixer.music.stop(); pygame.quit(); sys.exit()
            if event.type == pygame.VIDEORESIZE: pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f: pass
        if background_image: screen.blit(background_image, (0, 0))
        else: screen.fill(COLOR_BLACK)
        if font_info:
            draw_text(screen, "Press SPACE to start", font_info, COLOR_INSTRUCTIONS, instructions_pos)
            draw_text(screen, "Press ESC to quit", font_info, COLOR_INSTRUCTIONS, quit_pos)
        pygame.display.flip(); pygame.time.Clock().tick(FPS)

# --- Main Application ---
def main():
    if True: pygame.init(); pygame.mixer.init()
    window_width, window_height = LOGICAL_WIDTH, LOGICAL_HEIGHT; volume_level = 0.8; screen = None
    if True:
        screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Tic Tac Toe")
    clock = pygame.time.Clock(); score_x = 0; score_o = 0; click_sound = None
    try: click_sound = pygame.mixer.Sound(CLICK_SOUND)
    except pygame.error as e:
        print(f"Warning: Click sound load error: {e}")
        class DummySound:
            def play(self): pass
            def set_volume(self, vol): pass
        click_sound = DummySound()
    app_running = True; current_state = "opening"; is_fullscreen = False
    while app_running:
        current_physical_size = pygame.display.get_surface().get_size()
        if click_sound and hasattr(click_sound, 'set_volume'):
             try: click_sound.set_volume(volume_level)
             except: pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT: app_running = False; break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    try:
                        if is_fullscreen: screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
                        else: screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE | pygame.SCALED)
                        print(f"Toggled fullscreen: {is_fullscreen}. New size: {screen.get_size()}")
                    except pygame.error as e: print(f"Error toggling fullscreen: {e}"); is_fullscreen = not is_fullscreen
            if event.type == pygame.VIDEORESIZE:
                if not is_fullscreen:
                    window_width, window_height = event.w, event.h
                    print(f"Window resized to: {window_width}x{window_height}")
        if not app_running: break
        try:
            if current_state == "opening":
                opening_screen(screen, OPENING_MUSIC, volume_level); current_state = "menu"
            elif current_state == "menu":
                action = game_menu(screen, click_sound)
                if action in ["singleplayer", "multiplayer", "settings"]: current_state = action
            elif current_state == "settings":
                action = settings_screen(screen, click_sound)
                if action in ["volume", "screensize", "menu"]: current_state = action
            elif current_state == "volume":
                returned_volume = volume_settings_screen(screen, click_sound, volume_level)
                if returned_volume is not None:
                    volume_level = returned_volume; print(f"Volume set to: {int(volume_level * 100)}%")
                    try: pygame.mixer.music.set_volume(volume_level)
                    except pygame.error as e: print(f"Could not set music volume: {e}")
                current_state = "settings"

            elif current_state in ["singleplayer", "multiplayer"]:
                game_mode = current_state; game = TicTacToe(screen)
                result_state, winner = game.run_game(mode=game_mode, initial_volume=volume_level, current_score_x=score_x, current_score_o=score_o)
                print(f"Game finished. Winner: {winner}, Result state: {result_state}")
                if result_state == "quit": app_running = False
                elif result_state == "reset_score": score_x = 0; score_o = 0; current_state = game_mode
                elif result_state == "play_again":
                    if winner == 'X':
                        score_x += 1
                    elif winner == 'O':
                        score_o += 1
                    print(f"Scores: X={score_x}, O={score_o}")
                    current_state = game_mode
                else:
                    if winner == 'X':
                        score_x += 1
                    elif winner == 'O':
                        score_o += 1
                    print(f"Scores: X={score_x}, O={score_o}")
                    current_state = "menu"

            else: print(f"Error: Unknown state '{current_state}'"); current_state = "menu"
        except Exception as e:
             print(f"Error during state '{current_state}': {e}")
             import traceback; traceback.print_exc(); current_state = "menu"
        clock.tick(FPS)
    print("Exiting application.")
    pygame.mixer.music.stop(); pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()
