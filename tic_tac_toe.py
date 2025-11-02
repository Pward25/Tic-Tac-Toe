import arcade
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Tic Tac Toe"
GRID_SIZE = 3
CELL_SIZE = 180
GRID_OFFSET_X = 30
GRID_OFFSET_Y = 100

class TicTacToe(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.game_mode = None  # None, 'PVP', 'EASY', 'MEDIUM', 'HARD'
        self.waiting_for_computer = False
        self.computer_move_timer = 0
        
        # Load sound effects
        # Note: Download the sound files from your GitHub repo and place them in the same folder as this script
        # Or update the paths below to where your sound files are located
        try:
            # Try loading from local files first
            self.select_sound = arcade.load_sound("select.mp3")
            self.lose_sound = arcade.load_sound("lose.mp3")
            self.win_sound = arcade.load_sound("win.mp3")
            print("Sounds loaded successfully!")
        except Exception as e:
            print(f"Error loading sounds: {e}")
            print("Make sure select.mp3, lose.mp3, and win.mp3 are in the same folder as this script")
            self.select_sound = None
            self.lose_sound = None
            self.win_sound = None
        
    def on_draw(self):
        self.clear()
        
        # Draw title
        arcade.draw_text("TIC TAC TOE", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
                        arcade.color.BLACK, 32, anchor_x="center", bold=True)
        
        if self.game_mode is None:
            # Draw menu
            arcade.draw_text("Choose Game Mode:", SCREEN_WIDTH // 2, 480,
                           arcade.color.BLACK, 24, anchor_x="center", bold=True)
            
            # Player vs Player button
            self.draw_button(SCREEN_WIDTH // 2, 380, 250, 50, "Player vs Player",
                           arcade.color.LIGHT_BLUE, arcade.color.BLACK)
            
            # VS Computer buttons
            arcade.draw_text("VS Computer:", SCREEN_WIDTH // 2, 300,
                           arcade.color.BLACK, 20, anchor_x="center", bold=True)
            
            self.draw_button(SCREEN_WIDTH // 2, 240, 200, 45, "Easy",
                           arcade.color.LIGHT_GREEN, arcade.color.BLACK)
            
            self.draw_button(SCREEN_WIDTH // 2, 180, 200, 45, "Medium",
                           arcade.color.LIGHT_YELLOW, arcade.color.BLACK)
            
            self.draw_button(SCREEN_WIDTH // 2, 120, 200, 45, "Hard",
                           arcade.color.LIGHT_CORAL, arcade.color.BLACK)
            
            return
        
        # Draw grid lines
        for i in range(1, GRID_SIZE):
            x = GRID_OFFSET_X + i * CELL_SIZE
            arcade.draw_line(x, GRID_OFFSET_Y, x, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE,
                           arcade.color.BLACK, 3)
            y = GRID_OFFSET_Y + i * CELL_SIZE
            arcade.draw_line(GRID_OFFSET_X, y, GRID_OFFSET_X + GRID_SIZE * CELL_SIZE, y,
                           arcade.color.BLACK, 3)
        
        # Draw board border
        border_left = GRID_OFFSET_X
        border_right = GRID_OFFSET_X + GRID_SIZE * CELL_SIZE
        border_bottom = GRID_OFFSET_Y
        border_top = GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE
        arcade.draw_lrbt_rectangle_outline(border_left, border_right, border_bottom, border_top,
                                          arcade.color.BLACK, 3)
        
        # Draw X's and O's
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_x = GRID_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                cell_y = GRID_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                
                if self.board[row][col] == 'X':
                    offset = 50
                    arcade.draw_line(cell_x - offset, cell_y - offset,
                                   cell_x + offset, cell_y + offset,
                                   arcade.color.BLUE, 5)
                    arcade.draw_line(cell_x + offset, cell_y - offset,
                                   cell_x - offset, cell_y + offset,
                                   arcade.color.BLUE, 5)
                elif self.board[row][col] == 'O':
                    arcade.draw_circle_outline(cell_x, cell_y, 50,
                                             arcade.color.RED, 5)
        
        # Draw game status
        if self.game_over:
            if self.winner:
                text = f"Player {self.winner} Wins! Click to play again"
                color = arcade.color.GREEN
            else:
                text = "It's a Draw! Click to play again"
                color = arcade.color.ORANGE
        else:
            if self.game_mode == 'PVP':
                text = f"Current Player: {self.current_player}"
            else:
                if self.current_player == 'X':
                    text = "Your turn (X)"
                else:
                    text = "Computer thinking..."
            color = arcade.color.BLACK
            
        arcade.draw_text(text, SCREEN_WIDTH // 2, 30,
                        color, 18, anchor_x="center", bold=True)
        
        # Draw back button
        if not self.game_over:
            arcade.draw_text("Menu", 30, SCREEN_HEIGHT - 35,
                           arcade.color.GRAY, 14, anchor_x="left")
    
    def draw_button(self, center_x, center_y, width, height, text, bg_color, text_color):
        arcade.draw_lrbt_rectangle_filled(center_x - width/2, center_x + width/2,
                                         center_y - height/2, center_y + height/2,
                                         bg_color)
        arcade.draw_lrbt_rectangle_outline(center_x - width/2, center_x + width/2,
                                          center_y - height/2, center_y + height/2,
                                          arcade.color.BLACK, 2)
        arcade.draw_text(text, center_x, center_y, text_color, 18,
                        anchor_x="center", anchor_y="center", bold=True)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_mode is None:
            # Menu selection
            if self.is_button_clicked(x, y, SCREEN_WIDTH // 2, 380, 250, 50):
                self.game_mode = 'PVP'
                self.play_sound(self.select_sound)
            elif self.is_button_clicked(x, y, SCREEN_WIDTH // 2, 240, 200, 45):
                self.game_mode = 'EASY'
                self.play_sound(self.select_sound)
            elif self.is_button_clicked(x, y, SCREEN_WIDTH // 2, 180, 200, 45):
                self.game_mode = 'MEDIUM'
                self.play_sound(self.select_sound)
            elif self.is_button_clicked(x, y, SCREEN_WIDTH // 2, 120, 200, 45):
                self.game_mode = 'HARD'
                self.play_sound(self.select_sound)
            return
        
        # Check back button
        if 30 <= x <= 100 and SCREEN_HEIGHT - 50 <= y <= SCREEN_HEIGHT - 20:
            self.return_to_menu()
            return
        
        if self.game_over:
            self.reset_game()
            return
        
        # Don't allow moves during computer's turn
        if self.waiting_for_computer:
            return
        
        # Check if click is within grid
        if (GRID_OFFSET_X <= x <= GRID_OFFSET_X + GRID_SIZE * CELL_SIZE and
            GRID_OFFSET_Y <= y <= GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE):
            
            col = int((x - GRID_OFFSET_X) // CELL_SIZE)
            row = int((y - GRID_OFFSET_Y) // CELL_SIZE)
            
            if self.board[row][col] == '':
                self.play_sound(self.select_sound)
                self.make_move(row, col)
    
    def is_button_clicked(self, x, y, btn_x, btn_y, width, height):
        return (btn_x - width/2 <= x <= btn_x + width/2 and
                btn_y - height/2 <= y <= btn_y + height/2)
    
    def play_sound(self, sound):
        if sound:
            arcade.play_sound(sound)
    
    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
            # Play win/lose sound
            if self.game_mode != 'PVP':
                if self.current_player == 'X':
                    self.play_sound(self.win_sound)
                else:
                    self.play_sound(self.lose_sound)
            else:
                self.play_sound(self.win_sound)
        elif self.is_board_full():
            self.game_over = True
            self.winner = None
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # If computer's turn, trigger computer move
            if not self.game_over and self.game_mode != 'PVP' and self.current_player == 'O':
                self.waiting_for_computer = True
                self.computer_move_timer = 0.5  # Delay for realism
    
    def on_update(self, delta_time):
        if self.waiting_for_computer:
            self.computer_move_timer -= delta_time
            if self.computer_move_timer <= 0:
                self.computer_move()
                self.waiting_for_computer = False
    
    def computer_move(self):
        if self.game_mode == 'EASY':
            self.computer_move_easy()
        elif self.game_mode == 'MEDIUM':
            self.computer_move_medium()
        elif self.game_mode == 'HARD':
            self.computer_move_hard()
    
    def computer_move_easy(self):
        # Random move
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)
                      if self.board[r][c] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)
    
    def computer_move_medium(self):
        # 50% strategic, 50% random
        if random.random() < 0.5:
            self.computer_move_hard()
        else:
            self.computer_move_easy()
    
    def computer_move_hard(self):
        # Use minimax algorithm for optimal play
        best_score = float('-inf')
        best_move = None
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == '':
                    self.board[r][c] = 'O'
                    score = self.minimax(False, -float('inf'), float('inf'))
                    self.board[r][c] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        
        if best_move:
            self.make_move(best_move[0], best_move[1])
    
    def minimax(self, is_maximizing, alpha, beta):
        # Check terminal states
        if self.check_winner_for_player('O'):
            return 10
        if self.check_winner_for_player('X'):
            return -10
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            max_score = float('-inf')
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.board[r][c] == '':
                        self.board[r][c] = 'O'
                        score = self.minimax(False, alpha, beta)
                        self.board[r][c] = ''
                        max_score = max(score, max_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return max_score
        else:
            min_score = float('inf')
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.board[r][c] == '':
                        self.board[r][c] = 'X'
                        score = self.minimax(True, alpha, beta)
                        self.board[r][c] = ''
                        min_score = min(score, min_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return min_score
    
    def check_winner(self):
        return self.check_winner_for_player(self.current_player)
    
    def check_winner_for_player(self, player):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] == player:
                return True
        
        # Check columns
        for col in range(GRID_SIZE):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        
        return False
    
    def is_board_full(self):
        for row in self.board:
            if '' in row:
                return False
        return True
    
    def reset_game(self):
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.waiting_for_computer = False
    
    def return_to_menu(self):
        self.game_mode = None
        self.reset_game()

def main():
    game = TicTacToe()
    arcade.run()

if __name__ == "__main__":
    main()