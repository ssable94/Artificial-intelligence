"""

========================================================================================================================
(1) a description of how you formulated the problem and how your solution works
========================================================================================================================

~~~Problem formulation~~~

	Problem statement:
		In this problem we are rolling and twice re-rolling 5 dices for 13 times and after each rolling and twice
		re-rolling, dice combination is assigned a category and it will receive a particular score, depending on
		conditions of category and combination of dice a score will be assigned. and bonus is also given on meeting
		certain conditions. All this socres and if bonus received its summation will give final score for the game.

		Play the game 100 times and try to get higher value of min, max, and mean of scores of 100 games.

	Initial state:
		5 diced are rolled. all 13 categories are empty.

	action:
		if initially diced are rolled:
			chose dices for re-rolling depending upon available categories to fill
		if first re-roll has been done:
			chose dices for re-rolling depending upon available categories to fill
		if sencond re-roll has been done:
			select a category from available category in which this combination to put.
			Add category to selected category list (thus next time we will know that it is filled, so we can not
			fill it again)

	transition model:

		state						action				transition

		initial dice rolled 	->	chose dices to re-roll	->	dice once re-rolled
		(X categories available)

		dice once re-rolled	->	chose dices to re-roll	->	dice twice re-rolled

		dice twice re-rolled	->	chose category		->	end of chance
												(X-1 categories available)

		end of chance		->	if(x == 0):
								roll the dice	->	initial dice rolled (new game started)
												score = summation of score in all categories
							else:
								roll the dice	->	initial dice rolled (new chance started)

	Goal state:

		When game is played 100 times.

		We want to adjust code such that it will give higher values of min, max, and mean for the scores of game
		played.

~~~How my solutions works~~~

	-------------------------------
	~~~Strategy for rolling dice~~~
	-------------------------------

	I have used same piece of code to chose dices for re-rolling first time and second time.

	How dices were chose to re-roll:

	first choosing for "pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple", "quintupulo" this
	categories as achieving them is difficult than rest others.

	for catg = ["pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple", "quintupulo"]
	for catg each category:
		Based upon state of dice, probability and required re-roll set was calculated to reach that category
		category, re-roll set, and probability to reach that category was stored in data

		Ex:
		Dice Combination:
			6 4 1 6 1

		Data = [['triple',		[0, 3, 1],	0.4213],
			['elote',			[1],		0.16667],
			['pupusa de frijol',	[0, 2, 3],	0.13889],
			['cuadruple',		[0, 3, 1],	0.08796],
			['pupusa de queso',	[0, 2, 4],	0.02778],
			['quintupulo',		[0, 3, 1],	0.00463]]

	if data is not empty:
		then took out the list of categories whose probability value is maximum. (as two categories can have
		same value which is maximum value for probability in data)
		from this values best solution was found based on priority assigned to them

		Ex:
		Dice Combination:
			2 2 2 1 2

		Data = [['triple', [0, 3], 1],
			['cuadruple', [3], 1],
			['quintupulo', [3], 0.16667],
			['pupusa de frijol', [0, 1, 2], 0.13889],
			['pupusa de queso', [0, 1, 2], 0.02778]]

		Solutions = [['triple', [0, 3], 1],
				['cuadruple', [3], 1]]

		priority = { "pupusa de queso":240, "pupusa de frijol":420, "elote":300, "triple":1200, "cuadruple":150, "quintupulo":6}

		Hence,
		Best_solution = ['cuadruple', [3], 1]

	if Data is empty that means none of this "pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple",
	"quintupulo" categories were available

	Now chosing from:
	"unos", "doses", "treses", "cuatros", "cincos", "seises"

	will find numbers related to available category and then from those numbers we will chose number, which occurs the
	most.

	Ex:

	Dice combination:
		4 1 3 4 1

	clistp2 = ['cincos', 'unos', 'seises', 'doses']

	clispt2n = [5, 1, 6, 2]
	Numerical representation of available categories in clistp2

	count2 = [[1, 2], [5, 0], [6, 0], [2, 0]]
	sorted list of number of occurances of numerical representatoin of category in dice combination

	hence,
	best number = 1

	now we know the best number so chose the re-roll list as index of all the rest numbers. In the hope that they
	will give some more values of best number.

	Hence,
	re-roll list = [0, 2, 3]

	if both catg and clistp2 are empty
	that means
	only left category is "tamal"
	so for tamal just flip the dices with value less than 4.

	Ex:

	Dice combination:
		4 1 2 4 5

	re-roll = [1, 2]

	------------------------------------
	~~~strategy for choosing category~~~
	------------------------------------

	clistp2 = [ "unos", "doses", "treses", "cuatros", "cincos", "seises"]
	clistp1 = ["pupusa de queso", "pupusa de frijol", "elote", "triple", "cuadruple", "quintupulo"]
	Note: "tamal" not included it is kept as last option everytime.

	x = [score(clistp1[i], d) for i in range(0, len(clistp1))]
	y = [score(clistp2[i], d) for i in range(0, len(clistp2))]

	x -> stores score for dice combination for categories in clistp1
	y -> stores score for dice combination for categories in clistp2


	NOTE:
		Method to chose best solution in following pseudo code

		If we find two solutions giving the exact same score, then

		Following dictionaries were used as priority list, and value was chosen whose priority is least

		priority = { "pupusa de queso":240, "pupusa de frijol":420, "elote":300, "triple":1200, "cuadruple":150, "quintupulo":6}
		Numbers = { "unos" : 1, "doses" : 2, "treses" : 3, "cuatros" : 4, "cincos" : 5, "seises" : 6 }

	if clistp2 is not empty
		if clistp1 is not empty
			if max(x) == 0:	i.e., no category in clistp1 fulfils the requirement
				Chose the best solution in clistp2 and return it.
			else:			i.e., some category in clistp1 fulfils the requirement
				chose the best solution in clistp1 and return it
		else:
			Chose the best solution in clistp2 and return it.
	else:
		if clistp1 is not empty
			if max(x) != 0:	                   i.e., some category in clistp1 fulfils the requirement
				chose the best solution in clistp1 and return it
			else:
				here you have clistp2 empty and no category i clistp1 giving non-zero solution.
				So, you must chose the category from clistp1, which will give you score zero.

				So, category whose probability of satisfying a dice combination was low that was selected
				Ex:
					from:
						"pupusa de queso", "triple"
					"pupusa de queso" was chosen.


========================================================================================================================
(2) any problems you faced, assumptions you made, etc.
========================================================================================================================

~~~Problems faced~~~

	Alpha beta with chance for this problem is computationally expensive.
	Thus implemented dice re-rolling for level one deapth only

~~~Assumptions~~~

	All 13 categories need to be fill, you can leave any blank i.e., you can not chose same category twice

========================================================================================================================
(3) a brief analysis of how well your program works and how it could be improved in the future.
========================================================================================================================

~~~brief analysis of how well your program works~~~

	Sample output
		(for n=100)
		Final score: 205
		Min/max/mean scores: 119 317 196.65

	Mean value hovers around 196 approximately.
	Sample output
		(for n=10000)
		Final score: 144
		Min/max/mean scores: 76 324 195.734

	How program works well is relative term, thus providing rough idea about different aspects or program

	~~~computational complexity~~~
		only sort operation in all over the algorithm is of complextiy n(log n) or less depending how python
		implements the sort, rest all are O(n) or O(1).

		Also, probabilities are all precomputed thus code is much efficient.

		Approximate computational complexity = n * 6(log 6)					n -> number of games
								 = n							... as 6(log 6) is constant

			All the lists used in algorithm are of size 6 or less
			thus, sorting is done on list of maximum 6 elements

	~~~Space Complexity~~~
		it do not use any kind of special databases, thus it will require same amount of memory to compute results
		for 100 games or 1000 games

		hence,
		Space complexity = O(1)

	~~~Time complexity~~~
		code with highest time complexity -> sorting
		maximun size of list to be sorted -> 6
		hence complexity is proportinal to 6(log 6)

		Approximate computational complexity = n * 6(log 6) 					n -> number of games
								 = n             					... as 6(log 6) is constant

			All the lists used in algorithm are of size 6 or less
			thus, sorting is done on list of maximum 6 elements

	~~~Optimality~~~
		Solution is suboptimal
		As it searches till depth 1 only and does not implement any logic for achieving bonus.

	~~~Completeness~~~
		It is complete as it will return some value in particular time, time directly proportional to number of
		games to be played.

~~~Future improvements~~~

	It can be made to search till level 2
	Efficient algorithm can be implemented to get bonus.



========================================================================================================================


Sample output:  Just printing last 2 lines
	Final score: 205
	Min/max/mean scores: 119 317 196.65

"""

