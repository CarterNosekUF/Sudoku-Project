import pygame
from sudoku_generator import generate_sudoku

# Sets colors for the program
line_color = (103, 135, 93)
background_color = (205, 232, 197)
white = (255, 255, 255)
dark_green = (31, 38, 26)


# Defines the Cell class
class Cell:
    # This class represents a single cell in the Sudoku board. There are 81 Cells in a Board.
    def __init__(self, value, row, col, screen=None):
        # Constructor for the Cell class
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        # Setter for this cell’s value
        self.value = value

    def set_sketched_value(self, value):
        # Setter for this cell’s sketched value
        self.sketched_value = value

    def draw(self):
        # Draws this cell, along with the value inside it.
        # If this cell has a nonzero value, that value is displayed.
        # Otherwise, no value is displayed in the cell.
        # The cell is outlined red if it is currently selected.
        # draw red rectangle around cell
        red = (255, 0, 0)
        square_size = 70
        pygame.draw.rect(screen, red, pygame.Rect(self.col * square_size + 2, self.row *
                                                  square_size + 2, square_size - 3, square_size - 3), 5)


class Board:
    # This class represents an entire Sudoku board. A Board object has 81 Cell objects.
    def __init__(self, width, height, screen, difficulty):
        # Checks the difficulty parameter and calls the generate_sudoku method accordingly
        if difficulty == "easy":
            self.board_list = generate_sudoku(9, 30)
        elif difficulty == "medium":
            self.board_list = generate_sudoku(9, 40)
        elif difficulty == "hard":
            self.board_list = generate_sudoku(9, 50)
        self.board = []
        # Creates a board filled with cell objects
        for r in range(len(self.board_list)):
            self.board.append([])
            for c in range(0, 9):
                temp_cell = Cell(self.board_list[r][c], r, c, screen)
                self.board[r].append(temp_cell)
        # Creates a sketched values board initially filled with zeros
        self.sketched_values = []
        dimensions = len(self.board_list)
        for r in range(dimensions):
            self.sketched_values.append([])
            for c in range(dimensions):
                self.sketched_values[r].append(0)

    # Defines the draw method of the class
    def draw(self):
        # Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
        line_color = (103, 135, 93)
        sketched_color = (157, 172, 167)
        box_height = 210
        box_width = 210
        pygame.draw.line(screen, line_color, (0, 0), (630, 0), 4)
        # Draws vertical and horizontal lines
        for x in range(9):
            pygame.draw.line(screen, line_color, (0, box_height), (900, box_height), 4)
            box_height += 210
        for x in range(9):
            pygame.draw.line(screen, line_color, (box_width, 630), (box_width, 0), 4)
            box_width += 210
        line_width = 70
        line_height = 70
        for x in range(9):
            pygame.draw.line(screen, line_color, (0, line_height), (900, line_height), 2)
            line_height += 70
        for x in range(9):
            pygame.draw.line(screen, line_color, (line_width, 630), (line_width, 0), 2)
            line_width += 70
        # Sets the font for the numbers
        font = pygame.font.Font(None, 70)
        sketched_font = pygame.font.Font(None, 60)
        square_size = 70
        for x in range(9):
            for y in range(9):
                # since the 2d board list is a list of rows, swapping y and x here makes the rows
                # on the screen match up with the rows in the 2d board list
                tmp = self.board[x][y].value
                if tmp != 0:
                    nums = font.render(str(tmp), True, line_color)
                    screen.blit(nums, (y * square_size + 22, x * square_size + 15))
                if self.sketched_values[x][y] != 0:
                    nums = sketched_font.render(str(self.sketched_values[x][y]), True, sketched_color)
                    screen.blit(nums, (y * square_size + 5, x * square_size + 5))

    # Defines the select method of the class
    def select(self, row, col):
        # Marks the cell at (row, col) in the board as the current selected cell.
        # Once a cell has been selected, the user can edit its value or sketched value.
        self.selected_cell = (row, col)
        cell_value = self.board[self.selected_cell[0]][self.selected_cell[1]]
        box_selected = Cell(cell_value, self.selected_cell[0], self.selected_cell[1])
        return box_selected

    # Defines the click method of the class
    def click(self, x, y):
        # Returns the cell that the user clicks
        row = y // 70
        col = x // 70
        cell = (row, col)
        self.select(row, col)
        return cell

    def sketch(self, value):
        # Sets the sketched value of the current selected cell equal to user entered value.
        # It will be displayed at the top left corner of the cell using the draw() function.
        if self.board_list[self.selected_cell[0]][self.selected_cell[1]] == 0:
            self.sketched_values[self.selected_cell[0]][self.selected_cell[1]] = value

    def place_number(self):
        # Sets the value of the current selected cell equal to user entered value.
        # Called when the user presses the Enter key.
        if self.board_list[self.selected_cell[0]][self.selected_cell[1]] == 0:
            if self.sketched_values[self.selected_cell[0]][self.selected_cell[1]] != 0:
                value = self.sketched_values[self.selected_cell[0]][self.selected_cell[1]]
                self.board[self.selected_cell[0]][self.selected_cell[1]].set_cell_value(value)
                self.sketched_values[self.selected_cell[0]][self.selected_cell[1]] = 0

    # Resets the board and sketched_values to it's original state
    def reset_to_original(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                self.board[row][col].set_cell_value(self.board_list[row][col])
                self.sketched_values[row][col] = 0

    # Defines the is_full getter
    def is_full(self):
        # Returns True if the board is full, False if else
        zero_count = 0
        for x in range(9):
            for y in range(9):
                if self.board[x][y].value == 0:
                    zero_count += 1
        if zero_count > 0:
            return False
        else:
            return True

    # Defines the check_board method
    def check_board(self):
        # is board solved correctly
        # is each row valid
        for row in range(9):
            possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for col in range(9):
                try:
                    possible_nums.remove(self.board[row][col].value)
                except:
                    return False
            if len(possible_nums) > 0:
                return False

        # is each column valid
        for col in range(9):
            possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for row in range(9):
                try:
                    possible_nums.remove(self.board[row][col].value)
                except:
                    return False
            if len(possible_nums) > 0:
                return False

        # is each box valid
        # turn the 2d board into a list of boxes
        list_boxes = [[], [], [], [], [], [], [], [], []]
        # Iterates through the first box
        for row in range(0, 3):
            for col in range(3):
                list_boxes[0].append(self.board[row][col].value)
            for col in range(3, 6):
                list_boxes[1].append(self.board[row][col].value)
            for col in range(3, 6):
                list_boxes[2].append(self.board[row][col].value)
        # Iterates through the second box
        for row in range(3, 6):
            for col in range(3):
                list_boxes[3].append(self.board[row][col].value)
            for col in range(3, 6):
                list_boxes[4].append(self.board[row][col].value)
            for col in range(3, 6):
                list_boxes[5].append(self.board[row][col].value)
        # Iterates through the third box
        for row in range(6, 9):
            for col in range(3):
                list_boxes[6].append(self.board[row][col].value)
            for col in range(3, 6):
                list_boxes[7].append(self.board[row][col].value)
            for col in range(3, 6):
                list_boxes[8].append(self.board[row][col].value)
        # Checks if the boxes are valid
        for box in range(9):
            possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for num_in_box in range(9):
                try:
                    possible_nums.remove(list_boxes[box][num_in_box])
                except:
                    return False
            if len(possible_nums) > 0:
                return False
        return True


# Defines the start_menu method
def start_menu():
    # Sets all screen variables
    welcome = "welcome to sudoku!"
    select_txt = "select game mode:"
    width = 630
    height = 730
    title_font = pygame.font.SysFont('couriernew', 50)
    select_font = pygame.font.SysFont('couriernew', 40)
    button_font = pygame.font.SysFont('couriernew', 20)
    # Fills the screen with the background color
    screen.fill(background_color)
    # Builds welcome text
    welcome_surf = title_font.render(welcome, True, line_color)
    welcome_rect = welcome_surf.get_rect(center=(width // 2, height - 450))
    screen.blit(welcome_surf, welcome_rect)
    # Builds select text
    select_surf = select_font.render(select_txt, True, line_color)
    select_rect = select_surf.get_rect(center=(width // 2, height - 200))
    screen.blit(select_surf, select_rect)
    # Builds the easy button
    pygame.draw.rect(screen, line_color, pygame.Rect(70, 580, 130, 60))
    easy_text = "easy"
    easy_surf = button_font.render(easy_text, True, dark_green)
    easy_rect = easy_surf.get_rect(center=(135, 610))
    screen.blit(easy_surf, easy_rect)
    # Builds the medium button
    pygame.draw.rect(screen, line_color, pygame.Rect(250, 580, 130, 60))
    medium_text = "medium"
    medium_surf = button_font.render(medium_text, True, dark_green)
    medium_rect = medium_surf.get_rect(center=(315, 610))
    screen.blit(medium_surf, medium_rect)
    # Builds the hard button
    pygame.draw.rect(screen, line_color, pygame.Rect(430, 580, 130, 60))
    hard_text = "hard"
    hard_surf = button_font.render(hard_text, True, dark_green)
    hard_rect = hard_surf.get_rect(center=(495, 610))
    screen.blit(hard_surf, hard_rect)
    # Updates the display with defined variables
    pygame.display.update()
    # Creates an event loop
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # difficulty selection
                # Checks which button is clicked
                x, y = event.pos
                if (70 <= x <= 200) and (580 <= y <= 640):
                    difficulty = "easy"
                    waiting = False
                elif (250 <= x <= 380) and (580 <= y <= 640):
                    difficulty = "medium"
                    waiting = False
                elif (430 <= x <= 560) and (580 <= y <= 640):
                    difficulty = "hard"
                    waiting = False
    return difficulty


# Defines the buttons method
def buttons():
    # Sets the button font
    button_font = pygame.font.SysFont('couriernew', 20)
    # Builds the reset button
    pygame.draw.rect(screen, line_color, pygame.Rect(70, 650, 130, 50))
    easy_text = "reset"
    easy_surf = button_font.render(easy_text, True, dark_green)
    easy_rect = easy_surf.get_rect(center=(135, 675))
    screen.blit(easy_surf, easy_rect)
    # Builds the restart button
    pygame.draw.rect(screen, line_color, pygame.Rect(250, 650, 130, 50))
    medium_text = "restart"
    medium_surf = button_font.render(medium_text, True, dark_green)
    medium_rect = medium_surf.get_rect(center=(315, 675))
    screen.blit(medium_surf, medium_rect)
    # Builds the exit button
    pygame.draw.rect(screen, line_color, pygame.Rect(430, 650, 130, 50))
    hard_text = "exit"
    hard_surf = button_font.render(hard_text, True, dark_green)
    hard_rect = hard_surf.get_rect(center=(495, 675))
    screen.blit(hard_surf, hard_rect)


# Defines the main method
def main():
    # Establishes an overall runtime loop
    up = True
    while up:
        # Defines the required variables
        difficulty_selection = start_menu()
        board = generate_sudoku(9, 2)
        grid = Board(630, 730, None, difficulty_selection)
        screen.fill(background_color)
        current_coord = None

        GAME_WIN = pygame.USEREVENT + 1
        # custom event, triggers win screen
        GAME_LOSS = pygame.USEREVENT + 2
        # custom event, triggers loss screen
        # Establishes a second runtime loop which keeps the original game data
        running = True
        game_over = False
        while running:
            for event in pygame.event.get():
                # Calls the buttons method
                buttons()
                # Checks for mouse button press
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, background_color,
                                     pygame.Rect(0, 0, 630, 630))  # redraws bg without covering buttons
                    grid.draw()
                    x, y = event.pos
                    # Checks if a game control button is pressed
                    if 0 <= x <= 630 and 630 <= y <= 730:
                        if (70 <= x <= 200) and (650 <= y <= 700):  # Reset button
                            pygame.draw.rect(screen, background_color, pygame.Rect(0, 0, 630, 630))
                            grid.reset_to_original()
                            grid.draw()
                        elif (250 <= x <= 380) and (650 <= y <= 700):  # Restart button
                            running = False
                        elif (430 <= x <= 560) and (650 <= y <= 700):  # Exit button
                            running = False
                            up = False
                    # Establishes the protocol for when a cell is pressed
                    else:
                        current_coord = grid.click(x, y)
                        cell_value = board[current_coord[0]][current_coord[1]]
                        box_selected = Cell(cell_value, current_coord[0], current_coord[1])
                        box_selected.draw()
                try:  # Tries every way the user can interact with the board
                    # Checks for a keypress and changes the board accordingly
                    if event.type == pygame.KEYDOWN:
                        cell_value = board[current_coord[0]][current_coord[1]]
                        box_selected = Cell(cell_value, current_coord[0], current_coord[1])
                        # Checks for left arrow key
                        if event.key == pygame.K_LEFT:
                            if current_coord[1] == 0:
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                            else:
                                current_coord = ((current_coord[0]), (current_coord[1] - 1))
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                        # Checks for right arrow key
                        elif event.key == pygame.K_RIGHT:
                            try:
                                current_coord = ((current_coord[0]), (current_coord[1] + 1))
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                            except IndexError:
                                current_coord = ((current_coord[0]), (current_coord[1] - 1))
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                        # Checks for up arrow key
                        elif event.key == pygame.K_UP:
                            if current_coord[0] == 0:
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                            else:
                                current_coord = ((current_coord[0] - 1), (current_coord[1]))
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                        # Checks for down arrow key
                        elif event.key == pygame.K_DOWN:
                            try:
                                current_coord = ((current_coord[0] + 1), (current_coord[1]))
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                            except IndexError:
                                current_coord = ((current_coord[0] - 1), (current_coord[1]))
                                box_selected = grid.select((current_coord[0]), (current_coord[1]))
                        # Next segment checks for number keys for sketching
                        # Checks for number 1 key
                        elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            grid.sketch(1)
                        # Checks for number 2 key
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            grid.sketch(2)
                        # Checks for number 3 key
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            grid.sketch(3)
                        # Checks for number 4 key
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            grid.sketch(4)
                        # Checks for number 5 key
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            grid.sketch(5)
                        # Checks for number 6 key
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            grid.sketch(6)
                        # Checks for number 7 key
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            grid.sketch(7)
                        # Checks for number 8 key
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                            grid.sketch(8)
                        # Checks for number 9 key
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                            grid.sketch(9)
                        # Checks if return is pressed, places number
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            pygame.draw.rect(screen, background_color, pygame.Rect(0, 0, 630, 630))
                            grid.draw()
                            grid.place_number()
                            # Updates the screen
                        pygame.draw.rect(screen, background_color, pygame.Rect(0, 0, 630, 630))
                        grid.draw()
                        box_selected.draw()
                # If TypeError occurs, the program simply looks for the next input
                except TypeError:
                    continue
                # Checks if the user closed the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    up = False
                # quits game event loop and sets win to false
                if event.type == GAME_LOSS:
                    win = False
                    game_over = True
                    break
                # quits game event loop and sets win to true
                if event.type == GAME_WIN:
                    win = True
                    game_over = True
                    break
            grid.draw()

            # checks whether to post gamewin or gameloss event when the board is full
            if grid.is_full():
                if not grid.check_board():
                    pygame.event.post(pygame.event.Event(GAME_LOSS))
                if grid.check_board():
                    pygame.event.post(pygame.event.Event(GAME_WIN))

            # end window
            if game_over:
                # Sets screen variables
                end_font = pygame.font.SysFont('impact', 75)
                exit_font = pygame.font.SysFont('impact', 30)
                play_again_font = pygame.font.SysFont('impact', 20)
                screen.fill(background_color)
                # Checks if win and sets win screen
                if win:
                    display_text = 'GAME WON!'
                    pygame.draw.rect(screen, (255, 165, 0), pygame.Rect(250, 300, 130, 60))
                    exit_surf = exit_font.render('EXIT', True, (255, 255, 255))
                    exit_rect = exit_surf.get_rect(center=(315, 330))
                    screen.blit(exit_surf, exit_rect)
                # Checks if loss and sets loss screen
                if not win:
                    display_text = 'GAME OVER'
                    pygame.draw.rect(screen, (255, 165, 0), pygame.Rect(250, 300, 130, 60))
                    play_again_surf = play_again_font.render('PLAY AGAIN?', True, (255, 255, 255))
                    play_again_rect = play_again_surf.get_rect(center=(315, 330))
                    screen.blit(play_again_surf, play_again_rect)
                # Builds screen elements
                surf = end_font.render(display_text, 0, (100, 100, 100))
                rect_end = surf.get_rect(center=(630 // 2, 730 // 2 - 150))
                screen.blit(surf, rect_end)
                # Updates the screen
                pygame.display.update()
                # event loop for end window
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # Checks if user clicks the button
                            x, y = event.pos
                            if 185 < x < 315 and 360 > y > 240:
                                # If win, the button will be a quit button
                                if win:
                                    pygame.quit()
                                    waiting = False
                                    up = False
                                # If loss, the button will be a try again button, which recursively runs the program again
                                else:
                                    main()

                        # closes window
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            running = False
                            up = False
            # Updates the screen
            pygame.display.update()


if __name__ == '__main__':
    # Initializes pygame variables
    pygame.init()
    screen = pygame.display.set_mode((630, 730))
    pygame.display.set_caption("sudoku")
    icon = pygame.image.load('sudoku.png')
    pygame.display.set_icon(icon)
    # Calls the main method
    main()
