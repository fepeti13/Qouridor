import pygame

class GameView:
    def __init__(self, SCREEN_WIDTH, SCREEEN_HEIGTH):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quoridor Starter")

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.screen, color, rect)

    def render_frame(self, ui_model):

        WHITE = (255, 255, 255)
        BLUE = (0, 120, 255)
        RED = (255, 0, 255)
        BROWN = (88, 57, 39)
        GRAY = (100, 100, 100)

        self.screen.fill(WHITE)
        for i in range(3*self.N - 1):
            for j in range(3*self.N - 1):
                if self.walls[i][j] != None:
                    pygame.draw.rect(self.screen, GRAY, self.ui_model.walls[i][j].rect)

        for i in range(self.N):
            for j in range(self.N):
                pygame.draw.rect(self.screen, BROWN, self.ui_model.squares[i][j].rect)

        pygame.display.flip()

        pass