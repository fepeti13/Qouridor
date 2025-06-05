import copy

class BotEngine:
    def __init__(self, logic_model, max_depth=2):
        self.model = logic_model
        self.max_depth = max_depth

    def evaluate(self, model):
        # Heuristic: Favor shorter path for self (player 1), longer for opponent (player 2)
        my_path = model.shortest_path_to_goal(1)
        opp_path = model.shortest_path_to_goal(2)
        return opp_path - my_path

    def minimax(self, model, depth, maximizing_player):
        if depth == 0 or model.is_game_over():
            return self.evaluate(model), None

        if maximizing_player:
            best_value = -float('inf')
            best_move = None

            for move in model.get_valid_moves(1):
                new_model = copy.deepcopy(model)
                new_model.matrix[new_model.player1[0]][new_model.player1[1]] = 0
                new_model.player1 = move
                new_model.matrix[move[0]][move[1]] = 1

                value, _ = self.minimax(new_model, depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_move = ('L', move[0], move[1])

            if model.my_walls_count > 0:
                for wall in model.get_valid_walls():
                    new_model = copy.deepcopy(model)
                    new_model.place_wall(wall[0], wall[1], wall[2])
                    new_model.my_walls_count -= 1

                    value, _ = self.minimax(new_model, depth - 1, False)
                    if value > best_value:
                        best_value = value
                        if wall[0] == 'H':
                            best_move = ('F', wall[1], wall[2], wall[1], wall[2] + 2)
                        else:
                            best_move = ('F', wall[1], wall[2], wall[1] + 2, wall[2])

            return best_value, best_move

        else:
            best_value = float('inf')
            best_move = None

            for move in model.get_valid_moves(2):
                new_model = copy.deepcopy(model)
                new_model.matrix[new_model.player2[0]][new_model.player2[1]] = 0
                new_model.player2 = move
                new_model.matrix[move[0]][move[1]] = 2

                value, _ = self.minimax(new_model, depth - 1, True)
                if value < best_value:
                    best_value = value
                    best_move = ('L', move[0], move[1])

            if model.opponent_walls_count > 0:
                for wall in model.get_valid_walls():
                    new_model = copy.deepcopy(model)
                    new_model.place_wall(wall[0], wall[1], wall[2])
                    new_model.opponent_walls_count -= 1

                    value, _ = self.minimax(new_model, depth - 1, True)
                    if value < best_value:
                        best_value = value
                        if wall[0] == 'H':
                            best_move = ('F', wall[1], wall[2], wall[1], wall[2] + 2)
                        else:
                            best_move = ('F', wall[1], wall[2], wall[1] + 2, wall[2])

            return best_value, best_move

    def make_a_move(self):
        _, best_move = self.minimax(self.model, self.max_depth, True)
        return best_move
