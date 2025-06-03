import copy
from collections import deque
import sys

class LogicModel:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.SWN = 2 * N - 1
        
        # Initialize empty matrix
        self.matrix = []
        for i in range(self.SWN):
            row = [0] * self.SWN
            self.matrix.append(row)

        # Player positions will be set when reading input
        self.player1 = None  # My player
        self.player2 = None  # Opponent
        
        # Wall counts
        self.my_walls_count = M
        self.opponent_walls_count = M

    def read_initial_input(self):
        line = input().strip().split()
        N, M = int(line[0]), int(line[1])
        self.__init__(N, M)
        
        for i in range(self.SWN):
            row = list(map(int, input().strip().split()))
            self.matrix[i] = row
            
            # Find player positions
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
            
            # Update player positions
            for j in range(self.SWN):
                if row[j] == 1:
                    self.player1 = (i, j)
                elif row[j] == 2:
                    self.player2 = (i, j)
        
        # Read remaining walls count
        self.my_walls_count = int(input().strip())
        
        return opponent_move

    def is_valid_position(self, row, col):
        """Check if position is within board bounds and on a valid square"""
        return (0 <= row < self.SWN and 0 <= col < self.SWN and 
                row % 2 == 0 and col % 2 == 0)

    def is_wall_between(self, pos1, pos2):
        """Check if there's a wall between two adjacent positions"""
        r1, c1 = pos1
        r2, c2 = pos2
        
        # Calculate wall position (midpoint between the two positions)
        wall_r = (r1 + r2) // 2
        wall_c = (c1 + c2) // 2
        
        return self.matrix[wall_r][wall_c] == 9

    def get_valid_moves(self, player_num):
        """Get all valid moves for a player (including jumps)"""
        if player_num == 1:
            current_pos = self.player1
            opponent_pos = self.player2
        else:
            current_pos = self.player2
            opponent_pos = self.player1
        
        valid_moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # up, down, left, right
        
        for dr, dc in directions:
            new_r = current_pos[0] + dr
            new_c = current_pos[1] + dc
            
            # Check if new position is valid
            if not self.is_valid_position(new_r, new_c):
                continue
            
            # Check if there's a wall blocking the move
            if self.is_wall_between(current_pos, (new_r, new_c)):
                continue
            
            # If opponent is in the way, try to jump
            if (new_r, new_c) == opponent_pos:
                # Try to jump over opponent
                jump_r = new_r + dr
                jump_c = new_c + dc
                # If straight jump is possible
                if (self.is_valid_position(jump_r, jump_c) and 
                    not self.is_wall_between((new_r, new_c), (jump_r, jump_c))):
                    valid_moves.append((jump_r, jump_c))
                else:
                    # Try diagonal jumps if straight jump is blocked
                    side_directions = [(0, -2), (0, 2)] if dr != 0 else [(-2, 0), (2, 0)]
                    for side_dr, side_dc in side_directions:
                        diag_r, diag_c = new_r + side_dr, new_c + side_dc
                        if (self.is_valid_position(diag_r, diag_c) and 
                            not self.is_wall_between((new_r, new_c), (diag_r, diag_c))):
                            valid_moves.append((diag_r, diag_c))
            else:
                # Normal move
                valid_moves.append((new_r, new_c))
        
        return valid_moves

    def get_valid_walls(self):
        """Get all valid wall placements"""
        valid_walls = []
        
        # Check horizontal walls
        for i in range(1, self.SWN, 2):
            for j in range(0, self.SWN-2, 2):
                if (self.matrix[i][j] == 0 and self.matrix[i][j+1] == 0 and 
                    self.matrix[i][j+2] == 0):
                    if self.can_place_wall('H', i, j):
                        valid_walls.append(('H', i, j))
        
        # Check vertical walls  
        for i in range(0, self.SWN-2, 2):
            for j in range(1, self.SWN, 2):
                if (self.matrix[i][j] == 0 and self.matrix[i+1][j] == 0 and 
                    self.matrix[i+2][j] == 0):
                    if self.can_place_wall('V', i, j):
                        valid_walls.append(('V', i, j))
        
        return valid_walls

    def can_place_wall(self, wall_type, row, col):
        """Check if a wall can be placed without blocking all paths"""
        # Create temporary copy to test if wall blocks any player's path
        temp_model = copy.deepcopy(self)
        temp_model.place_wall(wall_type, row, col)
        
        # Check if both players still have a path to their goal
        return (temp_model.has_path_to_goal(1) and temp_model.has_path_to_goal(2))

    def place_wall(self, wall_type, row, col):
        """Place a wall on the board"""
        if wall_type == 'H':  # Horizontal wall
            self.matrix[row][col] = 9
            self.matrix[row][col+1] = 9
            self.matrix[row][col+2] = 9
        else:  # Vertical wall
            self.matrix[row][col] = 9
            self.matrix[row+1][col] = 9
            self.matrix[row+2][col] = 9

    def has_path_to_goal(self, player_num):
        """Check if player has a path to their goal using BFS"""
        if player_num == 1:
            start = self.player1
            # Player 1 goal: reach the opposite side from where they started
            if self.player1[0] <= self.SWN // 2:
                goal_condition = lambda pos: pos[0] == self.SWN - 1  # Reach bottom
            else:
                goal_condition = lambda pos: pos[0] == 0  # Reach top
        else:
            start = self.player2
            # Player 2 goal: reach the opposite side from where they started
            if self.player2[0] <= self.SWN // 2:
                goal_condition = lambda pos: pos[0] == self.SWN - 1  # Reach bottom
            else:
                goal_condition = lambda pos: pos[0] == 0  # Reach top
        
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            current_pos = queue.popleft()
            
            if goal_condition(current_pos):
                return True
            
            # Check all adjacent positions
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
        """Calculate shortest path distance to goal using BFS"""
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
        
        return float('inf')  # No path found

    def is_game_over(self):
        """Check if the game is over"""
        # Check if player 1 reached their goal
        if self.player1[0] <= self.SWN // 2:
            if self.player1[0] == self.SWN - 1:
                return 1
        else:
            if self.player1[0] == 0:
                return 1
        
        # Check if player 2 reached their goal  
        if self.player2[0] <= self.SWN // 2:
            if self.player2[0] == self.SWN - 1:
                return 2
        else:
            if self.player2[0] == 0:
                return 2
        
        return 0

    def evaluate_position(self):
        """Evaluate the board position for player 1 (0 to 1, higher is better for player 1)"""
        game_result = self.is_game_over()
        if game_result == 1:
            return 1.0
        elif game_result == 2:
            return 0.0
        
        # Calculate shortest path distances
        player1_distance = self.shortest_path_to_goal(1)
        player2_distance = self.shortest_path_to_goal(2)
        
        if player1_distance == float('inf'):
            return 0.0
        if player2_distance == float('inf'):
            return 1.0
        
        # Higher score if player 1 is closer to goal relative to player 2
        total_distance = player1_distance + player2_distance
        if total_distance == 0:
            return 0.5
        
        return 1.0 - (player1_distance / total_distance)

    def make_move(self, new_pos):
        """Move player 1 to a new position"""
        # Clear old position
        self.matrix[self.player1[0]][self.player1[1]] = 0
        
        # Set new position
        self.player1 = new_pos
        self.matrix[new_pos[0]][new_pos[1]] = 1

    def make_wall_move(self, wall_type, row, col):
        """Place a wall"""
        self.place_wall(wall_type, row, col)
        self.my_walls_count -= 1

    def get_all_possible_moves(self):
        """Get all possible moves (pawn moves + wall placements)"""
        moves = []
        
        # Get pawn moves
        for pos in self.get_valid_moves(1):
            temp_model = copy.deepcopy(self)
            temp_model.make_move(pos)
            moves.append(('L', pos, temp_model))
        
        # Get wall moves if we have walls left
        if self.my_walls_count > 0:
            for wall_type, row, col in self.get_valid_walls():
                temp_model = copy.deepcopy(self)
                temp_model.make_wall_move(wall_type, row, col)
                moves.append(('F', (wall_type, row, col), temp_model))
        
        return moves