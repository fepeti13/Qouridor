import pygame

class GameView:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quoridor Starter")

    def render_frame(self, ui_model):

        WHITE = (255, 255, 255)
        BLUE = (0, 120, 255)
        RED = (255, 0, 255)
        BROWN = (88, 57, 39)
        GRAY = (100, 100, 100)

        self.screen.fill(WHITE)
        for i in range(3*ui_model.N - 1):
            for j in range(3*ui_model.N - 1):
                if ui_model.walls[i][j] != None:
                    if ui_model.walls[i][j].activated == True:
                        pygame.draw.rect(self.screen, BLUE, ui_model.walls[i][j].rect)
                    else:
                        pygame.draw.rect(self.screen, GRAY, ui_model.walls[i][j].rect)

        for i in range(ui_model.N):
            for j in range(ui_model.N):
                pygame.draw.rect(self.screen, BROWN, ui_model.squares[i][j].rect)

        pygame.display.flip()

        pass