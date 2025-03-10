import math
import numpy as np
from pick import pick

# TODO
# 1. cleanup code
# 2. get user to input sudoku grid size and rows 
	# --- 1. ask user for grid size and set global variable
	# * 2. ask user for sort sudoku and create grid (normal, chaos, killer)
	# * 3. ask user for sub grids
# 3. score each cell based on different hueristics
	# --- score by number of options
	# --- score by influence on other cells in row/col/subgrid
	# --- score by number of influencable cells
# 4. interact with user about best cell
	# --- 1. show best cell and ask user to solve 
	# * 2. provide extra hints so the user can solve it
	# * 3. provide option to add more solved cells so user can move on without hints 
# 5. solve sudoku to check users answer
	# 1. solve the entire sudoku using backtracking
	# 2. check users answers with solved sudoku
# 6. iterate until sudoku is solved
# 7. cleanup code
# 8. test code
	# 1. test for edge cases
	# 2. test if codes keeps working
	# 3. test for efficiency

class Question:
	def __init__(self, title, options):
		self.title = title if title else "Choose an option."
		self.options = options if options else []

	def askQuestion(self):
		print(f"\n{self.title}")
		for i, option in enumerate(self.options):
			print(f"{i + 1}. {option}")

		while True:
			answer = input("\nEnter the number of your choice: ")
			if answer.isdigit() and 0 < int(answer) <= len(self.options):
				answer = int(answer) - 1
				return self.options[answer], answer
			else:
				print("\nWrong input. Please pick an option from the list above.")


