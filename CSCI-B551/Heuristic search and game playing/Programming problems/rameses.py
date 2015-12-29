"""
Problem formulation:
    In this problem we have to find best next move to play
    Game:
        Board of size n*n, each player puts a pebble empty square.
    Rule:
        Player who first completes the row or column or diagonal loses

Initial State:
    Board configuration provided by user in the form of string like "x.x......"

Action:
    Put pebble in empty square.

Transition model:
    If we put pebble in empty square of current state new board state will be generated.

State space:
    every possible combination which can be generated by putting or not putting a pebble in each empty square.
    ( pebble are not put in square if the given state represents the end of game by game rule.)

Edge weight:
    Implemented algorithm do not use edge weight

Goal state:
    At least one row or one column or one diagonal has no empty squares.

Successor function:
    It will give all possible states from current state.

Evaluation function:
    After max plays his move preferably even number of moves should be open. So, that max and min alternatively will
    fill those up and min will have to make concluding move in which min will complete row or column or diagonal.
    Although this not perfect evaluation function as putting pebble in one empty square can leave other empty square
    as only the empty square in a row or column or a diagonal, thus if we put pebble in this square we will lose.
    But, still this evaluation function works fine.

Algorithm:
    Alpha - Beta pruning


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~Features of the program ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) Implemented using alpha beta pruning
2) It has lookup tree, to keep track of visited states
3) Multi-threading is done in order to produce result in given time.
4) It uses iterative deepening approach
5) bound on memory usage

    Alpha beta tree is depth first algorithm, thus it's memory efficient.
    But lookup_tree build will increase in size as new entries will be added to it.
    bound has been put on number of entries to be put in lookup_tree so that is will not consume too much memory
    thus, saving the system resources and avoiding crashing of system.

    NOTE: Value for lookup_entries_bound need to be set manually. (preferably according to available memory in system)

6) Quick termination
    as soon as stop variable changes to 1, computations will end quickly.
    each min and max program checks value of depth_limit, it will be set to 0.
    Hence, no min or max function will call its successor and return to its parent.
    Thus quickly ending computations.


"""
import sys
from random import shuffle
from threading import Thread
from time import sleep
from time import time


# Declaring the class for creating lookup tree
class Tree(object):
	def __init__(self):
		self.left = None            # left is assigned to empty square
		self.right = None           # right is assigned to non-empty square
		self.index = None           # index of number it represents also used to check if the node contains data or not


# To rotate given matrix by 90 degree
def rotate90(array):
	array2 = [[0 for k in range(0, size)] for j in range(0, size)]        # initialising the matrix to be returned
	for i in range(0, size):
		for j in range(0, size):
			array2[i][j] = array[size - j - 1][i]
	return array2


# To get mirror image of matrix on x-axis
def mirror(array):
	array2 = [[0 for i in range(0,size)] for j in range(0,size)]        # initialising the matrix to be returned
	for i in range(0,size):
		for j in range(0,size):
			array2[i][j]=array[i][size-j-1]
	return array2


# it will return all possible symmetrical compositions of matrix, containing rotations and mirrors
def symmetry(array):

	# rotations of matrix
	state = array[:]
	children = [state]
	temp = rotate90(state)
	children.append(temp)
	temp = rotate90(temp)
	children.append(temp)
	temp = rotate90(temp)
	children.append(temp)

	# mirror image of matrix an its rotation
	temp = mirror(array)
	children.append(temp)
	temp = rotate90(temp)
	children.append(temp)
	temp = rotate90(temp)
	children.append(temp)
	temp = rotate90(temp)
	children.append(temp)

	return children


# it will not only look for the matrix in lookup tree, but also all its possible symmetrical compositions
def symmetry_lookup(state, node, depth):

	children = symmetry(state)          # get all symmetrical possible combinations
	returned = 0
	for c in children:
		returned = lookup(c, node, depth)
		if returned != 0:
			return returned
	return returned


# it will lookup for particular state or matrix in lookup tree
def lookup(state, node, depth):

	if depth == number_of_squares:
		return node.index

	if node.index is None:
		return 0

	if state[depth/size][depth % size] == 0:            # presence of left node represents absence of pebble in square
		if node.left is None:
			return 0
		else:
			return lookup(state, node.left, depth+1)

	if state[depth/size][depth % size] == 1:            # presence of right node represents presence of pebble in square
		if node.right is None:
			return 0
		else:
			return lookup(state, node.right, depth+1)


def flush_lookup_tree(node):
	if node.index is not None:
		node.index = None
		if node.left is not None:
			flush_lookup_tree(node.left)
			del node.left
			node.left = None
		if node.right is not None:
			flush_lookup_tree(node.right)
			del node.right
			node.right = None


# it will insert matrix and its value in lookup tree
def insert_in_lookup_tree(tuple, node):

	global lookup_entries
	global lookup_entries_bound
	if lookup_entries < lookup_entries_bound:
		lookup_entries += 1

		state = tuple[0]
		for depth in range(0, number_of_squares):

			if node.index is None:                          # setting index value of node as index value of square
				node.index = depth

			if state[depth/size][depth % size] == 0:        # presence of left node represents absence of pebble in square
				if node.left is None:
					node.left = Tree()
				node = node.left

			elif state[depth/size][depth % size] == 1:      # presence of right node represents presence of pebble in square
				if node.right is None:
					node.right = Tree()
				node = node.right

		node.index = tuple[2]


