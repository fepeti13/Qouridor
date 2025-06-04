from LogicModel import LogicModel

class LogicController:
    def __init__(self):
        self.logic_model = LogicModel(5, 6)  
        self.max_depth = 4
        
    def minimax(self, model, depth, maximizing_player, alpha, beta):
        
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
            eval_score = model.evaluate_position()
            return eval_score

    def find_best_move(self):
        
        best_score = float('-inf')
        best_move = None
        
        print(self.logic_model.get_all_possible_moves())

        for move_type, move_data, child_model in self.logic_model.get_all_possible_moves():
            score = self.minimax(child_model, self.max_depth - 1, False, float('-inf'), float('inf'))
            if score > best_score:
                best_score = score
                best_move = (move_type, move_data)
        
        return best_move

    def format_output(self, move_type, move_data):
        
        if move_type == 'L':
            row, col = move_data
            return f"L {row} {col}"
        else:
            wall_type, row, col = move_data
            if wall_type == 'H':
                return f"F {row} {col} {row} {col+2}"
            else:
                return f"F {row} {col} {row+2} {col}"

    def start_game(self):
        self.logic_model.read_initial_input()

        best_move = self.find_best_move()
        if best_move:
            move_type, move_data = best_move
            if move_type == "F":
                self.logic_model.my_walls_count
            output = self.format_output(move_type, move_data)
            print(output)
        else:
            
            valid_moves = self.logic_model.get_valid_moves(1)
            if valid_moves:
                pos = valid_moves[0]
                print(f"L {pos[0]} {pos[1]}")
        self.play_game()

    def play_game(self):   
        self.logic_model.read_move_input()
        
        best_move = self.find_best_move()
        if best_move:
            move_type, move_data = best_move
            if move_type == "F":
                self.logic_model.my_walls_count
            output = self.format_output(move_type, move_data)
            print(output)
        else:
            
            valid_moves = self.logic_model.get_valid_moves(1)
            if valid_moves:
                pos = valid_moves[0]
                print(f"L {pos[0]} {pos[1]}")

        self.play_game()

if __name__ == "__main__":
    controller = LogicController()
    controller.start_game()