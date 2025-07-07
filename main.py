class Game:
    def __init__(self):
        # Initialize the 9x9 Sudoku board with all zeros
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # Store solutions found during the solving process
        self.solutions = []

    def reset(self):
        # Reset the board to all zeros
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # Clear any previously found solutions
        self.solutions = []

    def print_board(self):
        # Print the current state of the Sudoku board
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("- - - - - - - - - - - - ")  # Separator for 3x3 blocks

            for c in range(9):
                if c % 3 == 0 and c != 0:
                    print(" | ", end="")  # Separator for 3x3 blocks
                if c == 8:
                    print(self.board[r][c])  # Print digit and newline at end of row
                else:
                    print(str(self.board[r][c]) + " ", end="")  # Print digit and space

    def insert(self, row, col, value):
        # Check if the row, column, and value are within valid ranges
        if not (0 <= row < 9 and 0 <= col < 9 and 0 <= value <= 9):  # Value can be 0 for deletion
            print("Invalid input: Row, column must be between 0-8 and value between 0-9.")
            return False

        # If the value is 0, it means we are trying to delete, so just set it and return
        if value == 0:
            self.board[row][col] = 0
            return True

        # Check if the value already exists in the given row (excluding the current position if it's already set)
        for i in range(9):
            if self.board[row][i] == value and i != col:
                print(f"Invalid insertion: {value} already exists in row {row}.")
                return False

        # Check if the value already exists in the given column (excluding the current position if it's already set)
        for i in range(9):
            if self.board[i][col] == value and i != row:
                print(f"Invalid insertion: {value} already exists in column {col}.")
                return False

        # Check if the value already exists in the 3x3 subgrid (excluding the current position if it's already set)
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == value and (i, j) != (row, col):
                    print(f"Invalid insertion: {value} already exists in the 3x3 block at ({start_row}, {start_col}).")
                    return False

        # If all checks pass, perform the insertion
        self.board[row][col] = value
        return True

    def delete(self, row, col):
        # Check if the row and column are within valid ranges
        if not (0 <= row < 9 and 0 <= col < 9):
            print("Invalid input: Row, column must be between 0-8.")
            return False

        # Use the insert function to set the cell to 0 (effectively deleting it)
        return self.insert(row, col, 0)

    def build(self, arr):
        # Reset the board before building to ensure a clean slate
        self.reset()

        # Check if the array is 9x9
        if not (len(arr) == 9 and all(len(row) == 9 for row in arr)):
            print("Invalid input: Array must be 9x9.")
            return False

        # Insert each digit from the input array
        for r in range(9):
            for c in range(9):
                value = arr[r][c]
                # Only attempt to insert if the value is not 0
                if value != 0:
                    # Use the insert function to place the digit.
                    # The insert function will handle validity checks.
                    if not self.insert(r, c, value):
                        print(f"Invalid board: Conflict found at ({r}, {c}) with value {value}. Board reset.")
                        self.reset()  # Reset the board if an invalid insertion occurs
                        return False
        # If all digits are inserted successfully, the board is built
        print("Board successfully built.")
        return True

    def find_empty(self):
        # Find the next empty cell (represented by 0)
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c  # Return row and column of the empty cell
        return None  # Return None if no empty cells are found

    def is_valid(self, num, pos):
        # Check if placing 'num' at 'pos' (row, col) is valid according to Sudoku rules

        row, col = pos

        # Check row
        for c in range(9):
            if self.board[row][c] == num and col != c:
                return False

        # Check column
        for r in range(9):
            if self.board[r][col] == num and row != r:
                return False

        # Check 3x3 box
        box_x = col // 3
        box_y = row // 3

        for r in range(box_y * 3, box_y * 3 + 3):
            for c in range(box_x * 3, box_x * 3 + 3):
                if self.board[r][c] == num and (r, c) != pos:
                    return False

        return True

    def solve_sudoku(self):
        # Recursive backtracking function to find solutions
        find = self.find_empty()
        if not find:
            # If no empty cells, a solution is found. Store a copy of the board.
            self.solutions.append([row[:] for row in self.board])
            return True  # Indicate that a solution was found

        row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                # If we already have two solutions, stop searching for more
                if len(self.solutions) >= 2:
                    return True

                self.solve_sudoku()  # Recursively call solve_sudoku

                # Backtrack: reset the cell if the current path doesn't lead to a solution
                if len(self.solutions) < 2:  # Only backtrack if we haven't found two solutions yet
                    self.board[row][col] = 0
        return False

    def solve(self):
        # Main function to initiate the solving process and handle results
        self.solutions = []  # Clear solutions before starting a new solve
        # Create a deep copy of the current board state to work on
        original_board = [row[:] for row in self.board]
        self.solve_sudoku()  # Start the recursive solving

        # Restore the original board state after solving
        self.board = original_board

        if len(self.solutions) == 0:
            print("\nNo solutions exist for this Sudoku puzzle.")
        elif len(self.solutions) == 1:
            print("\nUnique solution found:")
            # Set the board to the unique solution for display
            self.board = self.solutions[0]
            self.print_board()
        else:
            print("\nMultiple solutions exist for this Sudoku puzzle.")
            print("Here are two possible solutions:")
            print("\nSolution 1:")
            # Temporarily set board to first solution for printing
            self.board = self.solutions[0]
            self.print_board()
            print("\nSolution 2:")
            # Temporarily set board to second solution for printing
            self.board = self.solutions[1]
            self.print_board()
            # Restore the original board state after displaying solutions
            self.board = original_board


