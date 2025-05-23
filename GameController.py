# UI class for Qouridor game
"""
The board will have two parts:
-the squares, where we can actually step
-the walls
"""

#CODES
PLAYER1 = 1
PLAYER2 = 2
EMPTY_SQUARE = 0
EMPTY_WALL = 0
WALL = 9


import pygame
from dataclasses import dataclass
from UIModel import UIModel
from GameView import GameView
from LogicModel import LogicModel

SCREEN_WIDTH = 600
BOARD_SCREEN_RATIO = 3 / 5
TOP_LEFT_RATIO = 1 / 5

class GameController:
    def __init__(self, N):
        print("I started the project")
        pygame.init()
        
        self.N = N

        self.compute_base_metrics()

        self.ui_model = UIModel(N, self.BOARD_WIDTH, self.TOP_LEFT_POINT)
        self.game_view = GameView(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        self.start_game()

    def compute_base_metrics(self):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_WIDTH

        self.BOARD_WIDTH = SCREEN_WIDTH * BOARD_SCREEN_RATIO
        
        self.BASE_ELEMENT_N = self.N * 4 + (self.N - 1)                                                       #we want a broad_with which is divisible by the base element size
        self.BASE_ELEMENT_WIDTH = self.BOARD_WIDTH // self.BASE_ELEMENT_N                           #so we will not have problems with pixels truncation
        self.BOARD_WIDTH = self.BASE_ELEMENT_N * self.BASE_ELEMENT_WIDTH

        self.BOARD_HEIGHT = self.BOARD_WIDTH

        self.TOP_LEFT_POINT = (SCREEN_WIDTH * TOP_LEFT_RATIO, SCREEN_WIDTH * TOP_LEFT_RATIO)

    def start_game(self):
        #we need to initialize the matrix as empty
        self.logic_model = LogicModel(self.N)

        #render the window
        self.show_board()
        self.run_game()

        #I need to decide who starts (I will make a random fucntion for this)
        #I should notify the user with a message

        #if bot starts
            #run_game

        #else
            #waits for a move, returns the matrix
            #run_game
        pass


    def run_game(self):
        running = True
        clock = pygame.time.Clock

        while running:
            #running = self.handle_events() #check if the window was not closed

            #sends the current matrix
            #self.update_game_state()       #returns the matrix, with the modifications of the opponent

            #transforms the matrix into ui_model

            #self.game_view.render_frame(self.ui_model)    #shows the modifications to the user

            #makes the table active, is waiting for a move, returns the matrix


            clock().tick(180)

        pygame.quit()
        pass

    def show_board(self):
        self.convert_logic_to_ui()
        self.game_view.render_frame(self.ui_model)

    def convert_logic_to_ui(self):
        SWN = 2*self.N -1

        #check if walls are activated
        for i in range(SWN):
            if i % 2 == 0:
                for j in range(1, SWN, 2):
                    if self.logic_model.matrix[i][j] == WALL:
                        #activate the neccessary walls
                        #I need to tranform the indexes
                        #ti = (i - 1) // 2 * 3 + 2
                        

                        ti = (i // 2) * 3
                        tj = (j - 1) // 2 * 3 + 2
                        #
                        self.ui_model.walls[ti][tj].activated = True
                        self.ui_model.walls[ti+1][tj].activated = True

                        print('elso', i, j, ti, tj)
                        pass
            else:
                for j in range(SWN):
                    
                    if self.logic_model.matrix[i][j] == WALL:
                        #activate the neccesary walls
                        if j % 2 == 1:
                            ti = (i - 1) // 2 * 3 + 2
                            tj = (j - 1) // 2 * 3 + 2
                            self.ui_model.walls[ti][tj].activated = True

                            print('masodik', i, j, ti, tj)
                            pass
                        else:
                            ti = (i - 1) // 2 * 3 + 2
                            tj = (j // 2) * 3
                            #tj = (j - 1) // 2 * 3 + 2
                            self.ui_model.walls[ti][tj].activated = True
                            self.ui_model.walls[ti][tj+1].activated = True

                            print('harmadik', i, j, ti, tj)

        

board = GameController(5)