class Sudoku:	
	def __init__(self, grid_size=9):
		self.grid_size = grid_size  # Grid size (default is 9x9)
		self.subgrid_size = int(math.sqrt(grid_size))  # Subgrid size (e.g., 3 for a 9x9 grid)
		self.board = np.full((grid_size, grid_size), np.nan)  # Board setup
		self.solution = np.full((grid_size, grid_size), np.nan)  # Empty solution grid
		self.options = []
		for i in range(grid_size):
			self.options.append([])
			for j in range(grid_size):
				self.options[i].append([])	  

	def set_board(self):
		self.board = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]
		# print("Enter the Sudoku board row by row, using 0 for empty cells.")
		# for i in range(9):
		# 	while True:
		# 		try:
		# 			row = input(f"Row {i + 1}: ").strip()
		# 			if len(row) != 9 or not row.isdigit():
		# 				raise ValueError("Please enter exactly 9 digits.")
		# 			self.board.append([int(num) for num in row])
		# 			break
		# 		except ValueError as e:
		# 			print(e)
		# return self.board

	def print_board(self):
		for row in range(self.grid_size):
			# Print horizontal grid separator every subgrid_size rows
			if row % self.subgrid_size == 0 and row != 0:
				print("-" * (self.grid_size * 2 + self.subgrid_size - 1))  # Add spacing for visual grid

			for col in range(self.grid_size):
				# Print vertical grid separator every subgrid_size columns
				if col % self.subgrid_size == 0 and col != 0:
					print("|", end=" ")  # Add a column separator

				# Print the number, with a period for empty cells (0)
				print(f"{self.board[row][col] if self.board[row][col] != 0 else '.'}", end=" ")

			print()  # Newline after each row

	def is_completed(self):
		for row in range(self.grid_size):
			for col in range(self.grid_size):
				if self.board[row][col] == 0:
					return False

		return True
	
	def is_valid_num(self, row, col, num):
		for x in range(self.grid_size):
			if self.board[row][x] == num or self.board[x][col] == num:
				return False

		start_row = self.subgrid_size * (row // self.subgrid_size)
		start_col = self.subgrid_size * (col // self.subgrid_size)

		for i in range(self.subgrid_size):
			for j in range(self.subgrid_size):
				if self.board[i + start_row][j + start_col] == num:
					return False

		return True

	def solve_sudoku(self):
		def askHintOrAll(row, col, score):
			hintOrAllQuestion = Question("Do you want the next best hint or all the best options?", ['Hint', 'All'])
			hintOrAllAnswer, hintOrAllIndex = hintOrAllQuestion.askQuestion()

			if hintOrAllIndex == 0:
				print("\nYou choose the next best hint")
				print(f"\nRow {row} and column {col} is the next best cell to fill in with a score of {score}")
			elif hintOrAllIndex == 1:
				print("\nYou choose all best options")

				if len(single_options) > 0:
					for r, c, o in single_options:
						print(f"\nRow {r + 1} and column {c + 1} has one option")

				print(f"\nRow {row} and column {col} is the next best cell to fill in with a score of {score}")
			else:
				print("\nInvalid answer")
				return False

		def askInput():
			nonlocal self
			# change to one or multiple when ready
			inputQuestion = Question("Do you want to give a cell a try?", ['Yes', 'No'])
			inputAnswer, inputIndex = inputQuestion.askQuestion()

			if inputIndex == 0:
				rowAnswer = input("\nWhich row? ")
				while rowAnswer.isdigit() and 1 > int(rowAnswer) > 9:
					rowAnswer = input("Which row? Please fill in a number between 1 and 9")
					
				colAnswer = input("\nWhich column? ")
				while colAnswer.isdigit() and 1 > int(colAnswer) > 9:
					colAnswer = input("Which column? Please fill in a number between 1 and 9")

				numAnswer = input("\nWhich number? ")
				while numAnswer.isdigit() and 1 > int(numAnswer) > 9:
					numAnswer = input("Which number? Please fill in a number between 1 and 9")

				rowAnswer = int(rowAnswer) - 1
				colAnswer = int(colAnswer) - 1
				numAnswer = int(numAnswer)

				if self.is_valid_num(rowAnswer, colAnswer, numAnswer):
					print("\nNice, this is correct!")
					self.board[rowAnswer][colAnswer] = numAnswer
					self.options[rowAnswer][colAnswer] = []
					self.print_board()
				else:
					print("\nToo bad, better next time.")
			elif inputIndex == 1:
				print("\n'Till next time!")
				return False
			else:
				print("\nInvalid answer")
				return False

		if self.is_completed():
			print("The sudoku is complete!")
			self.print_board()
			return False
		else:
			options = sudoku.get_options()

			row, col, score, single_options = sudoku.get_best_cell()
			row += 1
			col += 1

			askHintOrAll(row, col, score)

			askInput()


			self.solve_sudoku()
			return True

	def get_options(self):
		for row in range(self.grid_size):
			for col in range(self.grid_size):
				if(self.board[row][col] == 0):
					# change to this, if speed matter
					# for num in range(len(options[row][col]) + 1, 10):
					for num in range(1, self.grid_size + 1):
						if self.is_valid_num(row, col, num):
							if num not in self.options[row][col]:
								self.options[row][col].append(num)
		return self.options

	def get_best_cell(self):
		best_row, best_col = -1, -1
		best_score = 0

		scores = np.zeros((self.grid_size, self.grid_size))
		single_options = []

		for row in range(self.grid_size):
			for col in range(self.grid_size):
				if(len(self.options[row][col]) > 0):
					if(len(self.options[row][col]) == 1):
						scores[row][col] = 100
						single_options.append([row, col, self.options[row][col][0]])
					scores[row][col] += self.score_sudoku_cell(row, col)

		for row in range(self.grid_size):
			for col in range(self.grid_size):
				if(scores[row][col] > best_score):
					best_score = scores[row][col]
					best_row, best_col = row, col

		return best_row, best_col, int(best_score), single_options

	def score_sudoku_cell(self, row, col):
		current_cel = self.options[row][col]
		score = 0
		influenced_cells = []

		def calculate_score(row, col):
			nonlocal self, current_cel, score, influenced_cells
			if([row, col] in influenced_cells):
				return
			else:
				options_length = len(self.options[row][col])
				if(options_length > 0):
					score += (1 / options_length)

					equal_array = np.intersect1d(current_cel, self.options[row][col])
					score += (options_length - len(equal_array)) / options_length

					influenced_cells.append([row, col])

		for r in range(self.grid_size):
			if(r != row):
				calculate_score(r, col)

		for c in range(self.grid_size):
			if(c != col):
				calculate_score(row, c)

		subgrid_row_start = (row // self.subgrid_size) * self.subgrid_size
		subgrid_col_start = (col // self.subgrid_size) * self.subgrid_size

		for r in range(subgrid_row_start, subgrid_row_start + self.subgrid_size):
			for c in range(subgrid_col_start, subgrid_col_start + self.subgrid_size):
				if (r != row or c != col):
					calculate_score(r, c)

		score += len(influenced_cells)

		return score


# Main program
if __name__ == '__main__':
	grid_size = 9
	# grid_size = input("What is the size of the grid? ")
	sudoku = Sudoku(9)
	sudoku.set_board()
	print("\nInitial board:")
	sudoku.print_board()
	sudoku.solve_sudoku()
