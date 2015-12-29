"""
========================================================================================================================
(1) a description of how you formulated the problem and how your solution works
========================================================================================================================
~~~ Problem Formulation:
	In simple words this is basically graph coloring problem with few nodes in graph already colored.

	Problem statement:
		We have to assign each state a frequency such that no two neighbouring states will have same frequency.
			Some states have transmitters which can only transmit particular frequency.

	Initial state:
		list of all states with list of their neighbours and possible frequency for the transmittors in that state.

      Action:
                Chose one state according to:
                        Least number of values in the domain,
                        then according to degree of node.

                        if we have multiple nodes after above two constrains chose any one node.
                        Now create list of colors in  least constraining order.

		Chose colors from this list serially
		and assign color to node, remove that color from its neighbours and check arc consistacny.
		if not possible then backtrack.

      Transition model:
                State                   action                  Result
                list of nodes           Give color to           list of nodes with
                with some nodes         selected node           one less node with
                no assigned             remove that color       no frequency assigned
                frequency               from neighbours
                                        available frequency
                                        list
      Goal State:
                All states assigned particular freqency such that no two neighbouring states having same frequency.
                With following constrains given initially.
                
~~~How my solutions works~~~

	-------------------------------
	~~~Strategy for choosing node~~~
	-------------------------------
		Least number of values in the domain,
		then according to degree of node.

		If we get list of multiple states, then chose first state in the list.

	---------------------------------
	~~~strategy for choosing color~~~
	---------------------------------
		Make list of available in frequency for chosen state in least constraining order.
		Now chose color from the list serially


	--------------
	~~~coloring~~~
	--------------
		Give a frequency to chosen node and remove that frequency from its neighbous.

	---------------------
	~~~arc consistency~~~
	---------------------
		checked if given assignment is valid or not using arc consistency.

	If it is not possible to assign frequency to a give state, then backtrack.

========================================================================================================================
(2) any problems you faced, assumptions you made, etc.
========================================================================================================================

~~~Problems faced~~~

	None. Its a standard algorithm graph coloring algorithms, thus no problems were faced while coding.

~~~Assumptions~~~

	No special assumptions.

========================================================================================================================
(3) a brief analysis of how well your program works and how it could be improved in the future.
========================================================================================================================

~~~brief analysis of how well your program works~~~

	~~~computational complexity~~~
		It depends on number of nodes backtracked. Number of nodes backtrack depend on how sequence in which input
		was provided and in which order we chose nodes to assign colors.

		Thus, it will vary greatly ranging from n to  n^d
		n -> number of states
		d -> number of possible frequencies

	~~~Space Complexity~~~
		it like depth first search
		Space complexity = O(nd)

	~~~Time complexity~~~
		it is similar to computational complexity

		Thus, it will vary greatly ranging from n to  n^d
		n -> number of states
		d -> number of possible frequencies

	~~~Optimality~~~
		No concept of optimality in this algorithm

	~~~Completeness~~~
		It is complete as it will find solution if there is any, and if their is no solution it will find that
		there is no solution

~~~Future improvements~~~

	Maybe better data structures can be used

========================================================================================================================
(4) Features of the program.
========================================================================================================================

1) Used all three constrains:
	For chosing state:
		1. Most constraining variable
		2. Most constrained variable
	For chosing color:
		3. Least constraining value

2) Arc consistency: (optimized)
	Used arc consistency to check whether given assignment will lead to valid solution or not.
	which is one of the best algorithm.

	Optimization was done by not checking all the pairs in the state.
	Only the state which was assigned a color and its neighbours were checked in arc consistency,
	As only there state in arc consistency will be changed.

3) Efficient backtracking:
	Backtracking was made efficient by modifying the algorithm to restore the state to original state if
	coloring was not possible.

	restoring was done by storing minimum number of states.
"""



import sys
from city import City
from time import time


def is_coloring_possible(given_states, given_id, given_color):
	if given_states[given_id].color_it(given_color) == -1:
		return -1
	for node in given_states[given_id].ngb:
		given_states[node].remove_color(given_color)
	if arc_node(given_states, given_id) == -1:
		return -1
	if -1 in [arc_node(given_states, x) for x in given_states[given_id].ngb]:
		return -1
	return 1


def arc_node(given_states, given_id):
	if given_states[given_id].color == 0:
		if given_states[given_id].rvalue > 1:
			return 1
		if given_states[given_id].rvalue == 0:
			return -1
		for node in given_states[given_id].ngb:
			if given_states[node].color == 0:
				if given_states[node].rvalue == 1:
					if given_states[node].color_list[0] == given_states[given_id].color_list[0]:
						return -1
	return 1


def color_in_increasing_constrain_order(given_states, given_id):
	return [a for a, b in sorted([[x,len([x for ngb in given_states[given_id].ngb if x in given_states[ngb].color_list])] for x in given_states[given_id].color_list], key=lambda tup: tup[1])]


def find_colors(given_states):
	rvalue_set = [x.rvalue for x in given_states if x.rvalue != 0]
	if not rvalue_set:
		return 1

	min_rvalue = min(rvalue_set)
	min_rvalue_set = [i for i in range(0,len(given_states)) if given_states[i].rvalue == min_rvalue]
	max_degree = max([given_states[x].degree for x in min_rvalue_set])
	max_degree_list = [i for i in min_rvalue_set if given_states[i].degree == max_degree]
	chosen = max_degree_list[0]

	for color in color_in_increasing_constrain_order(given_states,chosen):
		restore = [[node, City(given_states[node].ngb[:], given_states[node].color,given_states[node].color_list[:])] for node in[chosen]+given_states[chosen].ngb]
		if is_coloring_possible(given_states, chosen, color) == 1:
			if find_colors(given_states) == 1:
				return 1
			else:
				for node in restore:
					given_states[node[0]] = node[1]
		else:
			for node in restore:
				given_states[node[0]] = node[1]
			global backtrack
			backtrack += 1
	return -1


if __name__ == '__main__':
	start_time, backtrack, states, states_dict, proceed, reverse_state_dict = time(), 0,  [], {}, 1, {}
	with open("adjacent-states") as f:
		content = f.readlines()
		for i in range(0, len(content)):
			states_dict[(content[i].rstrip()).split()[0]] = i
			reverse_state_dict[i] = (content[i].rstrip()).split()[0]
		for i in range(0, len(content)):
			states.append(City([states_dict[k] for k in (content[i].rstrip()).split()[1:]], 0, [1, 2, 3, 4]))

	with open(sys.argv[1]) as f:
		content = f.readlines()
		colors = {"A": 1, "B": 2, "C": 3, "D": 4}
		reverse_color = {1: "A", 2: "B", 3: "C", 4: "D"}
		for i in range(0, len(content)):
			spt = content[i].rstrip().split()
			if len(spt) > 1:
				if is_coloring_possible(states, states_dict[spt[0]], colors[spt[1]]) == -1:
					print "With given constraints it is not possible to do assignment"
					proceed = -1

	if (find_colors(states) == -1) or (proceed == -1):
		print "Coloring not possible"
	else:
		print "Time took:", time()-start_time
		f = open('result.txt', 'w')
		for i in range(0, 50):
			f.write('{} {}\n'.format(reverse_state_dict[i],reverse_color[states[i].color]))
		f.close()
		print "Number of backtracks:", backtrack
