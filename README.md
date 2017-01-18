

The sudoku program runs a server on the specified port which serves a web page with a sudoku board.

Alternatively, the sudoku module can be imported and its solve used like this, an example of a board being solved in this manner is in example.py.

from sudoku import solve

input = {
	(0,0):3,
	(1,0):6,
	(3,1):9,
	....
}

answer = solve(input)

answer is a 2d list of the solution
