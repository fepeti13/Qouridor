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
SCREEN_HEIGHT = 600
BOARD_SCREEN_RATIO_WIDTH = 3 / 5

class UIController:
    def __init__(self, N, M):
        print("I started the project")
        pygame.init()
        
        self.N = N
        self.M = M

        self.compute_base_metrics()

        self.ui_model = UIModel(N, M, self.BOARD_WIDTH, self.TOP_LEFT_POINT,
                                self.UP_WALL_BAR_MIDDLE_LEFT_POINT, self.DOWN_WALL_BAR_MIDDLE_LEFT_POINT)
        self.game_view = GameView(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        self.start_game()

    def compute_base_metrics(self):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        #how many walls do I need to have vertically
        wall_count = 2 + self.N / 2
        buffer_space = 100
        WALL_HEIGHT = int((SCREEN_HEIGHT - buffer_space) / wall_count)

        self.BOARD_WIDTH = (self.N / 2) * WALL_HEIGHT

        self.BASE_ELEMENT_N = self.N * 4 + (self.N - 1)                                                       #we want a broad_with which is divisible by the base element size
        self.BASE_ELEMENT_WIDTH = self.BOARD_WIDTH // self.BASE_ELEMENT_N                           #so we will not have problems with pixels truncation
        self.BOARD_WIDTH = self.BASE_ELEMENT_N * self.BASE_ELEMENT_WIDTH

        self.BOARD_HEIGHT = self.BOARD_WIDTH

        self.TOP_LEFT_POINT = (WALL_HEIGHT + (buffer_space / 2), WALL_HEIGHT + (buffer_space / 2))

        self.UP_WALL_BAR_MIDDLE_LEFT_POINT = (self.TOP_LEFT_POINT[0], self.TOP_LEFT_POINT[1] / 2)
        self.DOWN_WALL_BAR_MIDDLE_LEFT_POINT = (self.TOP_LEFT_POINT[0], self.TOP_LEFT_POINT[1] + self.BOARD_WIDTH + self.TOP_LEFT_POINT[1] / 2)

    def start_game(self):
        #we need to initialize the matrix as empty
        self.logic_model = LogicModel(self.N, self.M)
        player1_pos, player2_pos = self.square_cordinates_ui_to_logic([self.ui_model.player1.pos, self.ui_model.player2.pos])
        self.logic_model.set_player_positions(player1_pos, player2_pos)

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
        clock = pygame.time.Clock()


        self.dragging = False
        self.dragged_rect = None
        self.drag_offset = None

        self.screen = self.game_view.render_frame(self.ui_model)

        while running:
            #running = self.handle_events() #check if the window was not closed

            self.make_a_move()

            #sends the current matrix
            #self.update_game_state()       #returns the matrix, with the modifications of the opponent

            #transforms the matrix into ui_model

            #self.game_view.render_frame(self.ui_model)    #shows the modifications to the user

            #makes the table active, is waiting for a move, returns the matrix


            clock.tick(180)

        pygame.quit()
        pass

    def make_a_move(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                player_moved_in_this_round = False


                #if move option was pressed
                print(self.ui_model.player_move_options)
                for option in self.ui_model.player_move_options:
                    if option.rect.collidepoint(mouse_pos):
                        print("Option at pos was pressed", option.pos)
                        new_player_pos = self.square_cordinates_ui_to_logic([option.pos])[0]
                        self.logic_model.make_move(new_player_pos, self.ui_model.player1.num)
                        
                        self.ui_model.update_player_pos(option.pos, self.ui_model.player1)
                        player_moved_in_this_round = True

                #reset the components
                self.ui_model.player_move_options = []


                #if a player was pressed
                if self.ui_model.player1.rect.collidepoint(mouse_pos) and not player_moved_in_this_round:
                    
                    cordinates = self.logic_model.get_valid_moves(self.ui_model.player1.num)
                    cordinates = self.square_cordinates_logic_to_ui(cordinates)
                    self.ui_model.add_player_move_options(cordinates)
                        

                #if a wall is picked up
                for wall in self.ui_model.bar_walls:
                    if wall.rect.collidepoint(mouse_pos):
                        self.dragging = True
                        self.dragged_rect = wall
                        self.dragged_rect.activated = False
                        self.drag_offset = (mouse_pos[0] - wall.rect.x, mouse_pos[1] - wall.rect.y)
                        print("Mouse was pressed on:", wall.rect)
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    print("Mouse was release")
                    self.dragged_rect.activated = True
                    # On drop: find which rect we're over and change its color
                    for i in range(self.ui_model.WN):
                        for j in range(self.ui_model.WN):
                            wall = self.ui_model.walls[i][j]
                            if wall is not None and wall.rect.collidepoint(mouse_pos):
                                cordinates = self.get_full_wall_location(i, j)
                                if cordinates != None:
                                    for x, y in cordinates:
                                        self.ui_model.walls[x][y].color = (0, 255, 0)
                                    self.dragged_rect.activated = False
                                    
                                
                                print("Mouse was released on:", wall.rect, i, j)
                    self.dragged_rect = None
                    self.dragging = False
                    self.ui_model.ghost_rect = None
                    

        

        # Draw dragged rect on top following mouse
        if self.dragging and self.dragged_rect:
            self.ui_model.ghost_rect = self.dragged_rect.rect.copy()
            self.ui_model.ghost_rect.topleft = (mouse_pos[0] - self.drag_offset[0], mouse_pos[1] - self.drag_offset[1])

        self.screen = self.game_view.render_frame(self.ui_model)

    def square_cordinates_logic_to_ui(self, cordinates):
        new_cordinates = []
        for cordinate in cordinates:
            new_cordinates.append((cordinate[0]//2, cordinate[1]//2))

        return new_cordinates

    def square_cordinates_ui_to_logic(self, cordinates):
        new_cordinates = []
        for cordinate in cordinates:
            new_cordinates.append((int(cordinate[0] * 2), int(cordinate[1] * 2)))

        return new_cordinates

    def get_full_wall_location(self, i, j):
        wall = self.ui_model.walls[i][j]
        if wall.position == "border-down":
            cordinates = [(i - 4, j), (i - 3, j), (i - 2, j), (i - 1, j), (i, j)]
        elif wall.position == "border-up":
            cordinates = [(i, j), (i + 1, j), (i + 2, j), (i + 3, j), (i + 4, j)]
        elif wall.position == "border-right":
            cordinates = [(i, j - 4), (i, j - 3), (i, j - 2), (i, j - 1), (i, j)]
        elif wall.position == "border-left":
            cordinates = [(i, j), (i, j + 1), (i, j + 2), (i, j + 3), (i, j + 4)]
        elif wall.position == "up":
            cordinates = [(i - 3, j), (i - 2, j), (i-1, j), (i, j), (i + 1, j)]
        elif wall.position == "down":
            cordinates = [(i - 1, j), (i, j), (i + 1, j), (i + 2, j), (i + 3, j)]
        elif wall.position == "left":
            cordinates = [(i, j - 3), (i, j - 2), (i, j - 1), (i, j), (i, j + 1)]
        elif wall.position == "right":
            cordinates = [(i, j - 1), (i, j), (i, j + 1), (i, j + 2), (i, j + 3)]
        elif wall.position == "center":
            cordinates = [(i - 2, j), (i - 1, j), (i, j), (i + 1, j), (i + 2, j)]

        if self.check_cordinates(cordinates):
            return cordinates
        return None

    def check_cordinates(self, cordinates):
        #the cordinates are given in the ui_model system, we need to convert them back to the logical_model
        #for that I will use always the left and upper part of each wall pair(from the UI model)
        #so we need always need the first, third, and fourth elements of the cordinates and convert those back

        checkable_cordinats = cordinates[0], cordinates[2], cordinates[3]

        for cordinate in checkable_cordinats:
            x = int(cordinate[0] / 1.5)
            y = int(cordinate[1] / 1.5)
            print("Checked location:", x, y)
            if self.logic_model.matrix[x][y] == WALL:
                return False

        return True

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

        

board = UIController(5, 10)