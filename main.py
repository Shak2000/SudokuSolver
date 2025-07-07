class Game:
    def __init__(self):
        self.board = [[0 for i in range(9)] for j in range(9)]

    def reset(self):
        self.board = [[0 for i in range(9)] for j in range(9)]

    def insert(self, row, col, value):
        for i in range(9):
            if self.board[i][col] == value or self.board[row][i] == value:
                return False

        for i in range(row // 3, row // 3 + 3):
            for j in range(col // 3, col // 3 + 3):
                if self.board[i][j] == value:
                    return False

        self.board[row][col] = value
        return True

    def solve(self):
        pass


def main():
    print("Welcome to the Sudoku Solver!")


if __name__ == "__main__":
    main()
