import pygame
from dataclasses import dataclass

@dataclass
class Wall:
    rect: pygame.Rect
    position: str

@dataclass
class Square:
    rect: pygame.Rect

class UIModel:
    def __init__(self, N, BOARD_WIDTH):
        self.N = N
        self.BOARD_WIDTH = BOARD_WIDTH

        self.compute_cordinates()
        self.create_walls()
        self.create_squares()

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