import copy
from collections import deque
import sys

class LogicModel:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.SWN = 2 * N - 1
        
        
        self.matrix = []
        for i in range(self.SWN):
            row = [0] * self.SWN
            self.matrix.append(row)

        
        self.player1 = None  
        self.player2 = None  
        
        
        self.my_walls_count = M
        self.opponent_walls_count = M

    def read_initial_input(self):
        line = input().strip().split()
        N = int(line[0])
        M = int(line[1])
        self.__init__(N, M)
        
        for i in range(self.SWN):
            row = list(map(int, input().strip().split()))
            self.matrix[i] = row
            
            
            for j in range(self.SWN):
                if row[j] == 1:
                    self.player1 = (i, j)
                elif row[j] == 2:
                    self.player2 = (i, j)

    def read_move_input(self):
        move_line = input().strip().split()
        move_type = move_line[0]
        
        if move_type == 'L':
            x, y = int(move_line[1]), int(move_line[2])
            opponent_move = ('L', x, y)
        else:
            x1, y1, x2, y2 = int(move_line[1]), int(move_line[2]), int(move_line[3]), int(move_line[4])
            opponent_move = ('F', x1, y1, x2, y2)
            self.opponent_walls_count -= 1
        
        for i in range(self.SWN):
            row = list(map(int, input().strip().split()))
            self.matrix[i] = row
            
            
            for j in range(self.SWN):
                if row[j] == 1:
                    self.player1 = (i, j)
                elif row[j] == 2:
                    self.player2 = (i, j)
        
        return opponent_move

    def is_valid_position(self, row, col):
        
        return (0 <= row < self.SWN and 0 <= col < self.SWN and 
                row % 2 == 0 and col % 2 == 0)

    def is_wall_between(self, pos1, pos2):
        
        r1, c1 = pos1
        r2, c2 = pos2
        
        
        wall_r = (r1 + r2) // 2
        wall_c = (c1 + c2) // 2
        
        return self.matrix[wall_r][wall_c] == 9

    def get_valid_moves(self, player_num):
        
        if player_num == 1:
            current_pos = self.player1
            opponent_pos = self.player2
        else:
            current_pos = self.player2
            opponent_pos = self.player1
        
        valid_moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  
        
        for dr, dc in directions:
            new_r = current_pos[0] + dr
            new_c = current_pos[1] + dc
            
            
            if not self.is_valid_position(new_r, new_c):
                continue
            
            
            if self.is_wall_between(current_pos, (new_r, new_c)):
                continue
            
            
            if (new_r, new_c) == opponent_pos:
                
                jump_r = new_r + dr
                jump_c = new_c + dc
                
                if (self.is_valid_position(jump_r, jump_c) and 
                    not self.is_wall_between((new_r, new_c), (jump_r, jump_c))):
                    valid_moves.append((jump_r, jump_c))
                else:
                    
                    side_directions = [(0, -2), (0, 2)] if dr != 0 else [(-2, 0), (2, 0)]
                    for side_dr, side_dc in side_directions:
                        diag_r, diag_c = new_r + side_dr, new_c + side_dc
                        if (self.is_valid_position(diag_r, diag_c) and 
                            not self.is_wall_between((new_r, new_c), (diag_r, diag_c))):
                            valid_moves.append((diag_r, diag_c))
            else:
                
                valid_moves.append((new_r, new_c))
        
        return valid_moves

    def get_valid_walls(self):
        
        valid_walls = []
        
        
        for i in range(1, self.SWN, 2):
            for j in range(0, self.SWN-2, 2):
                if (self.matrix[i][j] == 0 and self.matrix[i][j+1] == 0 and 
                    self.matrix[i][j+2] == 0):
                    if self.can_place_wall('H', i, j):
                        valid_walls.append(('H', i, j))
        
        
        for i in range(0, self.SWN-2, 2):
            for j in range(1, self.SWN, 2):
                if (self.matrix[i][j] == 0 and self.matrix[i+1][j] == 0 and 
                    self.matrix[i+2][j] == 0):
                    if self.can_place_wall('V', i, j):
                        valid_walls.append(('V', i, j))
        
        return valid_walls

    def can_place_wall(self, wall_type, row, col):
        
        
        temp_model = copy.deepcopy(self)
        temp_model.place_wall(wall_type, row, col)
        
        
        return (temp_model.has_path_to_goal(1) and temp_model.has_path_to_goal(2))

    def place_wall(self, wall_type, row, col):
        
        if wall_type == 'H':  
            self.matrix[row][col] = 9
            self.matrix[row][col+1] = 9
            self.matrix[row][col+2] = 9
        else:  
            self.matrix[row][col] = 9
            self.matrix[row+1][col] = 9
            self.matrix[row+2][col] = 9

    def has_path_to_goal(self, player_num):
        
        if player_num == 1:
            start = self.player1
            
            if self.player1[0] <= self.SWN // 2:
                goal_condition = lambda pos: pos[0] == self.SWN - 1  
            else:
                goal_condition = lambda pos: pos[0] == 0  
        else:
            start = self.player2
            
            if self.player2[0] <= self.SWN // 2:
                goal_condition = lambda pos: pos[0] == self.SWN - 1  
            else:
                goal_condition = lambda pos: pos[0] == 0  
        
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            current_pos = queue.popleft()
            
            if goal_condition(current_pos):
                return True
            
            
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dr, dc in directions:
                new_r, new_c = current_pos[0] + dr, current_pos[1] + dc
                
                if ((new_r, new_c) not in visited and 
                    self.is_valid_position(new_r, new_c) and
                    not self.is_wall_between(current_pos, (new_r, new_c))):
                    visited.add((new_r, new_c))
                    queue.append((new_r, new_c))
        
        return False

    def shortest_path_to_goal(self, player_num):
        
        if player_num == 1:
            start = self.player1
            if self.player1[0] <= self.SWN // 2:
                goal_condition = lambda pos: pos[0] == self.SWN - 1
            else:
                goal_condition = lambda pos: pos[0] == 0
        else:
            start = self.player2
            if self.player2[0] <= self.SWN // 2:
                goal_condition = lambda pos: pos[0] == self.SWN - 1
            else:
                goal_condition = lambda pos: pos[0] == 0
        
        visited = set()
        queue = deque([(start, 0)])
        visited.add(start)
        
        while queue:
            current_pos, distance = queue.popleft()
            
            if goal_condition(current_pos):
                return distance
            
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dr, dc in directions:
                new_r, new_c = current_pos[0] + dr, current_pos[1] + dc
                
                if ((new_r, new_c) not in visited and 
                    self.is_valid_position(new_r, new_c) and
                    not self.is_wall_between(current_pos, (new_r, new_c))):
                    visited.add((new_r, new_c))
                    queue.append(((new_r, new_c), distance + 1))
        
        return float('inf')  

    def is_game_over(self):
        
        
        if self.player1[0] <= self.SWN // 2:
            if self.player1[0] == self.SWN - 1:
                return 1
        else:
            if self.player1[0] == 0:
                return 1
        
        
        if self.player2[0] <= self.SWN // 2:
            if self.player2[0] == self.SWN - 1:
                return 2
        else:
            if self.player2[0] == 0:
                return 2
        
        return 0

    def evaluate_position(self):
        
        game_result = self.is_game_over()
        if game_result == 1:
            return 1.0
        elif game_result == 2:
            return 0.0
        
        
        player1_distance = self.shortest_path_to_goal(1)
        player2_distance = self.shortest_path_to_goal(2)
        
        if player1_distance == float('inf'):
            return 0.0
        if player2_distance == float('inf'):
            return 1.0
        
        
        total_distance = player1_distance + player2_distance
        if total_distance == 0:
            return 0.5
        
        return 1.0 - (player1_distance / total_distance)

    def make_move(self, new_pos):
        
        
        self.matrix[self.player1[0]][self.player1[1]] = 0
        
        
        self.player1 = new_pos
        self.matrix[new_pos[0]][new_pos[1]] = 1

    def make_wall_move(self, wall_type, row, col):
        
        self.place_wall(wall_type, row, col)
        self.my_walls_count -= 1

    def get_all_possible_moves(self):
        
        moves = []
        
        
        for pos in self.get_valid_moves(1):
            temp_model = copy.deepcopy(self)
            temp_model.make_move(pos)
            moves.append(('L', pos, temp_model))
        
        
        if self.my_walls_count > 0:
            for wall_type, row, col in self.get_valid_walls():
                temp_model = copy.deepcopy(self)
                temp_model.make_wall_move(wall_type, row, col)
                moves.append(('F', (wall_type, row, col), temp_model))
        
        return moves

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