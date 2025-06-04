
from LogicModel import LogicModel
from LogicController import LogicController
import io
import sys

class GameRunner:
    def __init__(self, N=5, M=10):
        self.N = N
        self.M = M
        
        
        self.player1_controller = LogicController()
        self.player2_controller = LogicController()
        
        
        self.current_board = LogicModel(N, M)
        self.setup_initial_board()
        
        self.move_count = 0
        self.current_player = 1
        
    def setup_initial_board(self):
        """Set up the initial game state"""
        
        self.current_board.player1 = (0, self.N-1)
        self.current_board.player2 = (self.current_board.SWN-1, self.N-1)
        
        
        self.current_board.matrix[self.current_board.player1[0]][self.current_board.player1[1]] = 1
        self.current_board.matrix[self.current_board.player2[0]][self.current_board.player2[1]] = 2
    
    def format_board_for_input(self, for_player1=True):
        """Format the current board state for LogicController input"""
        lines = []
        
        if self.move_count == 0:
            
            lines.append(f"{self.N} {self.M}")
            for i in range(self.current_board.SWN):
                row = " ".join(str(self.current_board.matrix[i][j]) for j in range(self.current_board.SWN))
                lines.append(row)
        else:
            
            lines.append(self.last_move_output)
            for i in range(self.current_board.SWN):
                row = " ".join(str(self.current_board.matrix[i][j]) for j in range(self.current_board.SWN))
                lines.append(row)
            
            
            if for_player1:
                lines.append(str(self.current_board.my_walls_count))
            else:
                lines.append(str(self.current_board.opponent_walls_count))
        
        return "\n".join(lines)
    
    def apply_move_to_board(self, move_str, player_num):
        """Apply a move string to the current board"""
        parts = move_str.strip().split()
        move_type = parts[0]
        
        if move_type == 'L':
            
            new_row, new_col = int(parts[1]), int(parts[2])
            
            if player_num == 1:
                
                old_pos = self.current_board.player1
                self.current_board.matrix[old_pos[0]][old_pos[1]] = 0
                
                self.current_board.player1 = (new_row, new_col)
                self.current_board.matrix[new_row][new_col] = 1
            else:
                
                old_pos = self.current_board.player2
                self.current_board.matrix[old_pos[0]][old_pos[1]] = 0
                
                self.current_board.player2 = (new_row, new_col)
                self.current_board.matrix[new_row][new_col] = 2
                
        elif move_type == 'F':
            
            x1, y1, x2, y2 = int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])
            
            
            if x1 == x2:  
                wall_type = 'H'
                row, col = x1, min(y1, y2)
            else:  
                wall_type = 'V'
                row, col = min(x1, x2), y1
            
            
            self.current_board.place_wall(wall_type, row, col)
            
            
            if player_num == 1:
                self.current_board.my_walls_count -= 1
            else:
                self.current_board.opponent_walls_count -= 1
        
        
        self.last_move_output = move_str.strip()
    
    def get_player_move(self, player_num):
        """Get a move from the specified player's controller"""
        
        input_str = self.format_board_for_input(for_player1=(player_num == 1))
        
        
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(input_str)
        
        
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            if player_num == 1:
                self.player1_controller.play_game()
            else:
                self.player2_controller.play_game()
            
            
            move_output = sys.stdout.getvalue().strip()
            
        finally:
            
            sys.stdin = old_stdin
            sys.stdout = old_stdout
        
        return move_output
    
    def print_board(self):
        """Print the current board state"""
        print(f"\n=== Move {self.move_count} ===")
        print(f"Player 1 walls: {self.current_board.my_walls_count}")
        print(f"Player 2 walls: {self.current_board.opponent_walls_count}")
        print(f"Current player: {self.current_player}")
        
        
        for i in range(self.current_board.SWN):
            row_str = ""
            for j in range(self.current_board.SWN):
                if self.current_board.matrix[i][j] == 1:
                    row_str += "P1 "
                elif self.current_board.matrix[i][j] == 2:
                    row_str += "P2 "
                elif self.current_board.matrix[i][j] == 9:
                    row_str += "## "
                elif i % 2 == 0 and j % 2 == 0:
                    row_str += "·  "
                else:
                    row_str += "   "
            print(row_str)
        print("-" * 30)
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.current_board.is_game_over() != 0
    
    def get_winner(self):
        """Get the winner of the game"""
        return self.current_board.is_game_over()
    
    def run_game(self, max_moves=100, show_board=True):
        """Run a complete game between two LogicControllers"""
        print("🎮 Starting Quoridor Game: LogicController vs LogicController")
        print(f"Board: {self.N}x{self.N}, Walls: {self.M} each")
        
        self.last_move_output = ""  
        
        if show_board:
            self.print_board()
        
        while not self.is_game_over() and self.move_count < max_moves:
            self.move_count += 1
            
            try:
                
                print(f"\nPlayer {self.current_player} is thinking...")
                move = self.get_player_move(self.current_player)
                print(f"Player {self.current_player} plays: {move}")
                
                
                self.apply_move_to_board(move, self.current_player)
                
                if show_board:
                    self.print_board()
                
                
                self.current_player = 2 if self.current_player == 1 else 1
                
            except Exception as e:
                print(f"Error during Player {self.current_player}'s move: {e}")
                break
        
        
        winner = self.get_winner()
        print(f"\n🏁 GAME OVER!")
        if winner != 0:
            print(f"🎉 Winner: Player {winner}!")
        else:
            print("Game ended in a draw (max moves reached)")
        print(f"Total moves: {self.move_count}")



if __name__ == "__main__":
    
    game = GameRunner(N=5, M=10)
    game.run_game(max_moves=50, show_board=True)