"""
========================================================================================================================
(1) a description of how you formulated the problem and how your solution works
========================================================================================================================
~~~ Problem Formulation:
	In simple words this is part of speech tagging problem, in which we have to tag all the words in a sentence according
	to the given part of speech tags.
	Problem statement:
		We have to assign tags to all the words in all the sentences given in the test file. We are required to perform
		the tagging using 5 different algorithms and then find the best one in the end.
	Initial state:
		We are given one training data file which is used for creating the knowledge base of the problem. Then this training
		data set is used to tag the words in all the sentences of the test file.
      Action:
                Read the training data file to create the learning data:
                        1. Prepare different tables for P(S1), P(Si+1|Si), and P(Wi|Si).
				2. Use these tables and the algos to tag the words in the test file.
      Transition model:
                State                   action                  Result
                list of sentences       Assign tags to all      all the words are tagged
				list of nodes with      words.                  according to the algo and
                with some words                                 the available training data
				not present in the                              set.
				training set.

      Goal State:
                Assignment of part of speech tags to all the words.
~~~How my solutions works~~~
	---------------------------------------------
	~~~Strategy for creating the learning data~~~
	---------------------------------------------
		For every sentence in the training data
		file.
		Read the words and their tags and prepare
		below tables for further use in the other
		algos for tagging.

		P(S1)
		Frequency of one tag occuring for a word
		with respect to the all the tags for the
		same word.


		P(Si+1|Si)
		The frequency of one tag given the
		previous tag.


		P(Wi|Si)
		This is done by observing the frequency of
		a tag appearing for every word in training
		file.

	-----------------------------------------------------
	~~~Strategy for naive inference~~~~~~~~~~~~~~~~~~~~~~
	-----------------------------------------------------
		Here, there are two cases:
		A. When the word is not present in training set:
			a. If the word has some digit, assign the
				tag 'det' to the word.
			b. If the word is first word in sentence:
				Just assign the tag which has occurred max
				for this word.
			c. If the word is not the first word,
				Use the tag of the previous word in the
				sentence. And then assign the tag which has
				occurred max for this combination of word
				and previous tag.
		B. When the word is present in the training set:
			Use the tag assigned to the prev word and then
			assign the tag which has max probability of
			occurrence given the current word and the
			previous tag.
	-----------------------------------------------------------
	~~~Strategy for Sampling - Gibbs(MCMC)~~~~~~~~~~~~~~~
	-----------------------------------------------------------
		Take a sample list.

		Take some initial sample, randomly assign some
		tags to the words in each sentence.
		Append this sample to the Sample list

		For every other sample:
			Copy the previous sample and modify the tags
			based on the calculation below;
				for the first word in the sentence:
					a.Assigning a tag depends only on the
					  probability of the current tag and
					  the current word.
					b.Calculate the probability of
					  occurrence of each tag for the current
					  word, multiply it with the probability
					  of that tag.
					c.Now choose a random number between 0 & 1.
					d.Look for the index in the above created
					  matrix where the value is less than or
					  equal to the random number.
					e.Assign the tag corresponding to that index
					to the word.
				for the rest of the words:
					a.Assining a tag will depend on the tag of the
					  previous word and the probability of occurrence
					  of each tag given the word.
					b.Do this for all the tags in the list.
					c.Now choose a random number between 0 & 1.
					d.Look for the index in the above created
					  matrix where the value is less than or
					  equal to the random number.
					e.Assign the tag corresponding to that index
					to the word.
			Append the sample to the Sample List.

		Once all the samples are calculated(we can take any number
		of samples greater than 5), output the last sample in the
		Sample List as this will approximately give the correct
		tagging result.


	-----------------------------------------------------
	~~~Strategy for Approximate max marginal inference~~~
	-----------------------------------------------------
		Using the Gibbs sampling Generate the set of
		samples

		Now for each word find the tag which occurs the
		most in the generated samples and assign it to
		the word.

		And posterior for that tag is number of times
		that tag occured divided by total number of
		samples

	-----------------------------------------------------
	~~~Strategy for Viterbi~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	-----------------------------------------------------
		Viterbi is dynamic algoirthm. It calculates best
		sequences of tag till n words and then using this
		data it calculate most favoriable tag for next word

		create table of size number of tags*length of
		sentence
		for w=0, calculate es(w) for each tag and store
		it into table say at column v0
		for next words calculate
		es(w) * 1<=i<=N max (vj-1(t) p(si|si-1))
		and store it into column vj
		and keep an edge pointing to previous entry from
		which max was selected.

		After completion of the algorithm find the maximum
		value for last word, chose the tag corresponding to
		that max value, now backtrack to find tags for previous
		tags.

	-----------------------------------------------------
	~~~Strategy for Best~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	-----------------------------------------------------
		Results of Viterbi were used to find the best
		approach.


========================================================================================================================
(2) the results of the evaluation on the bc.test file / output
========================================================================================================================

	Following it the output of the program on bc.test file

	==> So far scored 1993 sentences with 29351 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.67%
		  2. Sampler:       93.59%               46.36%
	   3. Max marginal:       95.19%               55.75%
			4. MAP:       95.80%               58.30%
		     5. Best:       95.80%               58.30%
	----
					  : he   stopped ,    embarrassed ,    and  morgan said ,    ``   i    understand that ,    but  i    don't savvy why  you'd go   off  and  leave your jobs in   the  first place ''   .
	 0. Ground truth (-190.50): pron verb    .    verb        .    conj noun   verb .    .    pron verb       det  .    conj pron verb  verb  adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
		  1. Naive (-191.57): pron verb    .    verb        .    conj noun   verb .    .    pron verb       adp  .    conj pron verb  noun  adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
		2. Sampler (-191.18): pron verb    .    verb        .    conj noun   verb .    .    pron verb       pron .    conj pron verb  prt   adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
			     (-191.52): pron verb    .    verb        .    conj noun   verb .    .    pron verb       adp  .    conj pron verb  adp   adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
			     (-191.15): pron verb    .    verb        .    conj noun   verb .    .    pron verb       det  .    conj pron verb  adv   adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
			     (-189.32): pron verb    .    verb        .    conj noun   verb .    .    pron verb       pron .    conj pron verb  adv   adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
			     (-189.32): pron verb    .    verb        .    conj noun   verb .    .    pron verb       pron .    conj pron verb  adv   adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
	 3. Max marginal (-188.67): pron verb    .    verb        .    conj noun   verb .    .    pron verb       pron .    conj pron verb  verb  adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
					  : 1.0  1.0     1.0  1.0         1.0  1.0  1.0    1.0  1.0  1.0  1.0  1.0        0.6  1.0  0.98 1.0  1.0   0.4   1.0  1.0   1.0  1.0  1.0  1.0   1.0  1.0  1.0  1.0  1.0   1.0   1.0  1.0
		    4. MAP (-190.73): pron verb    .    verb        .    conj noun   verb .    .    pron verb       pron .    conj pron verb  noun  adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .
		   5. Best (-190.73): pron verb    .    verb        .    conj noun   verb .    .    pron verb       pron .    conj pron verb  noun  adv  prt   verb prt  conj verb  det  noun adp  det  adj   noun  .    .

	==> So far scored 1994 sentences with 29383 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.64%
		  2. Sampler:       93.59%               46.34%
	   3. Max marginal:       95.19%               55.72%
			4. MAP:       95.79%               58.27%
		     5. Best:       95.79%               58.27%
	----
					  : ``   we   got  fired ''   ,    jones said .
	 0. Ground truth ( -56.34): .    pron verb verb  .    .    noun  verb .
		  1. Naive ( -56.34): .    pron verb verb  .    .    noun  verb .
		2. Sampler ( -56.34): .    pron verb verb  .    .    noun  verb .
			     ( -56.34): .    pron verb verb  .    .    noun  verb .
			     ( -56.34): .    pron verb verb  .    .    noun  verb .
			     ( -56.34): .    pron verb verb  .    .    noun  verb .
			     ( -56.34): .    pron verb verb  .    .    noun  verb .
	 3. Max marginal ( -56.34): .    pron verb verb  .    .    noun  verb .
					  : 1.0  1.0  1.0  1.0   1.0  1.0  1.0   1.0  1.0
		    4. MAP ( -56.34): .    pron verb verb  .    .    noun  verb .
		   5. Best ( -56.34): .    pron verb verb  .    .    noun  verb .

	==> So far scored 1995 sentences with 29392 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.67%
		  2. Sampler:       93.59%               46.37%
	   3. Max marginal:       95.19%               55.74%
			4. MAP:       95.79%               58.30%
		     5. Best:       95.79%               58.30%
	----
					  : ``   we   had  to   do   something ''   .
	 0. Ground truth ( -39.71): .    pron verb prt  verb noun      .    .
		  1. Naive ( -39.71): .    pron verb prt  verb noun      .    .
		2. Sampler ( -39.71): .    pron verb prt  verb noun      .    .
			     ( -39.71): .    pron verb prt  verb noun      .    .
			     ( -39.71): .    pron verb prt  verb noun      .    .
			     ( -39.71): .    pron verb prt  verb noun      .    .
			     ( -39.71): .    pron verb prt  verb noun      .    .
	 3. Max marginal ( -39.71): .    pron verb prt  verb noun      .    .
					  : 1.0  1.0  1.0  0.98 1.0  1.0       1.0  1.0
		    4. MAP ( -39.71): .    pron verb prt  verb noun      .    .
		   5. Best ( -39.71): .    pron verb prt  verb noun      .    .

	==> So far scored 1996 sentences with 29400 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.70%
		  2. Sampler:       93.60%               46.39%
	   3. Max marginal:       95.19%               55.76%
			4. MAP:       95.80%               58.32%
		     5. Best:       95.80%               58.32%
	----
					  : they were a    pair of   lost ,    whipped kids ,    morgan thought as   he   went to   bed  .
	 0. Ground truth (-116.47): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb adp  noun .
		  1. Naive (-117.46): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb prt  noun .
		2. Sampler (-117.46): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb prt  noun .
			     (-117.58): pron verb det  noun adp  verb .    verb    noun .    noun   noun    adp  pron verb adp  noun .
			     (-118.02): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adv  pron verb adp  noun .
			     (-116.47): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb adp  noun .
			     (-117.58): pron verb det  noun adp  verb .    verb    noun .    noun   noun    adp  pron verb adp  noun .
	 3. Max marginal (-116.47): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb adp  noun .
					  : 1.0  1.0  1.0  1.0  1.0  1.0  1.0  1.0     0.96 1.0  1.0    0.74    0.9  1.0  1.0  0.68 1.0  1.0
		    4. MAP (-116.47): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb adp  noun .
		   5. Best (-116.47): pron verb det  noun adp  verb .    verb    noun .    noun   verb    adp  pron verb adp  noun .

	==> So far scored 1997 sentences with 29418 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.67%
		  2. Sampler:       93.60%               46.37%
	   3. Max marginal:       95.19%               55.78%
			4. MAP:       95.80%               58.34%
		     5. Best:       95.80%               58.34%
	----
					  : gavin paused wearily .
	 0. Ground truth ( -38.81): noun  verb   adv     .
		  1. Naive ( -38.81): noun  verb   adv     .
		2. Sampler ( -38.81): noun  verb   adv     .
			     ( -38.81): noun  verb   adv     .
			     ( -38.81): noun  verb   adv     .
			     ( -38.81): noun  verb   adv     .
			     ( -38.81): noun  verb   adv     .
	 3. Max marginal ( -38.81): noun  verb   adv     .
					  : 1.0   1.0    1.0     1.0
		    4. MAP ( -38.81): noun  verb   adv     .
		   5. Best ( -38.81): noun  verb   adv     .

	==> So far scored 1998 sentences with 29422 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.70%
		  2. Sampler:       93.60%               46.40%
	   3. Max marginal:       95.19%               55.81%
			4. MAP:       95.80%               58.36%
		     5. Best:       95.80%               58.36%
	----
					  : ``   you  can't stay here with me   .
	 0. Ground truth ( -50.01): .    pron verb  verb adv  adp  pron .
		  1. Naive ( -50.01): .    pron verb  verb adv  adp  pron .
		2. Sampler ( -50.01): .    pron verb  verb adv  adp  pron .
			     ( -50.01): .    pron verb  verb adv  adp  pron .
			     ( -50.01): .    pron verb  verb adv  adp  pron .
			     ( -50.01): .    pron verb  verb adv  adp  pron .
			     ( -50.01): .    pron verb  verb adv  adp  pron .
	 3. Max marginal ( -50.01): .    pron verb  verb adv  adp  pron .
					  : 1.0  1.0  1.0   0.96 1.0  1.0  1.0  1.0
		    4. MAP ( -50.01): .    pron verb  verb adv  adp  pron .
		   5. Best ( -50.01): .    pron verb  verb adv  adp  pron .

	==> So far scored 1999 sentences with 29430 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.96%               47.72%
		  2. Sampler:       93.60%               46.42%
	   3. Max marginal:       95.20%               55.83%
			4. MAP:       95.80%               58.38%
		     5. Best:       95.80%               58.38%
	----
					  : it's late and  you  said they'd be   here by   dawn ''   .
	 0. Ground truth ( -78.87): prt  adv  conj pron verb prt    verb adv  adp  noun .    .
		  1. Naive ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
		2. Sampler ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
			     ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
			     ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
			     ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
			     ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
	 3. Max marginal ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
					  : 1.0  0.76 1.0  1.0  1.0  1.0    1.0  1.0  1.0  1.0  1.0  1.0
		    4. MAP ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .
		   5. Best ( -77.76): prt  adj  conj pron verb prt    verb adv  adp  noun .    .

	==> So far scored 2000 sentences with 29442 words.
				 Words correct:     Sentences correct:
	   0. Ground truth:      100.00%              100.00%
		    1. Naive:       93.95%               47.70%
		  2. Sampler:       93.60%               46.40%
	   3. Max marginal:       95.19%               55.80%
			4. MAP:       95.80%               58.35%
		     5. Best:       95.80%               58.35%
	----

	For this particular problem we can order the algorithms according to their accuracy in increasing order
	1) Naive
	2) Sampler
	3) Max marginal
	4) Map / Viterbi
	4) Best / Viterbi

========================================================================================================================
(3) a discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.
========================================================================================================================
~~~Problems faced~~~
	None. Initially we did not have the idea how to handle the words not present in the training set. Later we assigned
	each tag some constant probability for such words.
~~~Assumptions~~~
	When a word is not present in the training set, the probability of a tag given this word, is assumed to be 1/12
	instead of 0.
~~~simplifications~~
	No special simplifications
~~~design decisions~~~
	No special design decisions

========================================================================================================================
(4) Features of the program
========================================================================================================================
	~~~Handling of the numbers:
		it checkes if the word is number of not if it is then it will replace it by string "1".
		thus, all the numbers are mapped to "1"
		and every seen or unseen number will the correct tag as "num"
	~~~Cache Implementation:
		Implemented cache to store the intermediates result during mcmc sampling making algorithm faster.

========================================================================================================================
(4) Data sets
========================================================================================================================
	bc.test - Provided by Prof. David Crandall
	bc.test.tiny - Provided by Prof. David Crandall
	bc.train - Provided by Prof. David Crandall
"""

