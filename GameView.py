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
                        pygame.draw.rect(self.screen, ui_model.walls[i][j].color, ui_model.walls[i][j].rect)
                    else:
                        pygame.draw.rect(self.screen, ui_model.walls[i][j].color, ui_model.walls[i][j].rect)

        for i in range(ui_model.N):
            for j in range(ui_model.N):
                pygame.draw.rect(self.screen, BROWN, ui_model.squares[i][j].rect)

        pygame.draw.ellipse(self.screen, ui_model.player1.color, ui_model.player1.rect)
        pygame.draw.ellipse(self.screen, ui_model.player2.color, ui_model.player2.rect)

        for option in ui_model.player_move_options:
            pygame.draw.ellipse(self.screen, option.color, option.rect)

        for wall in ui_model.bar_walls:
            if wall.activated == True:
                pygame.draw.rect(self.screen, wall.color, wall.rect)

        if ui_model.ghost_rect is not None:
            pygame.draw.rect(self.screen, BLUE, ui_model.ghost_rect)

        pygame.display.flip()

        return self.screen