# function to check it is goal state or not
def is_terminating_state(state):

	value = 0                           # variable to hold the estimated value for the function

	for i in state:                     # calculating the value for rows
		if 0 in i:
			value += 1

	for i in range(0, size):            # calculating the value for backslash type diagonal
		if state[i][i] == 0:
			value += 1
			break

	for a in range(0, size):            # calculating the value for forwardslash type diagonal
		if state[a][size-1-a] == 0:
			value += 1
			break

	for i in map(list, zip(*state)):    # calculating the value for columns
		if 0 in i:
			value += 1

	if value < (size*2 + 2):
		return True
	else:
		return False


# Calculates available number of positions to put pebble
# Ex: output :[ 0 1 0 ]
#             [ 0 0 1 ]
#             [ 1 0 0 ]
#       it means that we will not lose if we put pebble in the square whose value is 1
#       and we will lose if we put pebble in the square where value is zero
#       square with value zero is combination of empty squares in which if we put pebble we will lose
#       and squares which already have pebbles.
def open_moves(state):

	# calculating number of open field
	openmatrix = []
	for i in state:
		openmatrix.append(i[:])

	for i in range(0, size):
		for j in range(0, size):
			open_sq = 0
			if state[i][j] == 0:

				open_sq = 1

				# checking for the row
				zeros = 0
				k = 0
				while k < size:
					if state[i][k] == 0:
						zeros += 1
					k += 1
				if zeros == 1:
					open_sq = 0

				# checking for the column
				zeros = 0
				k = 0
				while k < size:
					if state[k][j] == 0:
						zeros += 1
					k += 1
				if zeros == 1:
					open_sq = 0

				#checking for diagonals
				zeros = 0
				if i == j:
					k = 0
					while k < size:
						if state[k][k] == 0:
							zeros += 1
						k += 1
					if zeros == 1:
						open_sq = 0

				zeros = 0
				if (i+j) == (size-1):
					k = 0
					while k < size:
						if state[k][size-1-k] == 0:
							zeros += 1
						k += 1
					if zeros == 1:
						open_sq = 0
			openmatrix[i][j] = open_sq
	return openmatrix


# evaluate the state
# Basically approach is that after max makes move, even number of open position should be available
# so that max and min will fill them alternatively and min have to make losing move
def eval_state(state, player):      # player = 0 -> represents max
	# player = 1 -> represents min
	evalue = 0
	if is_terminating_state(state):
		if player == 0:
			return -3
		else:
			return 3
	for c in open_moves(state):
		for d in c:
			if d != 0:
				evalue += 1
	if evalue % 2 == player:
		return 3
	else:
		return -3


# simply gives number of empty positions in matrix or board
def empty_squares(state):

	evalue = 0
	for c in state:
		for d in c:
			if d == 0:
				evalue += 1
	return evalue


# Generate and returns the list of childs
# child structure
# child[0] -> matrix or board representation
# child[1] -> index of square on board or matrix on which parents state put pebble to get this state
# child[2] -> evaluated value of the board
def gen_childs(state):

	open_moves_matrix = open_moves(state)
	list_of_empty_square = []
	for i in range(0,size):
		for j in range(0,size):
			if open_moves_matrix[i][j] == 1:
				list_of_empty_square.append([i,j])

	shuffle(list_of_empty_square)               # shuffling the elements to get randomness

	childs = []
	for num in list_of_empty_square:            # just choosing empty position one by one and putting the pebble
		temp = []
		for i in range(0,size):
			temp.append([])
		for i in range(0, size):
			temp[i] = state[i][:]
		temp[num[0]][num[1]] = 1
		position = num[0]*size + num[1]
		childs.append([temp, position, 0])
	return childs


# Alpha beta function
# vary similar to max function just modified it to return best move position on calling point
def alpha_beta(state, depth, alpha, beta):

	pos = 0
	childs = gen_childs(state)
	if not childs:
		losing_position = -1
		for x in range(0, size):
			if state[0][x] == 0:
				losing_position = x
				break
		return [losing_position, 0]
	if depth < depth_limit:
		for c in childs:
			c[2] = min_play(c[0],depth+1, alpha, beta)
			if pos == 0:
				alpha = c[2]
				pos = c[1]
			else:
				if c[2] > alpha:
					alpha = c[2]
					pos = c[1]

			if alpha >= beta:
				return [pos, alpha]

	else:
		for c in childs:
			c[2] = eval_state(c[0], 0)              # 0 -> represents that function was called from max
			if pos == 0:
				alpha = c[2]
				pos = c[1]
			else:
				if c[2] > alpha:
					alpha = c[2]
					pos = c[1]

			if alpha >= beta:
				return [pos, alpha]

	return [pos, alpha]


