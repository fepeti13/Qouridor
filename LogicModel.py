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
        
        # Track wall counts for each player
        self.player1_walls_count = M
        self.player2_walls_count = M
        
        # Legacy support (these point to player2's walls for backward compatibility)
        self.my_walls_count = M
        self.opponent_walls_count = M

    def set_player_positions(self, pos_player1, pos_player2):
        self.player1 = pos_player1
        self.player2 = pos_player2

    def get_wall_count(self, player_num):
        """Get remaining wall count for a player"""
        if player_num == 1:
            return self.player1_walls_count
        else:
            return self.player2_walls_count

    def use_wall(self, player_num):
        """Decrement wall count for a player"""
        if player_num == 1:
            if self.player1_walls_count > 0:
                self.player1_walls_count -= 1
                return True
        else:
            if self.player2_walls_count > 0:
                self.player2_walls_count -= 1
                # Update legacy counters
                self.my_walls_count -= 1
                return True
        return False

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
            print(current_pos, opponent_pos)
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

    def execute_move(self, player_num, move):
        """Execute a move for the specified player"""
        if move[0] == 'L':
            # Location move: L x y
            new_pos = (int(move[1]), int(move[2]))
            self.make_move(new_pos, player_num)
        elif move[0] == 'F':
            # Fence/Wall move: F x1 y1 x2 y2
            x1, y1, x2, y2 = int(move[1]), int(move[2]), int(move[3]), int(move[4])
            
            # Determine if it's horizontal or vertical wall
            if x1 == x2:  # Same row, so it's a horizontal wall
                wall_type = 'H'
                # For horizontal walls, use the leftmost position
                row, col = x1, min(y1, y2)
            else:  # Same column, so it's a vertical wall
                wall_type = 'V'
                # For vertical walls, use the topmost position
                row, col = min(x1, x2), y1
            
            # Check if player has walls remaining
            if self.get_wall_count(player_num) > 0:
                self.place_wall(wall_type, row, col)
                self.use_wall(player_num)
            else:
                print(f"Warning: Player {player_num} tried to place wall but has no walls remaining!")

    def make_move(self, new_pos, player_num):
        """Move a player to a new position"""
        if player_num == 1:
            old_pos = self.player1
            self.player1 = new_pos
        else:
            old_pos = self.player2
            self.player2 = new_pos

        # Clear old position and set new position in matrix
        self.matrix[old_pos[0]][old_pos[1]] = 0
        self.matrix[new_pos[0]][new_pos[1]] = player_num

    def make_wall_move(self, wall_type, row, col, player_num=2):
        """Place a wall for the specified player"""
        if self.get_wall_count(player_num) > 0:
            self.place_wall(wall_type, row, col)
            self.use_wall(player_num)
        else:
            print(f"Warning: Player {player_num} has no walls remaining!")

    def get_all_possible_moves(self):
        
        moves = []
        
        
        for pos in self.get_valid_moves(1):
            temp_model = copy.deepcopy(self)
            temp_model.make_move(pos, 1)
            moves.append(('L', pos, temp_model))
        
        
        if self.player1_walls_count > 0:
            for wall_type, row, col in self.get_valid_walls():
                temp_model = copy.deepcopy(self)
                temp_model.make_wall_move(wall_type, row, col, 1)
                moves.append(('F', (wall_type, row, col), temp_model))
        
        return moves