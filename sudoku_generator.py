import random


# Defines the SudokuGenerator class which creates Sudoku objects
class SudokuGenerator:
    # Instantiates required attributes of the object
    def __init__(self, row_length, removed_cells):
        self.row_length = int(row_length)
        self.removed_cells = int(removed_cells)
        # Creates a 2D list that represents the empty sudoku board
        self.board = [[0 for i in range(row_length)] for i in range(row_length)]
        self.box_length = int(row_length ** 0.5)

    # Simple getter function for the board
    def get_board(self):
        return self.board

    # Prints the board
    def print_board(self):
        print(self.board)

    # Checks if a given number would be valid in a given row
    # Returns True if num is not in row, False if num is in row
    def valid_in_row(self, row, num):
        # Iterates through each column and checks if num is already present in the row
        for i in range(self.row_length):
            if self.board[int(row)][i] == num:
                return False
        return True

    # Checks if a given number would be valid in a given column
    # Returns True if num is not in col, False if num is in col
    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][int(col)] == num:
                return False
        return True

    # Checks if a given number would be valid in a given box
    # Returns True if num is not in the box, False if num is in the box
    def valid_in_box(self, row_start, col_start, num):
        for row in range(int(row_start), int(row_start) + 3):
            for col in range(int(col_start), int(col_start) + 3):
                if self.board[int(row)][int(col)] == num:
                    return False
        return True

    # Checks all valid conditions using previously defined methods
    # Returns True if all methods pass, returns False if any fail
    def is_valid(self, row, col, num):
        if not self.valid_in_col(col, num):
            return False
        if not self.valid_in_row(row, num):
            return False
        row_start = int(row) - (int(row % 3))
        col_start = int(col) - (int(col % 3))
        if not self.valid_in_box(row_start, col_start, num):
            return False
        return True

    # Fills the given box with random, and valid, numbers
    def fill_box(self, row_start, col_start):
        # Iterates through each cell in the given box
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                # Sets the cell to a valid, random number
                num = random.randint(1, 9)
                while not self.valid_in_box(row_start, col_start, num):
                    num = random.randint(1, 9)
                self.board[row][col] = num

    # Fills the board diagonally using the fill_box method
    def fill_diagonal(self):
        for i in range(0, self.row_length, 3):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    # Removes random cells according to what difficulty the game is on
    def remove_cells(self):
        for i in range(self.removed_cells):
            r_row = random.randint(0, 8)
            r_col = random.randint(0, 8)
            while self.board[r_row][r_col] == 0:
                r_row = random.randint(0, 8)
                r_col = random.randint(0, 8)
            self.board[r_row][r_col] = 0


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
