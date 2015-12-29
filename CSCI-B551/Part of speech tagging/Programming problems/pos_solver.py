# CS B551 Fall 2015, Assignment #5
# Based on skeleton code by D. Crandall


import random
import math
from smartcode import smartsolver

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
	def __init__(self):
		self.ss = smartsolver()
		self.viterbioutput = None

	def posterior(self, sentence, label):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return self.ss.smartposterior(sentence,label)
		#return 0

	# Do the training!
	#
	def train(self, data):
		newdata = []
		for a in data:
			newdata.append([list(a[0]),list(a[1])])

		for a in newdata:
			for i in range(0, len(a[0])):
				if self.ss.is_number(a[0][i]):
					#print a
					a[0][i] = "1"
			"""
			for word in s:
				if self.ss.is_number(word):
					word = "1"
			"""
		self.ss.smarttrain(newdata)

	# Functions for each algorithm.
	#
	def naive(self, sentence):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return self.ss.naiveAlgo(sentence)

	def mcmc(self, sentence, sample_count):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return [ self.ss.smartMcmc(sentence, sample_count*2)[-sample_count:], [] ]
		#[ [ [ "noun" ] * len(sentence) ] * sample_count, [] ]

	def best(self, sentence):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		if self.viterbioutput is None:
			self.viterbioutput = self.ss.smartviterbipappa(sentence)
			result = self.viterbioutput[:]
		else:
			result = self.viterbioutput[:]
			self.viterbioutput = None
		return result

	def max_marginal(self, sentence):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		return self.ss.smartmaxmarginal(sentence)
		#return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

	def viterbi(self, sentence):
		sentence = list(sentence)
		for i in range(0, len(sentence)):
			if self.ss.is_number(sentence[i]):
				sentence[i] = "1"
		if self.viterbioutput is None:
			self.viterbioutput = self.ss.smartviterbipappa(sentence)
			result = self.viterbioutput[:]
		else:
			result = self.viterbioutput[:]
			self.viterbioutput = None
		return result
		#return [ [ [ "noun" ] * len(sentence)], [] ]


	# This solve() method is called by label.py, so you should keep the interface the
	#  same, but you can change the code itself.
	# It's supposed to return a list with two elements:
	#
	#  - The first element is a list of part-of-speech labelings of the sentence.
	#    Each of these is a list, one part of speech per word of the sentence.
	#    Most algorithms only return a single labeling per sentence, except for the
	#    mcmc sampler which is supposed to return 5.
	#
	#  - The second element is a list of probabilities, one per word. This is
	#    only needed for max_marginal() and is the marginal probabilities for each word.
	#
	def solve(self, algo, sentence):
		if algo == "Naive":
			return self.naive(sentence)
		elif algo == "Sampler":
			return self.mcmc(sentence, 5)
		elif algo == "Max marginal":
			return self.max_marginal(sentence)
		elif algo == "MAP":
			return self.viterbi(sentence)
		elif algo == "Best":
			return self.best(sentence)
		else:
			print "Unknown algo!"