# Max function
def max_play(state, depth, alpha, beta):
	global cost
	cost += 1

	if is_terminating_state(state):
		return 4
	childs = gen_childs(state)

	if not childs:
		return -4

	if depth < depth_limit:
		for c in childs:
			lookup_result = symmetry_lookup(state, lookup_tree, 0)
			if lookup_result == 0:
				c[2] = min_play(c[0],depth+1, alpha, beta)
				insert_in_lookup_tree(c,lookup_tree)
			else:
				c[2] = lookup_result
			alpha = max(alpha, c[2])
			if alpha >= beta:
				return alpha

	else:
		for c in childs:
			c[2] = eval_state(c[0], 0)              # 0 -> represents that function was called from max
			alpha = max(alpha, c[2])
			if alpha >= beta:
				return alpha

	return alpha


# Min function
def min_play(state, depth, alpha, beta):
	global cost
	cost += 1

	if is_terminating_state(state):
		return -4

	childs = gen_childs(state)
	if not childs:
		return 4

	if depth < depth_limit:
		for c in childs:
			lookup_result = symmetry_lookup(state, lookup_tree, 0)
			if lookup_result == 0:
				c[2] = max_play(c[0], depth+1, alpha, beta)
				insert_in_lookup_tree(c,lookup_tree)
			else:
				c[2] = lookup_result
			beta = min(beta, c[2])
			if alpha >= beta:
				return beta
	else:
		for c in childs:
			c[2] = eval_state(c[0], 1)              # 1 -> represents that function was called from min
			beta = min(beta, c[2])
			if alpha >= beta:
				return beta

	return beta


# creating thread to get result in time
# one thread will halt for given time and another will compute the results till then
# when time is over it will signal other thread to stop and print the results.
def solving_thread(given):

	global depth_limit
	global stop
	global lookup_entries
	# creating 2 dimensional matrix to represent the state
	ogstate = []
	for i in range(0, size):
		ogstate.append([])
		for j in range(0, size):
			if given[i*size + j] == ".":
				ogstate[i].append(0)
			else:
				ogstate[i].append(1)

	# to check if the input is Goal state or not

	if is_terminating_state(ogstate):           # checking if game is ended or not
		print "I win because give state is end of game assuming:"
		print "last move played by opponent hence, opponent completing one row, column or diagonal"
		stop = 1

	else:                                       # if game has not ended give next best move
		position = 0
		new_depth = 0

		# putting cap on level of depth as its useless to go to depth 50 in 3*3 borad
		max_level = empty_squares(ogstate)+2

		while stop == 0 and depth_limit < max_level:
			flush_lookup_tree(lookup_tree)              # flushing lookup_tree
			lookup_entries = 0                          # initializing lookup_entries for current iteration
			new_depth += 1
			depth_limit = new_depth
			position = alpha_beta(ogstate, 0, -4, 4)
			if position[1] == 4:
				stop = 1
		stop = 1

		# printing the solution
		next_move = position[0]
		print "I will suggest next move in row ", (next_move/size + 1), " and column ", (next_move % size + 1)
		print "After that board will look like:"
		print "0 stands for empty square and 1 stands for square with pebble"

		ogstate[next_move/size][next_move % size] = 1

		if is_terminating_state(ogstate):
			print "I lose :("
		for c in ogstate:
			print c
		for i in ogstate:
			for j in i:
				if j == 0:
					sys.stdout.write(".")
				else:
					sys.stdout.write("x")
		print
		# print"--- seconds ---", time()-start_time


# .........................Main start here...........................

lookup_tree = Tree()
if __name__ == '__main__':

	start_time = time()
	# initializing various variables

	# taking arguments
	arg = sys.argv
	size = int(arg[1])
	given = arg[2]
	given_time = arg[3]

	lookup_entries = 0                                      # initialising count for lookup entries
	lookup_entries_bound = 1000000                          # setting bound for number of lookup entries
	cost = 0                                                # to know the cost the computational cost
	stop = 0                                                # to stop the thread which is computing the next best move
	depth_limit = 1                                         # defining parameters on which program will run
	number_of_squares = size*size                           # setting number of squares

	allowed_time = float(given_time)
	if allowed_time <= 0 or len(given) < number_of_squares:
		print "Invalid input"
	else:

		if len(given) > number_of_squares:
			print "Thought length of second argument is greater than valid input," \
				" I will calculate result after truncating it to required size"
		thread = Thread(target=solving_thread, args=(given,))   # creating computing thread to solve the problem
		thread.start()                                          # starting the thread

		# print allowed_time
		if allowed_time > 0.2:
			if allowed_time < 1:
				allowed_time -= 0.05
			elif allowed_time < 5:
				allowed_time -= 0.1
			elif allowed_time < 50:
				allowed_time *= 0.98
			elif allowed_time < 100:
				allowed_time *= 0.99
			else:
				allowed_time -= 1

		# print allowed_time

		while allowed_time-(time()-start_time) > 0 and stop == 0:
			sleep(0.01)

		stop = 1                                                # changing global variable value to stop computing thread
		depth_limit = -1                                        # changing global variable value to stop computations
		# print"--- seconds ---", time()-start_time
