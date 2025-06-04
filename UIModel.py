import pygame
from dataclasses import dataclass

@dataclass
class Wall:
    rect: pygame.Rect
    position: str
    activated: bool
    color: pygame.Color

@dataclass
class Square:
    rect: pygame.Rect

@dataclass
class Player:
    rect: pygame.Rect
    pos: tuple
    color: pygame.Color
    square_player_ration: float
    num: int

BLACK = (0, 0, 0)
BROWN = (88, 57, 39)
GRAY = (100, 100, 100)

class UIModel:
    def __init__(self, N, M, BOARD_WIDTH, TOP_LEFT_POINT, UP_WALL_BAR_MIDDLE_LEFT_POINT, DOWN_WALL_BAR_MIDDLE_LEFT_POINT):
        self.N = N
        self.M = M
        self.BOARD_WIDTH = BOARD_WIDTH
        self.TOP_LEFT_POINT = TOP_LEFT_POINT
        self.UP_WALL_BAR_MIDDLE_LEFT_POINT = UP_WALL_BAR_MIDDLE_LEFT_POINT
        self.DOWN_WALL_BAR_MIDDLE_LEFT_POINT = DOWN_WALL_BAR_MIDDLE_LEFT_POINT

        self.player1 = None
        self.player2 = None
        self.player_move_options = []

        self.walls = []
        self.squares = []
        self.up_bar_walls = []
        self.down_bar_walls = []
        
        self.ghost_rect = None
        

        self.compute_cordinates()
        self.create_walls(3 * N -1)
        self.create_squares()
        self.create_wall_bars()
        self.create_players()

        self.bar_walls = self.up_bar_walls + self.down_bar_walls

    def compute_cordinates(self):
        self.WALL_WIDTH_COUNT = self.N * 4 + (self.N - 1) 
        self.WALL_WIDTH = self.BOARD_WIDTH / self.WALL_WIDTH_COUNT
        self.SQUARE_WIDTH = 4 * self.WALL_WIDTH
        self.WALL_HEIGHT = 9 * self.WALL_WIDTH

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

    def create_players(self):
        squrae_player_ratio = 4 / 5
        padding = (1 - squrae_player_ratio) / 2
        GREEN = (34, 139, 34)
        RED = (255, 0, 0)

        #player 1
        pos_player_1 = (0, self.N // 2)
        square1 = self.squares[pos_player_1[0]][pos_player_1[1]].rect

        circle_cordinate = (square1.x + square1.height * padding, square1.y + square1.width * padding)
        circle_width = (square1.width * squrae_player_ratio)
        circle_height = (square1.height * squrae_player_ratio)

        self.player1 = Player(pygame.Rect(circle_cordinate[0], circle_cordinate[1], circle_width, circle_height), pos_player_1, GREEN, squrae_player_ratio, 1)

        
        #player 2
        pos_player_2 = (self.N - 1, self.N // 2)
        square2 = self.squares[pos_player_2[0]][pos_player_2[1]].rect

        circle_cordinate = (square2.x + square2.height * padding, square2.y + square2.width * padding)
        circle_width = (square2.width * squrae_player_ratio)
        circle_height = (square2.height * squrae_player_ratio)

        self.player2 = Player(pygame.Rect(circle_cordinate[0], circle_cordinate[1], circle_width, circle_height), pos_player_2, RED, squrae_player_ratio, 2)

    def update_player_pos(self, pos, player):
        squrae_player_ratio = 4 / 5
        padding = (1 - squrae_player_ratio) / 2

        square = self.squares[pos[0]][pos[1]].rect

        circle_cordinate = (square.x + square.height * padding, square.y + square.width * padding)
        circle_width = (square.width * squrae_player_ratio)
        circle_height = (square.height * squrae_player_ratio)

        new_rect = pygame.Rect(circle_cordinate[0], circle_cordinate[1], circle_width, circle_height)

        player.rect = new_rect
        player.pos = pos


    def create_walls(self, WN):
        self.WN = WN
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

                    if j % 3 == 0:
                        position = "left"
                    elif j % 3 == 1:
                        position = "right"
                    else:
                        position = "center"

                    wall = Wall(rect, position, False, GRAY)
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

                        if i % 3 == 0:
                            position = "up"
                        else:
                            position = "down"

                        wall = Wall(rect, position, False, GRAY)
                        row.append(wall)
                    else: row.append(None)
                    wall_ind_x += 1
            
            wall_ind_y += 1
            self.walls.append(row)

        #if the walls are correct, we need to place the "border-..." type positions too
        for j in range(2, self.WN, 3):
            self.walls[0][j].position = "border-up"
            self.walls[self.WN-1][j].position = "border-down"

        for i in range(2, self.WN, 3):
            self.walls[i][0].position = "border-left"
            self.walls[i][self.WN-1].position = "border-right"

        #print(self.walls)

    def create_squares(self):
        for i in range(self.N):
            row = []
            for j in range(self.N):
                x = self.TOP_LEFT_POINT[0] + self.square_start_cordinates[j]
                y = self.TOP_LEFT_POINT[1] + self.square_start_cordinates[i]
                width = self.SQUARE_WIDTH
                height = self.SQUARE_WIDTH
                rect = pygame.Rect(x, y, width, height)
                square = Square(rect)
                row.append(square)
            self.squares.append(row)

        #print(self.squares)

    def create_wall_bars(self):
        
        bar_starting_x_positions = []

        SPACE_WIDTH = (self.BOARD_WIDTH - self.M * self.WALL_WIDTH) / (self.M - 1)

        current_pos = self.TOP_LEFT_POINT[0]
        for i in range(self.M):
            bar_starting_x_positions.append(current_pos)
            current_pos += (self.WALL_WIDTH + SPACE_WIDTH)

        for i in range(self.M):
            wall = Wall(pygame.Rect(bar_starting_x_positions[i], self.UP_WALL_BAR_MIDDLE_LEFT_POINT[1] - self.WALL_HEIGHT / 2, self.WALL_WIDTH, self.WALL_HEIGHT), None, True, BLACK)
            self.up_bar_walls.append(wall)
            wall = Wall(pygame.Rect(bar_starting_x_positions[i], self.DOWN_WALL_BAR_MIDDLE_LEFT_POINT[1] - self.WALL_HEIGHT / 2, self.WALL_WIDTH, self.WALL_HEIGHT), None, True, BLACK)
            self.down_bar_walls.append(wall)

    def add_player_move_options(self, cordinates):
        squrae_player_ratio = 4 / 5
        padding = (1 - squrae_player_ratio) / 2

        GRAY = (88, 88, 88)

        for cordinate in cordinates:
            square = self.squares[cordinate[0]][cordinate[1]].rect

            circle_cordinate = (square.x + square.height * padding, square.y + square.width * padding)
            circle_width = (square.width * squrae_player_ratio)
            circle_height = (square.height * squrae_player_ratio)

            self.player_move_options.append(Player(pygame.Rect(circle_cordinate[0], circle_cordinate[1], circle_width, circle_height), cordinate, GRAY, squrae_player_ratio, None))
