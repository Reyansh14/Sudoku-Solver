
# * This file is the GUI (work-in-progress) for the Sudoku Solver. In this GUI, the user actually solves the game, rather than the computer solving it for us.
# You can click on a square and enter any digit from 1-9. First, it writes your choice in grey font temporarily. To confirm the choice, press enter.
# If the entered value is incorrect, a red X shows up in the bottom of the screen. You can then try again with another value or press delete to erase the number.
# If the value is correct, the console prints 'Correct' and the value is set in dark font and unchangeable. The game is over when the entire board is filled correctly.

# TODO: Add a backtracking visualizer for the GUI as well, bugfixing, add a set amount of lives system, and 2 more boards giving the user a chance to pick the easy/medium/hard board.

import pygame
from sudoku_solver import solve_board, is_valid
import time
pygame.font.init()

# The Grid class holds all of the cubes of the board in a row/column structure.


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    # update_model updates the board with the latest changes each time it is called.
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    # place simply places the permanent value into the selected cube if it is valid. Otherwise, the value is not placed permanently (in dark font).
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if is_valid(self.model, val, (row, col)) and solve_board(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # sketch just draws the temporary value in grey before the user presses enter.
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    # draw creates the grid lines that make the board look like a traditional sudoku board.
    def draw(self, win):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap),
                             (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i*gap, 0),
                             (i*gap, self.height), thick)

        # Drawing cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    # select selects the square that was clicked on.
    def select(self, row, col):
        # resets all other selected values
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # clear clears any value entered in the selected cube, only if it is a temporary value (in grey).
    def clear(self, pos):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # click return the position of the cube that was clicked on.
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    # is_finished checks there are no more empty squares on the board
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

# The Cube class defines each cube in the grid as well as the specific attributes of each cube.


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # The draw method draws the selected box and the number on the selected box.
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2),
                            y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    # set sets the value for a box
    def set(self, val):
        self.value = val

    # set_temp sets the temporary value in a box
    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))
    # Drawing the time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # Drawing the strikes
    text = fnt.render("X" * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Drawing the grid and the board
    board.draw(win)

# format_time correctly formats the time and keeps track of how long the game is going on for.


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

# main puts together all of the helped functions thus far and runs the program.


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
