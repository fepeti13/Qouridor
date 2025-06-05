import pygame
from UIController import UIController
from LogicModel import LogicModel
from BotEngine import BotEngine
from Constants import *

class GameController:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        
        # Initialize UI Controller
        self.ui_controller = UIController(N, M)
        
        # Initialize Logic Model
        self.logic_model = LogicModel(N, M)
        
        # Set initial player positions
        player1_pos, player2_pos = self.ui_controller.square_cordinates_ui_to_logic([
            self.ui_controller.ui_model.player1.pos, 
            self.ui_controller.ui_model.player2.pos
        ])
        self.logic_model.set_player_positions(player1_pos, player2_pos)
        
        # Initialize Bot Engine
        self.bot_engine = BotEngine(self.logic_model)
        
        # Pass references to UI Controller
        self.ui_controller.set_game_dependencies(self.logic_model, self.bot_engine)
        
        self.active_player = PLAYER2
        
    def start_game(self):
        """Initialize and start the game"""
        # Show initial board
        self.ui_controller.show_board()
        
        # Start main game loop
        self.run_game()
    
    def run_game(self):
        """Main game loop"""
        running = True
        clock = pygame.time.Clock()
        
        # Initialize UI for game loop
        self.ui_controller.initialize_game_loop()
        
        while running:
            # Check for quit command
            
            if not running:
                break
                
            # Handle moves based on active player
            if self.active_player == PLAYER1:
                running, move_completed = self.handle_UI_move()
                if move_completed:
                    self.active_player = PLAYER2
            else:
                self.handle_bot_move()
                self.active_player = PLAYER1
            
            # Render the frame
            self.ui_controller.render_frame()
            
            clock.tick(180)
        
        pygame.quit()
    
    def handle_UI_move(self):
        """Handle human player move, returns True if move was completed"""
        return self.ui_controller.handle_UI_move()
    
    def handle_bot_move(self):
        """Handle bot player move"""
        print("Bot is making a move")
        move = self.bot_engine.make_a_move()
        print(move)
        
        # Apply move to logic model
        # TODO: Parse and apply the move to both logic and UI models
        self.logic_model.execute_move(PLAYER2, move)
        self.ui_controller.convert_logic_to_ui()
        
        # Update UI model based on the move
        # TODO: Update UI model to reflect the bot's move

if __name__ == "__main__":
    # Create and start the game
    game = GameController(5, 10)
    game.start_game()