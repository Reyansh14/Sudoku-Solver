# Sudoku-Solver
This is a Sudoku solving program that can solve any valid Sudoku board through a backtracking algorithm. There is also a second file that lets the user play Sudoku through a GUI created using Pygame.

There are 2 files: sudoku_solver.py (this file can solve the sudoku board through backtracking) and Sudoku_GUI.py which lets the user play Sudoku themselves.

# Algorithm:
 1: Find an empty space, denoted by 0
 2: Try entering digits 1-9. If it works, move on to the next spot. Else, try the next digit.
 3: If the entered number is invalid, go to the previous step and try a new number.
 4: Perform steps 1-3 until the board is filled.

# The GUI file is a work-in-progress. In this GUI, the user actually solves the game, rather than the computer solving it for us.
 You can click on a square and enter any digit from 1-9. First, it writes your choice in grey font temporarily. To confirm the choice, press enter.
 If the entered value is incorrect, a red X shows up in the bottom of the screen. You can then try again with another value or press delete to erase the number.
 If the value is correct, the console prints 'Correct' and the value is set in dark font and unchangeable. The game is over when the entire board is filled correctly.
TODO: Add a backtracking visualizer for the GUI as well, bugfixing, add a set amount of lives system, and 2 more boards giving the user a chance to pick the easy/medium/hard board.