import random
from ZacateState import Scorecard


def chose_category(clist, d):
	if len(clist) == 1:
		return "tamal"
	clistp2 = [x for x in clist if x in Scorecard.Numbers]
	clistp1 = [x for x in clist if x not in clistp2]
	if "tamal" in clistp1:
		clistp1.remove("tamal")
	x = [score(clistp1[i], d) for i in range(0, len(clistp1))]
	y = [score(clistp2[i], d) for i in range(0, len(clistp2))]
	if clistp2:
		if clistp1:
			if max(x) == 0:				# return clistp2[y.index(max(y))]
				solutions = []
				for i in range(0,len(y)):
					if y[i] == max(y):
						solutions.append(clistp2[i])
				best_solution = solutions[0]
				for c in solutions:
					if Scorecard.Numbers[best_solution] > Scorecard.Numbers[c]:
						best_solution = c
				return best_solution
			else:						# return clistp1[y.index(max(y))]

				solutions = []
				for i in range(0,len(x)):
					if x[i] == max(x):
						solutions.append(clistp1[i])
				priority = { "pupusa de queso":240, "pupusa de frijol":420, "elote":300, "triple":1200, "cuadruple":150, "quintupulo":6}
				best_solution = solutions[0]
				for c in solutions:
					if priority[best_solution] > priority[c]:
						best_solution = c
				return best_solution
		else:							# return clistp2[y.index(max(y))]
			solutions = []
			for i in range(0,len(y)):
				if y[i] == max(y):
					solutions.append(clistp2[i])
			best_solution = solutions[0]
			for c in solutions:
				if Scorecard.Numbers[best_solution] > Scorecard.Numbers[c]:
					best_solution = c
			return best_solution
	else:
		if clistp1:
			if max(x) != 0:				# return clistp1[x.index(max(x))]
				solutions = []
				for i in range(0,len(x)):
					if x[i] == max(x):
						solutions.append(clistp1[i])
				priority = { "pupusa de queso":240, "pupusa de frijol":420, "elote":300, "triple":1200, "cuadruple":150, "quintupulo":6}
				best_solution = solutions[0]
				for c in solutions:
					if priority[best_solution] > priority[c]:
						best_solution = c
				return best_solution
			else:
				priority = [["pupusa de queso",240], ["pupusa de frijol",420], ["elote",300], ["triple",1200], ["cuadruple",150], ["quintupulo",6]]
				available = []
				for c in clistp1:
					for d in priority:
						if c == d[0]:
							available.append(d)
				available = sorted(available,key=lambda x: x[1])
				return available[0][0]

	#return random.choice(clist)


