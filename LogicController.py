from LogicModel import LogicModel

class LogicController:
    def __init__(self):
        self.logic_model = LogicModel(5, 6)  # Default values, will be updated
        self.max_depth = 4
        
    def minimax(self, model, depth, maximizing_player, alpha, beta):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or model.is_game_over():
            return model.evaluate_position()
        
        if maximizing_player:
            max_eval = float('-inf')
            for move_type, move_data, child_model in model.get_all_possible_moves():
                eval_score = self.minimax(child_model, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            # For opponent moves, we need to simulate their possible moves
            # This is simplified - in a full implementation, we'd get opponent's valid moves
            eval_score = model.evaluate_position()
            return eval_score

    def find_best_move(self):
        """Find the best move using minimax algorithm"""
        best_score = float('-inf')
        best_move = None
        
        for move_type, move_data, child_model in self.logic_model.get_all_possible_moves():
            score = self.minimax(child_model, self.max_depth - 1, False, float('-inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_move = (move_type, move_data)
        
        return best_move

    def format_output(self, move_type, move_data):
        """Format the move for output"""
        if move_type == 'L':
            # Pawn move
            row, col = move_data
            return f"L {row} {col}"
        else:  # move_type == 'F'
            # Wall placement
            wall_type, row, col = move_data
            if wall_type == 'H':
                # Horizontal wall: from (row, col) to (row, col+2)
                return f"F {row} {col} {row} {col+2}"
            else:  # wall_type == 'V'
                # Vertical wall: from (row, col) to (row+2, col)
                return f"F {row} {col} {row+2} {col}"

    def play_game(self):
        """Main game loop"""
        # Read initial input
        self.logic_model.read_initial_input()
        
        # Check if it's the first move (no opponent move yet)
        try:
            # Try to read opponent's move
            opponent_move = self.logic_model.read_move_input()
        except:
            # This is the first move
            pass
        
        # Find and make the best move
        best_move = self.find_best_move()
        if best_move:
            move_type, move_data = best_move
            output = self.format_output(move_type, move_data)
            print(output)
        else:
            # Fallback: make any valid move
            valid_moves = self.logic_model.get_valid_moves(1)
            if valid_moves:
                pos = valid_moves[0]
                print(f"L {pos[0]} {pos[1]}")


# Main execution
if __name__ == "__main__":
    controller = LogicController()
    controller.play_game()