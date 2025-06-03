# GameController.py - Fixed version
import pygame
from UIModel import UIModel
from GameView import GameView
from LogicModel import LogicModel
from LogicController import LogicController
import copy

#CODES
PLAYER1 = 1
PLAYER2 = 2
EMPTY_SQUARE = 0
EMPTY_WALL = 0
WALL = 9

SCREEN_WIDTH = 600
BOARD_SCREEN_RATIO = 3 / 5
TOP_LEFT_RATIO = 1 / 5

class GameController:
    def __init__(self, N):
        print("Starting Quoridor Game")
        pygame.init()
        
        self.N = N
        self.current_player = 1  # 1 human, 2 BOT
        self.game_over = False
        self.winner = None

        # Drag and drop state
        self.dragging_wall = False
        self.drag_start_pos = None
        self.drag_wall_type = None
        self.drag_wall_rect = None
        self.hover_preview = None

        self.compute_base_metrics()

        # Initialize UI components
        self.ui_model = UIModel(N, self.BOARD_WIDTH, self.TOP_LEFT_POINT)
        self.game_view = GameView(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Initialize game logic
        self.logic_model = LogicModel(N, 10)  # N x N board, 10 walls each
        self.logic_controller = LogicController()
        
        self.start_game()

    def compute_base_metrics(self):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_WIDTH
        self.BOARD_WIDTH = SCREEN_WIDTH * BOARD_SCREEN_RATIO
        
        self.BASE_ELEMENT_N = self.N * 4 + (self.N - 1)
        self.BASE_ELEMENT_WIDTH = self.BOARD_WIDTH // self.BASE_ELEMENT_N
        self.BOARD_WIDTH = self.BASE_ELEMENT_N * self.BASE_ELEMENT_WIDTH
        self.BOARD_HEIGHT = self.BOARD_WIDTH
        self.TOP_LEFT_POINT = (SCREEN_WIDTH * TOP_LEFT_RATIO, SCREEN_WIDTH * TOP_LEFT_RATIO)

    def start_game(self):
        # Set initial player positions
        self.logic_model.player1 = (0, self.N-1)  # Top center
        self.logic_model.player2 = (self.logic_model.SWN-1, self.N-1)  # Bottom center
        
        # Update matrix with player positions
        self.logic_model.matrix[self.logic_model.player1[0]][self.logic_model.player1[1]] = 1
        self.logic_model.matrix[self.logic_model.player2[0]][self.logic_model.player2[1]] = 2
        
        # Update logic controller with our model
        self.logic_controller.logic_model = self.logic_model
        
        self.run_game()

    def run_game(self):
        running = True
        clock = pygame.time.Clock()

        while running and not self.game_over:
            running = self.handle_events()
            
            # Check for game over
            winner = self.logic_model.is_game_over()
            if winner != 0:
                self.game_over = True
                self.winner = winner
                break
            
            # AI turn
            if self.current_player == 2 and not self.game_over:
                self.make_bot_move()
            
            self.update_display()
            clock.tick(60)

        # Show game over screen
        if self.game_over:
            self.show_game_over()
            
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.current_player == 1:  # Human player turn
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_down(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.handle_mouse_up(event.pos)
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.end_turn()
        
        return True

    def handle_mouse_down(self, pos):
        # Try to move player first
        square_clicked = self.get_square_at_pos(pos)
        if square_clicked:
            if self.try_move_player(square_clicked):
                return
        
        # If not moving, try to start wall drag
        if self.logic_model.my_walls_count > 0:
            wall_area = self.get_wall_drag_area(pos)
            if wall_area:
                self.start_wall_drag(pos, wall_area)

    def handle_mouse_up(self, pos):
        if self.dragging_wall:
            self.try_place_wall(pos)
            self.stop_wall_drag()

    def handle_mouse_motion(self, pos):
        if self.dragging_wall:
            self.update_wall_drag(pos)
        else:
            self.update_wall_preview(pos)

    def get_square_at_pos(self, pos):
        """Get the logical square coordinates from mouse position"""
        for i in range(self.N):
            for j in range(self.N):
                if self.ui_model.squares[i][j].rect.collidepoint(pos):
                    # Convert UI coordinates to logic coordinates
                    logic_row = i * 2
                    logic_col = j * 2
                    return (logic_row, logic_col)
        return None

    def get_wall_drag_area(self, pos):
        """Check if position is in a wall drag area"""
        board_rect = pygame.Rect(self.TOP_LEFT_POINT[0], self.TOP_LEFT_POINT[1], 
                                self.BOARD_WIDTH, self.BOARD_HEIGHT)
        if board_rect.collidepoint(pos):
            return "board"
        return None

    def start_wall_drag(self, pos, area):
        """Start dragging a wall"""
        self.dragging_wall = True
        self.drag_start_pos = pos
        self.drag_wall_rect = pygame.Rect(pos[0]-25, pos[1]-5, 50, 10)
        self.drag_wall_type = 'H'

    def update_wall_drag(self, pos):
        """Update wall position during drag"""
        if self.drag_wall_rect:
            dx = pos[0] - self.drag_start_pos[0]
            dy = pos[1] - self.drag_start_pos[1]
            
            if abs(dx) > abs(dy):
                # Horizontal wall
                self.drag_wall_type = 'H'
                self.drag_wall_rect = pygame.Rect(pos[0]-25, pos[1]-5, 50, 10)
            else:
                # Vertical wall
                self.drag_wall_type = 'V'
                self.drag_wall_rect = pygame.Rect(pos[0]-5, pos[1]-25, 10, 50)

    def try_place_wall(self, pos):
        """Try to place wall at the given position"""
        wall_position = self.get_wall_logic_position(pos)
        if wall_position:
            wall_type, row, col = wall_position
            if self.logic_model.can_place_wall(wall_type, row, col):
                self.logic_model.place_wall(wall_type, row, col)
                self.logic_model.my_walls_count -= 1
                self.end_turn()
                return True
        return False

    def get_wall_logic_position(self, pos):
        """Convert mouse position to logic wall coordinates"""
        rel_x = pos[0] - self.TOP_LEFT_POINT[0]
        rel_y = pos[1] - self.TOP_LEFT_POINT[1]
        
        if rel_x < 0 or rel_y < 0 or rel_x > self.BOARD_WIDTH or rel_y > self.BOARD_HEIGHT:
            return None
        
        cell_size = self.BOARD_WIDTH / (self.N * 2 - 1)
        grid_x = int(rel_x / cell_size)
        grid_y = int(rel_y / cell_size)
        
        if self.drag_wall_type == 'H':
            if grid_y % 2 == 1 and grid_x % 2 == 0 and grid_x < self.logic_model.SWN - 2:
                return ('H', grid_y, grid_x)
        else:
            if grid_x % 2 == 1 and grid_y % 2 == 0 and grid_y < self.logic_model.SWN - 2:
                return ('V', grid_y, grid_x)
        
        return None

    def stop_wall_drag(self):
        """Stop wall dragging"""
        self.dragging_wall = False
        self.drag_start_pos = None
        self.drag_wall_rect = None
        self.drag_wall_type = None

    def update_wall_preview(self, pos):
        """Show preview of wall placement"""
        pass

    def try_move_player(self, target_square):
        """Try to move the player to target square"""
        valid_moves = self.logic_model.get_valid_moves(1)
        if target_square in valid_moves:
            old_pos = self.logic_model.player1
            self.logic_model.matrix[old_pos[0]][old_pos[1]] = 0
            self.logic_model.player1 = target_square
            self.logic_model.matrix[target_square[0]][target_square[1]] = 1
            self.end_turn()
            return True
        return False

    def make_bot_move(self):
        """Make AI move using LogicController"""
        best_move = self.logic_controller.find_best_move()
        if best_move:
            move_type, move_data = best_move
            
            if move_type == 'L':
                # AI pawn move
                new_pos = move_data
                old_pos = self.logic_model.player2
                self.logic_model.matrix[old_pos[0]][old_pos[1]] = 0
                self.logic_model.player2 = new_pos
                self.logic_model.matrix[new_pos[0]][new_pos[1]] = 2
            
            elif move_type == 'F':
                # AI wall placement
                wall_type, row, col = move_data
                self.logic_model.place_wall(wall_type, row, col)
                self.logic_model.opponent_walls_count -= 1
        
        self.end_turn()

    def end_turn(self):
        """End current player's turn"""
        self.current_player = 2 if self.current_player == 1 else 1

    def update_display(self):
        """Update the display"""
        self.convert_logic_to_ui()
        self.game_view.render_frame(self.ui_model, self.drag_wall_rect, self.drag_wall_type, 
                                   self.current_player, self.logic_model.my_walls_count, 
                                   self.logic_model.opponent_walls_count)

    def convert_logic_to_ui(self):
        """Convert logic model to UI model - Fixed version"""
        SWN = 2 * self.N - 1

        # Reset all walls first
        for i in range(3 * self.N - 1):
            for j in range(3 * self.N - 1):
                if self.ui_model.walls[i][j] is not None:
                    self.ui_model.walls[i][j].activated = False

        # Convert logic walls to UI walls
        for i in range(SWN):
            if i % 2 == 0:  # Even rows - horizontal walls
                for j in range(1, SWN, 2):  # Odd columns
                    if self.logic_model.matrix[i][j] == WALL:
                        ti = (i // 2) * 3
                        tj = (j - 1) // 2 * 3 + 2
                        if (ti < len(self.ui_model.walls) and tj < len(self.ui_model.walls[ti]) and
                            self.ui_model.walls[ti][tj] is not None):
                            self.ui_model.walls[ti][tj].activated = True
                        if (ti + 1 < len(self.ui_model.walls) and tj < len(self.ui_model.walls[ti+1]) and
                            self.ui_model.walls[ti+1][tj] is not None):
                            self.ui_model.walls[ti+1][tj].activated = True
            else:  # Odd rows - vertical walls
                for j in range(SWN):
                    if self.logic_model.matrix[i][j] == WALL:
                        if j % 2 == 1:  # Odd column
                            ti = (i - 1) // 2 * 3 + 2
                            tj = (j - 1) // 2 * 3 + 2
                            if (ti < len(self.ui_model.walls) and tj < len(self.ui_model.walls[ti]) and
                                self.ui_model.walls[ti][tj] is not None):
                                self.ui_model.walls[ti][tj].activated = True
                        else:  # Even column
                            ti = (i - 1) // 2 * 3 + 2
                            tj = (j // 2) * 3
                            if (ti < len(self.ui_model.walls) and tj < len(self.ui_model.walls[ti]) and
                                self.ui_model.walls[ti][tj] is not None):
                                self.ui_model.walls[ti][tj].activated = True
                            if (tj + 1 < len(self.ui_model.walls[ti]) and
                                self.ui_model.walls[ti][tj+1] is not None):
                                self.ui_model.walls[ti][tj+1].activated = True

        # Update player positions for UI
        self.ui_model.player1_pos = self.convert_logic_to_ui_pos(self.logic_model.player1)
        self.ui_model.player2_pos = self.convert_logic_to_ui_pos(self.logic_model.player2)

    def convert_logic_to_ui_pos(self, logic_pos):
        """Convert logic position to UI square indices"""
        return (logic_pos[0] // 2, logic_pos[1] // 2)

    def show_game_over(self):
        """Show game over screen"""
        font = pygame.font.Font(None, 74)
        if self.winner == 1:
            text = font.render("You Win!", True, (0, 255, 0))
        else:
            text = font.render("AI Wins!", True, (255, 0, 0))
        
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
        self.game_view.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)