def dicestoroll(d,clist):
	dice = d.dice
	clistp3 = ["tamal" for x in clist if x == "tamal"]
	clistp2 = [x for x in clist if x in Scorecard.Numbers]
	clistp1 = [x for x in clist if x not in clistp3+clistp2]
	clistp2 = clistp2 + clistp3
	x = [score(clistp1[i], d) for i in range(0, len(clistp1))]

	data = []

	"""if x:
		if max(x) != 0:
			return []
"""

	if "pupusa de queso" in clist:
		desired1 = [[1, -1], [2, -1], [3, -1], [4, -1], [5, -1]]
		desired2 = [[2, -1], [3, -1], [4, -1], [5, -1], [6, -1]]
		for i in range(0, 5):
			for d in desired1:
				if dice[i] == d[0]:
					d[1] = i
		for i in range(0, 5):
			for d in desired2:
				if dice[i] == d[0]:
					d[1] = i
		re_rolld1 = list({0, 1, 2, 3, 4} - {x[1] for x in desired1})
		re_rolld2 = list({0, 1, 2, 3, 4} - {x[1] for x in desired2})
		re_roll = []
		if len(re_rolld2) > len(re_rolld1):
			re_roll = re_rolld1
		else:
			re_roll = re_rolld2
		probability = {0: 1, 1: 0.16667, 2: 0.05556, 3: 0.02778, 4: 0.01851, 5: 0.01543}
		data.append(["pupusa de queso", re_roll, probability[len(re_roll)]])

	if "pupusa de frijol" in clist:
		desired1 = [[1, -1], [2, -1], [3, -1], [4, -1]]
		desired2 = [[2, -1], [3, -1], [4, -1], [5, -1]]
		desired3 = [[3, -1], [4, -1], [5, -1], [6, -1]]
		for i in range(0, 5):
			for d in desired1:
				if dice[i] == d[0]:
					d[1] = i
		for i in range(0, 5):
			for d in desired2:
				if dice[i] == d[0]:
					d[1] = i
		for i in range(0, 5):
			for d in desired3:
				if dice[i] == d[0]:
					d[1] = i
		re_rolld1 = list({0, 1, 2, 3, 4} - {x[1] for x in desired1})
		re_rolld2 = list({0, 1, 2, 3, 4} - {x[1] for x in desired2})
		re_rolld3 = list({0, 1, 2, 3, 4} - {x[1] for x in desired3})
		re_roll = re_rolld1
		if len(re_roll) > len(re_rolld2):
			re_roll = re_rolld2
		if len(re_roll) > len(re_rolld3):
			re_roll = re_rolld3

		"""
			for n: number of numbers present in re_roll
			formula for probability to achieve a category:
				(n*permutation(n-1)*6 - (n*(n-1)^2)/2)/6^n
		"""
		probability = {0: 1, 1: 1, 2: 0.30555, 3: 0.13889, 4: 0.09722, 5: 0.08744}
		data.append(["pupusa de frijol", re_roll, probability[len(re_roll)]])
	if "elote" in clist:
		counts = sorted([[i ,dice.count(i)] for i in range(1, 7)],key=lambda x: x[1], reverse=True)
		probability = 0

		re_roll = []
		if counts[0][1] == 5:
			re_roll.append(0)
			re_roll.append(1)
			probability = 0.13889			# 5/36
		elif counts[0][1] == 4:
			re_roll.append(dice.index(counts[1][0]))
			probability = 0.16667			# 1/6
		elif counts[0][1] == 3:
			probability = 1				# 1 satisfy the condition
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[2][0]))
				probability = 0.16667		# 1/6

		elif counts[0][1] == 2:
			probability = 0.16667			# 1/6
			re_roll.append(dice.index(counts[2][0]))
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[3][0]))
				probability = 0.19444		# 7/36
		elif counts[0][1] == 1:
			re_roll.append(0)
			re_roll.append(1)
			re_roll.append(2)
			probability = 0.02778			# 6/216
		data.append(["elote", re_roll, probability])

	if "triple" in clist:
		counts = sorted([[i ,dice.count(i)] for i in range(1, 7)],key=lambda x: x[1], reverse=True)
		probability = 0

		re_roll = []
		if counts[0][1] == 5:
			if counts[0][0] < 4:
				re_roll.append(0)
				re_roll.append(1)
			probability = 1				# 1 satisfies the condition
		elif counts[0][1] == 4:
			if counts[0][0] < 4:
				re_roll.append(dice.index(counts[0][0]))
			if counts[1][0] < 4:
				re_roll.append(dice.index(counts[1][0]))
			probability = 1				# 1 satisfies the condition
		elif counts[0][1] == 3:
			if counts[1][0] < 4:
				for i in range(0,5):
					if dice[i] == counts[1][0]:
						re_roll.append(i)
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[2][0]))
			probability = 1				# 1 satisfy the condition
		elif counts[0][1] == 2:
			probability = 0.42130			# (6^3 - 5^3)/6^3
			for i in range(0,5):
				if dice[i] == counts[1][0]:
					re_roll.append(i)
			for i in range(0,5):
				if dice[i] == counts[2][0]:
					re_roll.append(i)
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[3][0]))
				probability = 0.42130		# (6^3 - 5^3)/6^3
		elif counts[0][1] == 1:
			re_roll = [0,1,2,3,4]
			re_roll.remove(dice.index(max(dice)))
			probability = 0.13194			# 171/6^4
		data.append(["triple", re_roll, probability])

	if "cuadruple" in clist:
		counts = sorted([[i ,dice.count(i)] for i in range(1, 7)],key=lambda x: x[1], reverse=True)
		probability = 0

		re_roll = []
		if counts[0][1] == 5:
			if counts[0][0] < 4:
				re_roll.append(0)
			probability = 1				# 1 satisfies the condition
		elif counts[0][1] == 4:
			if counts[1][0] < 4:
				re_roll.append(dice.index(counts[1][0]))
			probability = 1				# 1 satisfies the condition
		elif counts[0][1] == 3:
			for i in range(0,5):
				if dice[i] == counts[1][0]:
					re_roll.append(i)
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[2][0]))
			probability = 0.30556			# 11/36
		elif counts[0][1] == 2:
			for i in range(0,5):
				if dice[i] == counts[1][0]:
					re_roll.append(i)
			for i in range(0,5):
				if dice[i] == counts[2][0]:
					re_roll.append(i)
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[3][0]))
			probability = 0.08796			# 19/216
		elif counts[0][1] == 1:
			re_roll = [0,1,2,3,4]
			re_roll.remove(dice.index(max(dice)))
			probability = 0.01929			# 25/6^4
		data.append(["cuadruple", re_roll, probability])

	if "quintupulo" in clist:
		counts = sorted([[i ,dice.count(i)] for i in range(1, 7)],key=lambda x: x[1], reverse=True)
		probability = 0

		re_roll = []
		if counts[0][1] == 5:
			probability = 1				# 1 satisfies the condition
		elif counts[0][1] == 4:
			re_roll.append(dice.index(counts[1][0]))
			probability = 0.16667			# 1/6
		elif counts[0][1] == 3:
			for i in range(0,5):
				if dice[i] == counts[1][0]:
					re_roll.append(i)
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[2][0]))
			probability = 0.02778			# 1/36
		elif counts[0][1] == 2:
			for i in range(0,5):
				if dice[i] == counts[1][0]:
					re_roll.append(i)
			for i in range(0,5):
				if dice[i] == counts[2][0]:
					re_roll.append(i)
			if counts[1][1] == 1:
				re_roll.append(dice.index(counts[3][0]))
			probability = 0.00463			# 1/216
		elif counts[0][1] == 1:
			re_roll = [0,1,2,3,4]
			re_roll.remove(dice.index(max(dice)))
			probability = 0.00077			# 1/6^4
		data.append(["quintupulo", re_roll, probability])


	if data:
		data = sorted(data,key=lambda x: x[2], reverse=True)
		# sorted(data,key=lambda x: x[2], reverse=True)
		solutions = []
		solutions.append(data[0])
		for i in range(1,len(data)):
			if data[0][2] == data[i][2]:
				solutions.append(data[i])
		priority = { "pupusa de queso":240, "pupusa de frijol":420, "elote":300, "triple":1200, "cuadruple":150, "quintupulo":6}
		best_solution = solutions[0]
		for c in solutions:
			if priority[best_solution[0]] > priority[c[0]]:
				best_solution = c
		return best_solution[1]
		#return data[0][1]
	"""
	"""

	if "tamal" in clistp2:
		clistp2.remove("tamal")

	chose = -1
	if clistp2:
		clistp2n = [Scorecard.Numbers[x] for x in clistp2]
		counts2 = sorted([[i ,dice.count(i)] for i in clistp2n],key=lambda x: x[1], reverse=True)
		chose = counts2[0][0]

		print "*********************"
		print clistp2
		print clistp2n
		print counts2

	if chose == 1:
		re_roll = []
		for i in range(0,5):
			if dice[i] != 1:
				re_roll.append(i)
		return re_roll
	elif chose == 2:
		re_roll = []
		for i in range(0,5):
			if dice[i] != 2:
				re_roll.append(i)
		return re_roll
	elif chose == 3:
		re_roll = []
		for i in range(0,5):
			if dice[i] != 3:
				re_roll.append(i)
		return re_roll
	elif chose == 4:
		re_roll = []
		for i in range(0,5):
			if dice[i] != 4:
				re_roll.append(i)
		return re_roll
	elif chose == 5:
		re_roll = []
		for i in range(0,5):
			if dice[i] != 5:
				re_roll.append(i)
		return re_roll
	elif chose == 6:
		re_roll = []
		for i in range(0,5):
			if dice[i] != 6:
				re_roll.append(i)
		return re_roll

	if "tamal" in clist:
		re_roll = []
		for i in range(0,5):
			if dice[i] < 4:
				re_roll.append(i)
		return re_roll
	return []


def score(category, d):
	dice = d.dice
	counts = [dice.count(i) for i in range(1, 7)]
	if category in Scorecard.Numbers:
		return counts[Scorecard.Numbers[category]-1] * Scorecard.Numbers[category]
	elif category == "pupusa de queso":
		return 40 if sorted(dice) == [1,2,3,4,5] or sorted(dice) == [2,3,4,5,6] else 0
	elif category == "pupusa de frijol":
		return 30 if (len(set([1,2,3,4]) - set(dice)) == 0 or len(set([2,3,4,5]) - set(dice)) == 0 or len(set([3,4,5,6]) - set(dice)) == 0) else 0
	elif category == "elote":
		return 25 if (2 in counts) and (3 in counts) else 0
	elif category == "triple":
		return sum(dice) if max(counts) >= 3 else 0
	elif category == "cuadruple":
		return sum(dice) if max(counts) >= 4 else 0
	elif category == "quintupulo":
		return 50 if max(counts) == 5 else 0
	elif category == "tamal":
		return sum(dice)