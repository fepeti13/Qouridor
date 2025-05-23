class LogicModel:
    def __init__(self, N):
        self.SWN = 2 * N - 1        #Square Wall N
        self.matrix = []
        for i in range(self.SWN):
            row = [0] * self.SWN
            self.matrix.append(row)

        self.matrix[0][N] = 1
        self.matrix[-1][N] = 2

        self.matrix[1][3] = 9
        self.matrix[3][7] = 9
        self.matrix[3][6] = 9
        self.matrix[2][3] = 9
 