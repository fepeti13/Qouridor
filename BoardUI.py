# UI class for Qouridor game
"""
The board will have two parts:
-the squares, where we can actually step
-the walls
"""


import pygame
from dataclasses import dataclass

@dataclass
class Wall:
    rect: pygame.Rect
    position: str

@dataclass
class Square:
    rect: pygame.Rect

class BoardUI:
    def __init__(self, N):
        print("I started the project")
        pygame.init()
        
        self.N = N

        SCREEN_WIDTH = 600
        SCREEN_HEIGHT = SCREEN_WIDTH
        
        BOARD_SCREEN_RATIO = 3 / 5
        TOP_LEFT_RATIO = 1 / 5

        self.BOARD_WIDTH = SCREEN_WIDTH * BOARD_SCREEN_RATIO
        self.BOARD_HEIGHT = self.BOARD_WIDTH
        self.TOP_LEFT_POINT = (SCREEN_WIDTH * TOP_LEFT_RATIO, SCREEN_WIDTH * TOP_LEFT_RATIO)

        #BLUE = (0, 120, 255)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quoridor Starter")

        #pygame.draw.rect(self.screen, BLUE, (self.TOP_LEFT_POINT[0], self.TOP_LEFT_POINT[1], self.BOARD_HEIGHT, self.BOARD_WIDTH))

        self.compute_cordinates()
        self.create_board(N)
        self.show_board()
        pass 

    def compute_cordinates(self):
        self.WALL_WIDTH_COUNT = self.N * 4 + (self.N - 1) 
        self.WALL_WIDTH = self.BOARD_WIDTH / self.WALL_WIDTH_COUNT
        self.SQUARE_WIDTH = 4 * self.WALL_WIDTH

        self.wall_start_cordinates = []
        current_reference_point = 0
        for i in range(self.N - 1):
            self.wall_start_cordinates.append(current_reference_point)
            self.wall_start_cordinates.append(current_reference_point + 2 * self.WALL_WIDTH)
            self.wall_start_cordinates.append(current_reference_point + 4 * self.WALL_WIDTH)
            current_reference_point += 5 * self.WALL_WIDTH

        self.wall_start_cordinates.append(current_reference_point )
        self.wall_start_cordinates.append(current_reference_point + 2 * self.WALL_WIDTH)

        #print(self.wall_start_cordinates)

        self.square_start_cordinates = []
        current_reference_point = 0
        for i in range(self.N):
            self.square_start_cordinates.append(current_reference_point)
            current_reference_point += 5 * self.WALL_WIDTH

        #print(self.square_start_cordinates)

        self.wall_widths = []
        for i in range(self.N-1):
            self.wall_widths.append(2 * self.WALL_WIDTH)
            self.wall_widths.append(2 * self.WALL_WIDTH)
            self.wall_widths.append(self.WALL_WIDTH)

        self.wall_widths.append(2 * self.WALL_WIDTH)
        self.wall_widths.append(2 * self.WALL_WIDTH)



    def create_walls(self, WN):
        
        self.walls = []
        
        wall_ind_y = 0
        for i in range(WN):
            row = []
            if i % 3 == 2:
                wall_ind_x = 0

                for j in range(WN):
                    x = self.TOP_LEFT_POINT[0] + self.wall_start_cordinates[wall_ind_x]
                    y = self.TOP_LEFT_POINT[1] + self.wall_start_cordinates[wall_ind_y]
                    width = self.wall_widths[wall_ind_x]
                    height = self.WALL_WIDTH
                    rect = pygame.Rect(x, y, width, height)
                    wall = Wall(rect, "border-up")
                    row.append(wall)

                    wall_ind_x += 1
            else:
                wall_ind_x = 0

                for j in range(WN):
                    if j % 3 == 2:
                        x = self.TOP_LEFT_POINT[0] + self.wall_start_cordinates[wall_ind_x]
                        y = self.TOP_LEFT_POINT[1] + self.wall_start_cordinates[wall_ind_y]
                        width = self.WALL_WIDTH
                        height = 2 * self.WALL_WIDTH
                        rect = pygame.Rect(x, y, width, height)
                        wall = Wall(rect, "border-up")
                        row.append(wall)
                    else: row.append(None)
                    wall_ind_x += 1
            
            wall_ind_y += 1
            self.walls.append(row)

        #print(self.walls)

    def create_squares(self):
        self.squares = []

        for i in range(self.N):
            row = []
            for j in range(self.N):
                x = self.TOP_LEFT_POINT[0] + self.square_start_cordinates[i]
                y = self.TOP_LEFT_POINT[1] + self.square_start_cordinates[j]
                width = self.SQUARE_WIDTH
                height = self.SQUARE_WIDTH
                rect = pygame.Rect(x, y, width, height)
                square = Square(rect)
                row.append(square)
            self.squares.append(row)

        print(self.squares)

    def create_board(self, N):
        
        self.create_walls(3*N - 1)
        self.create_squares()

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
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(WHITE)
            for i in range(3*self.N - 1):
                for j in range(3*self.N - 1):
                    if self.walls[i][j] != None:
                        pygame.draw.rect(self.screen, GRAY, self.walls[i][j].rect)

            for i in range(self.N):
                for j in range(self.N):
                    pygame.draw.rect(self.screen, BROWN, self.squares[i][j].rect)

            pygame.display.flip()
            pygame.time.Clock().tick(60)


        pygame.quit()
        pass

board = BoardUI(5)