def main():
    game = Game()
    print("Welcome to the Sudoku Solver!")

    while True:
        print("\n--- Menu ---")
        print("1. Start a new puzzle")
        print("2. Build an entire board")
        print("3. Insert a digit")
        print("4. Delete a digit")
        print("5. Solve the puzzle")
        print("6. Quit")
        game.print_board()  # Display the current board state

        choice = input("Enter your choice: ")

        if choice == '1':
            game.reset()
            print("New puzzle started. Board reset.")
        elif choice == '2':
            print("Please enter 9 rows of 9 whitespace-separated digits, each of them 0-9.")
            try:
                arr = []
                for i in range(9):
                    row_str = input(f"Enter row {i} (each digit 0-9): ")
                    # Split by any whitespace and filter out empty strings
                    row = [int(x) for x in row_str.split() if x.strip()]
                    if len(row) != 9:
                        print("Invalid input. Please enter 9 whitespace-separated digits.")
                        # Clear the partially built array and break to re-prompt for choice
                        arr = []
                        break
                    # Validate that all numbers are between 0 and 9
                    if not all(0 <= num <= 9 for num in row):
                        print("Invalid input. Digits must be between 0 and 9.")
                        arr = []
                        break
                    arr.append(row)

                if len(arr) == 9:  # Only attempt to build if all 9 rows were successfully parsed
                    game.build(arr)
                else:
                    print("Board build cancelled due to invalid input.")

            except ValueError:
                print("Invalid input. Please enter 9 rows of 9 whitespace-separated digits.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '3':
            try:
                row = int(input("Enter row (0-8): "))
                col = int(input("Enter column (0-8): "))
                value = int(input("Enter digit (1-9): "))
                if not game.insert(row, col, value):
                    print("Insertion failed. Please try again.")
            except ValueError:
                print("Invalid input. Please enter numbers for row, column, and digit.")
        elif choice == '4':  # Changed from '3' to '4' to match menu
            try:
                row = int(input("Enter row (0-8): "))
                col = int(input("Enter column (0-8): "))
                if not game.delete(row, col):
                    print("Deletion failed. Please try again.")
            except ValueError:
                print("Invalid input. Please enter numbers for row and column.")
        elif choice == '5':
            game.solve()
        elif choice == '6':
            print("Exiting Sudoku Solver. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")  # Updated range


if __name__ == "__main__":
    main()