import numpy,re,random
import math

class smartsolver:

	def __init__(self):
		self.word_dict = {}
		self.word_dict_reverse = {}
		self.pos_dict = {}
		self.pos_dict_reverse = {}
		self.word_count = 0
		self.pos_count = 0
		self.ProbTables = {}
		self.defaultWordProbability = 0.00
		self.cache = {}

	def getFromDict(self,dataDict, mapList):
		try:
			value = reduce(lambda d, k: d[k], mapList, dataDict)
			return value
		except:
			return None

	def setInDict(self,given_dataDict, given_maplist, value):
		if len(given_maplist) == 1:
			given_dataDict[given_maplist[0]] = value
		else:
			if given_maplist[0] in given_dataDict:
				newmaplist = given_maplist[1:][:]
				self.setInDict(given_dataDict[given_maplist[0]], newmaplist,value)
			else:
				i=len(given_maplist)-1
				while i > 0:
					new_dict = {given_maplist[i]:value}
					value = new_dict
					i -= 1
				given_dataDict[given_maplist[0]]=value

	def is_number(self,s):
		try:
			float(s)
			return True
		except ValueError:
			return False

	def smarttrain(self,data):

		for (s, gt) in data:
			for word in s:
				if word not in self.word_dict:
					if self.is_number(word):
						self.word_dict["1"] = self.word_count
						self.word_dict_reverse[self.word_count] = "1"
					else:
						self.word_dict[word] = self.word_count
						self.word_dict_reverse[self.word_count] = word
					self.word_count += 1
			for tag in gt:
				if tag not in self.pos_dict:
					self.pos_dict[tag] = self.pos_count
					self.pos_dict_reverse[self.pos_count] = tag
					self.pos_count += 1

		table1 = numpy.zeros(shape=(self.word_count, self.pos_count)).astype(int)

		for (s ,gt) in data:
			for i in range(0, len(s)):
				table1[self.word_dict[s[i]]][self.pos_dict[gt[i]]] += 1
		table8 = table1.sum(axis=1)
		table9 = numpy.zeros(shape=self.word_count).astype(float)
		wordcount = table1.sum()
		for i in range(0, self.word_count):
			table9[i] = float(table8[i])/float(wordcount)
		self.defaultWordProbability = table9.min()


		table3 = table1.sum(axis=0)
		total = 0
		for (s, gt) in data:
			total += len(s)
		table2 = numpy.zeros(shape=(1, self.pos_count)).astype(float)
		for i in range(0,self.pos_count):
			table2[0][i] = float(table3[i])/float(total)

		table4 = numpy.zeros(shape=(self.pos_count, self.pos_count)).astype(float)
		for (s, gt) in data:
			for i in range(1, len(gt)):
				table4[self.pos_dict[gt[i-1]]][self.pos_dict[gt[i]]] += 1
		table5 = table4.sum(axis=1)


		for i in range(0, self.pos_count):
			for j in range(0, self.pos_count):
				table4[i][j]=float(table4[i][j])/float(table5[i])
		table6 = numpy.zeros(shape=(self.pos_count, self.pos_count)).astype(float)
		numpy.copyto(table6, table4)
		table7 = table6.sum(axis = 0)
		for i in range(0, self.pos_count):
			for j in range(0, self.pos_count):
				table6[j][i] = float(table6[j][i])/float(table7[i])

		self.ProbTables["CountWordTag"] = table1
		self.ProbTables["ProbTag"] = table2
		self.ProbTables["CountTag"] = table3
		self.ProbTables["ProbTagSet"] = table4
		self.ProbTables["ProbTagSetTranspose"] = table6
		self.ProbTables["PorbWord"] = table9

		return self.ProbTables

	def naiveAlgo(self, sentence):
		result = []
		for i in range(0,len(sentence)):
			probability = -1
			for j in range(0,self.pos_count):
				prob = self.esiwi(j,sentence[i])*self.wsi(j)
				if prob > probability:
					probability = prob
					tag = self.pos_dict_reverse[j]
			result.append(tag)
		return [[result],[]]

	def wsi(self, i):
		return self.ProbTables["ProbTag"][0][i]

	def esiwi(self, tag_index, word):
		if word in self.word_dict:
			word_tag_count = self.ProbTables["CountWordTag"][self.word_dict[word]][tag_index]
			tag_count = self.ProbTables["CountTag"][tag_index]
			return float(word_tag_count)/float(tag_count)
		else:
			return 1.0/12.0

	def psiminus1si(self, tag_index1, tag_index2):
		return self.ProbTables["ProbTagSetTranspose"][tag_index1][tag_index2]
	def psiplus1si(self, tag_index1, tag_index2):
		return self.ProbTables["ProbTagSet"][tag_index1][tag_index2]

	def smartviterbibacha(self,sentence):
		smarttree = numpy.zeros(shape=(self.pos_count,len(sentence),2))

		for i in range(0, self.pos_count):
			smarttree[i][0][1] = -1

		max = 0
		for i in range(0, self.pos_count):
			value = self.wsi(i)*self.esiwi(i,sentence[0])
			if value > max:
				max = value
			smarttree[i][0][0] = value

		for i in range(0, self.pos_count):
			smarttree[i][0][0] = smarttree[i][0][0]/max


		for t in range(1,len(sentence)):
			max_column = 0
			for s in range(0, self.pos_count):
				max_value = 0
				esiwi = self.esiwi(s,sentence[t])
				if esiwi != 0:
					for olds in range(0, self.pos_count):
						val = smarttree[olds][t-1][0]*self.ProbTables["ProbTagSet"][olds][s]
						if val > max_value:
							max_value = val
							smarttree[s][t][0] = val
							smarttree[s][t][1] = olds
				smarttree[s][t][0] *= esiwi
				if smarttree[s][t][0] > max_column:
					max_column = smarttree[s][t][0]
			for s in range(0, self.pos_count):
				smarttree[s][t][0] = smarttree[s][t][0]/max_column

		max_value = 0
		max_index = 0
		for s in range(0, self.pos_count):
			if smarttree[s][len(sentence)-1][0] > max_value:
				max_value = smarttree[s][len(sentence)-1][0]
				max_index = s

		result = ["noun"] * len(sentence)
		result[len(sentence)-1] = self.pos_dict_reverse[max_index]

		t = len(sentence)-1
		while t >= 1:
			max_index = smarttree[max_index][t][1]
			result[t-1] = self.pos_dict_reverse[max_index]
			t -= 1
		return result

	def smartviterbipappa(self, sentence):
		presence = numpy.zeros(shape=(len(sentence)+1)).astype(int)
		result = ["noun"] * len(sentence)
		for i in range(0,len(sentence)):
			if sentence[i] in self.word_dict:
				presence[i] = 1
			else:
				presence[i] = 0

		start = 0
		pairs = []
		while start < len(sentence):
			if presence[start] == 0:
				start += 1
			else:
				break

		if start != len(sentence):
			pairs.append(start)
			for i in range(start+1,len(presence)):
				if presence[i] != presence[i-1]:
					if presence[i] == 1:
						pairs.append(i)
					else:
						pairs.append(i-1)
		i = 0
		while i<len(pairs):
			temp = self.smartviterbibacha(sentence[pairs[i]:(pairs[i+1]+1)])
			for j in range(pairs[i],(pairs[i+1]+1)):
				result[j] = temp[j-pairs[i]]
			i += 2
		return [[result], []]

	def gettag(self, WordTag):
		for j in range(1, self.pos_count):
				WordTag[j] = WordTag[j-1] + WordTag[j]

		sum = WordTag[-1]
		if sum == 0:
			for j in range(0, self.pos_count):
				WordTag[j] = 1.0/12.0
		else:
			for j in range(0, self.pos_count):
				WordTag[j] = WordTag[j]/sum

		randomIndex = random.random()
		outputIndex = 0
		for k in range(self.pos_count):
			if randomIndex <= WordTag[k]:
				outputIndex = k
				break
		return self.pos_dict_reverse[outputIndex]

	def smartMcmc(self, sentence, count):
		senlen = len(sentence)
		initialSample = []
		for i in range(0, senlen):
			initialSample.append(self.pos_dict_reverse[random.randint(0,11)])
		WordTag = numpy.zeros(shape=self.pos_count).astype(float)

		SampleList = []
		SampleList.append(initialSample)
		for samples in range(1,count):

			presample = SampleList[-1][:]
			SampleList.append(presample)

			for i in range(0,senlen):
				for j in range(self.pos_count):
					p_t = self.pos_dict[SampleList[-1][i-1]] if (i != 0) else self.pos_count
					n_t = self.pos_dict[SampleList[-1][i+1]] if (i != senlen-1) else self.pos_count
					savedwordtag = self.getFromDict(self.cache, [sentence[i],p_t,j,n_t])
					if savedwordtag is not None:
						for g in range(0, self.pos_count):
							WordTag[g]= savedwordtag[g]
					else:
						psi = self.wsi(j)
						pwisi = self.esiwi(j,sentence[i])
						psiminus1si = self.psiminus1si(p_t,j) if (i != 0) else 1
						psiplus1si = self.psiplus1si(j,n_t) if (i != senlen-1) else 1
						WordTag[j] = psi * pwisi * psiminus1si * psiplus1si
						storing = numpy.zeros(shape=self.pos_count).astype(float)
						for g in range(0, self.pos_count):
							storing[g]=WordTag[g]
						self.setInDict(self.cache,[sentence[i],p_t,j,n_t],storing)
				SampleList[samples][i] = self.gettag(WordTag)

		return SampleList



	def smartMcmcold(self, sentence, count):
		count = count + 5
		initialSample = []
		for i in range(0, len(sentence)):
			initialSample.append(self.pos_dict_reverse[random.randint(0,11)])
		WordTag = numpy.zeros(shape=((len(sentence)), self.pos_count)).astype(float)

		SampleList = []
		SampleList.append(initialSample)
		for samples in range(1,count):
			presample = SampleList[-1][:]
			SampleList.append(presample)
			for j in range(self.pos_count):
				WordTag[0][j] = self.esiwi(j,sentence[0])*self.wsi(j)
				if len(sentence) > 1:
					WordTag[0][j] *= float(self.ProbTables["ProbTagSetTranspose"][j][self.pos_dict[SampleList[-1][1]]])

			for j in range(1, self.pos_count):
				WordTag[0][j] = WordTag[0][j-1] + WordTag[0][j]
			for j in range(0, self.pos_count):
				if WordTag.sum() == 0:
					WordTag[0][j] = 1.0/12.0
				else:
					WordTag[0][j] = WordTag[0][j]/WordTag[0][self.pos_count -1]

			randomIndex = random.random()
			outputIndex = 0
			for k in range(self.pos_count):
				if randomIndex <= WordTag[0][k]:
					outputIndex = k
					break
			SampleList[samples][0] = self.pos_dict_reverse[outputIndex]

			a = range(1,len(sentence))
			random.shuffle(a)
			for i in a:
				for j in range(self.pos_count):
					WordTag[i][j] = self.esiwi(j,sentence[i]) * self.esiwi(j,sentence[i]) * self.wsi(j)
					if i != len(sentence)-1:
						WordTag[i][j] *= float(self.ProbTables["ProbTagSetTranspose"][j][self.pos_dict[SampleList[-1][i+1]]])

				for y in range(self.pos_count):
					if WordTag.sum() == 0:
						WordTag[i][y] = 1.0/12.0
					else:
						WordTag[i][y] = float(float(WordTag[i][y]) / float(WordTag.sum()))

				for j in range(1, self.pos_count):
					WordTag[i][j] = WordTag[i][j-1] + WordTag[i][j]

				randomIndex = random.random()

				outputIndex = 0
				for k in range(self.pos_count):
					if randomIndex <= WordTag[i][k]:
						outputIndex = k
						break

				SampleList[samples][i] = self.pos_dict_reverse[outputIndex]

		return SampleList

	def smartmaxmarginal(self, sentence):
		samplecount = 100
		using = 50
		samples = self.smartMcmc(sentence, samplecount)[-using:]
		countmatrix = numpy.zeros(shape=(len(sentence), self.pos_count), dtype = int)
		for i in range(0,using):
			for j in range(0, len(sentence)):
				countmatrix[j][self.pos_dict[samples[i][j]]] += 1
		tagsum = countmatrix.sum(axis=1)
		tagmax = countmatrix.max(axis=1)
		solution = countmatrix.argmax(axis=1)
		values =[]
		solutiontags = []
		for c in range(0, len(sentence)):
			values.append(float(tagmax[c])/float(tagsum[c]))
			solutiontags.append(self.pos_dict_reverse[solution[c]])
		return [ [ solutiontags], [values] ]

	def smartposterior(self, sentence, label):
		result = 0
		for i in range(0, len(sentence)):
			value = self.esiwi(self.pos_dict[label[i]],sentence[i])
			if value != 0:
				result += math.log(value)
		value = self.wsi(self.pos_dict[label[0]])
		if value != 0:
			result += math.log(value)
		for i in range(1, len(sentence)):
			value = self.ProbTables["ProbTagSet"][self.pos_dict[label[i-1]]][self.pos_dict[label[i]]]
			if value != 0:
				result += math.log(value)
		"""
		for i in range(0, len(sentence)):
			if sentence[i] in self.word_dict:
				value = self.ProbTables["PorbWord"][self.word_dict[sentence[i]]]
			else:
				value = self.defaultWordProbability
			if value != 0:
				result -= math.log(value)
		"""
		return result#self.defaultWordProbability