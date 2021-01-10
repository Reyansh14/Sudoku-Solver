
# * This is a Sudoku Solver implemented with a backtracking algorithm. Rather than using brute force, the backtracking algorithm takes a step back
# * each time it runs into an incorrect solution and tries another value.

# Algorithm:
# 1: Find an empty space, denoted by 0
# 2: Try entering digits 1-9. If it works, move on to the next spot. Else, try the next digit.
# 3: If the entered number is invalid, go to the previous step and try a new number.
# 4: Perform steps 1-3 until the board is filled.

# TODO: Add some more boards ranging in difficulty from easy to hard.

# Defining sample sudoku boards:
board1 = [
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

board2 = [
    [5, 6, 0, 0, 1, 0, 0, 0, 0],
    [3, 0, 0, 7, 0, 0, 9, 1, 0],
    [1, 0, 0, 0, 5, 2, 0, 0, 3],
    [8, 5, 0, 6, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 7, 1],
    [4, 0, 0, 0, 0, 0, 2, 0, 0],
    [6, 0, 0, 9, 0, 4, 0, 3, 2],
    [7, 0, 0, 0, 0, 1, 5, 0, 0],
    [2, 0, 0, 0, 3, 0, 0, 6, 4]
]

# make_board prints out the board in terminal with appropriate row and column divisions.


def make_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])

            else:
                print(str(board[i][j]) + " ", end="")

# get_empty_space finds empty spaces on the board denoted by 0 by looping through each element in the given board.


def get_empty_space(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # Returns row,column of an empty spot

    return None

# is_valid checks whether the given solution is valid or not


def is_valid(board, num, pos):

    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check cube
    cube_x = pos[1] // 3
    cube_y = pos[0] // 3

    for i in range(cube_y * 3, (cube_y * 3) + 3):
        for j in range(cube_x * 3, (cube_x * 3) + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True

# solve_board utilizes the helper functions above to solve the board recursively.


def solve_board(board):
    get_empty = get_empty_space(board)

    if not get_empty:
        return True
    else:
        row, column = get_empty

        for i in range(1, 10):
            if is_valid(board, i, (row, column)):
                board[row][column] = i

                if solve_board(board):
                    return True

                board[row][column] = 0

    return False


print("Welcome to my Sudoku Solver. The program will solve the sudoku board by using a backtracking algorithm.")
selection = input("Enter '1' to pick board 1 or '2' to pick board 2: ")

if selection == 1:
    print("ORIGINAL BOARD 1:")
    print(make_board(board1))
    solve_board(board1)
    print("SOLVED BOARD:")
    print(make_board(board1))
else:
    print("ORIGINAL BOARD 2:")
    print(make_board(board2))
    solve_board(board2)
    print("SOLVED BOARD:")
    print(make_board(board2))
