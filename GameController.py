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
import UIModel
import GameView

class GameController:
    def __init__(self, N):
        print("I started the project")
        pygame.init()
        
        self.N = N
        

        SCREEN_WIDTH = 600
        SCREEN_HEIGHT = SCREEN_WIDTH
        
        BOARD_SCREEN_RATIO = 3 / 5
        TOP_LEFT_RATIO = 1 / 5

        self.BOARD_WIDTH = SCREEN_WIDTH * BOARD_SCREEN_RATIO
        
        self.BASE_ELEMENT_N = N * 4 + (N - 1)                                                       #we want a broad_with which is divisible by the base element size
        self.BASE_ELEMENT_WIDTH = self.BOARD_WIDTH // self.BASE_ELEMENT_N                           #so we will not have problems with pixels truncation
        self.BOARD_WIDTH = self.BASE_ELEMENT_N * self.BASE_ELEMENT_WIDTH

        self.BOARD_HEIGHT = self.BOARD_WIDTH

        self.TOP_LEFT_POINT = (SCREEN_WIDTH * TOP_LEFT_RATIO, SCREEN_WIDTH * TOP_LEFT_RATIO)

        UIboard = UIModel(N, self.BOARD_WIDTH)
        gameView = GameView(SCREEN_WIDTH, SCREEN_HEIGHT)

        pass 

    def show_board(self):
        square_size = 60
        square_x = 100
        square_y = 100

        WHITE = (255, 255, 255)
        BLUE = (0, 120, 255)
        RED = (255, 0, 255)
        BROWN = (88, 57, 39)
        GRAY = (100, 100, 100)

        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.handle_events()

            self.update_game_state()

            self.gameView.render_frame(self.UIBoard)

            clock().tick(60)

        pygame.quit()
        pass

    def convert_input(self, matrix):
        MN = 2*self.N -1

        #check if walls are activated
        for i in range(MN):
            if i % 2 == 0:
                for j in range(0, MN, 2):
                    if matrix[i][j] == WALL:
                        #activate the neccessary walls
            else:
                for j in range(MN):
                    if matrix[i][j] == WALL:
                        #activate the neccesary walls

        

board = GameController(5)