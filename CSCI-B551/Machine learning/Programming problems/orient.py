"""
========================================================================================================================
(1) a description of how you formulated the problem and how your solution works
========================================================================================================================
~~~ Problem Formulation:
	In simple words this is a classification problem where we have to assign the correct orientation to an image.
	Problem statement:
		We have to assign orientation to all the images in the test file and we are given a set of flickr images
		with the image vectors and respective orientation.
	Initial state:
		We are given one training data file which is used for creating the knowledge base of the problem. Then this training
		data set is used to find the orientation of the images according to the best possible match based on the classifying 
		algorithm.
      Action:
	  Read the training data file to create the learning data:
            1. Prepare matrices for storing the images and the vectors.
      Transition model:
                State                       action                             Result
                list of image ids			Prepare the classifier			All the images in the test set will
				and their orientations      and assign orientation          will be assigned with an orientation.
                given in the test file      to each image                   
				not present in the                              
				training set.

      Goal State:
                Assignment of orientation to all the images and calculation of accuracy of the classifier.
~~~How my solutions works~~~
	---------------------------------------------
	~~~Strategy for creating the learning data~~~
	---------------------------------------------
		For the training data set,
		we have created a matrix to store the
		corresponding vectors of the images and
		the given orientation.

	-----------------------------------------------------
	~~~Strategy for knn~~~~~~~~~~~~~~~~~~~~~~
	-----------------------------------------------------
		
		A. For every image present in the test file-
			a. Calculate the euclidean distance of the
				vectors with all the data present in the
				training data set.
			b. Store the distance with each of the image
				in the training data set.
			c. Sort the distance in increasing order.
			d. According to the k value given in the 
			   function call, take those k values of 
			   distance and assign the orientation with 
			   the least distance out of the k values.
	---------------------------------------------------------------------
	~~~Strategy for Neural Network Implementation~~~~~~~~~~~~~~~~~~~~~~~~
	---------------------------------------------------------------------
		A. First create a network with the below details-
			a. Input layer - 192 nodes (one for every vector of the image)
			b. Hidden Layer - configurable parameter.
			c. Output Layer - 4 nodes(One for each orientation)
				The output layer is stored in the form of
				binary arrays to decide the orientation
				based on the bit set to one out of the four 
				bits.
		B. Feedforward algorithm is used to calculate the value of the
			output layer nodes.
		C. Stocastic Gradient Descent algorithm is used to optimize the
			gradient descent.
		D. Sigmoid activation function is used to calculate the derivate
			for each of the vector and weight combination.
		C. Backpropagation algorithm is used update the weights after we
			get the result from the output layer as below-
		   a.Once we get the output with the output layer, we calculate
		     the difference between the calculated orientation and the
		     actual orientation.
		   b.Based on the derivative of sigmoid function and the above
		     calculated difference, we decide on the direction in which
		     the weights should be moved(increased or decreased).
		   c.Using this criteria, the weights input to the output layer
			 are changed and accordingly using back propagation, all the
			 weights in the network are modified.
	    D. We are repeating the above processes for a specific number of 
		   times to improve the accuracy of the orientations assigned.
	-----------------------------------------------------
	~~~Strategy for Best~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	-----------------------------------------------------
		Results of Neural Network were used to find the best
		approach.


========================================================================================================================
(2) the results of the evaluation on the test file / output
========================================================================================================================

	For this particular problem we can order the algorithms according to their accuracy in increasing order
	1) KNN
	2) Neural Network(Backpropagation and Stocastic Gradient Descent implementation)
	
========================================================================================================================
(3) a discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.
========================================================================================================================
~~~Problems faced~~~
	Optimizing the program and debugging the neural network program.
~~~Assumptions~~~
	We have normalized the data to avoid overflow.
~~~simplifications~~
	No special simplifications
~~~design decisions~~~
	Stocastic Gradient was used instead of traditional gradient descent to improve the accuracy.


========================================================================================================================
(4) Data sets
========================================================================================================================
	test-data.txt - Provided by Prof. David Crandall
	train-data.txt - Provided by Prof. David Crandall
	test-data-mini.txt - Provided by Prof. David Crandall
	train-data-mini.txt - Provided by Prof. David Crandall


========================================================================================================================
(5) References
========================================================================================================================
	1) http://neuralnetworksanddeeplearning.com/chap1.html
"""


import sys, random, numpy
from pqdict import PQDict
from os import path
import pickle
from shutil import copyfile
from time import time


class Neural:

	def __init__(self, weights):
		self.num_layers = 3
		self.weights = weights

	def feed_Forward(self, ac):
		for weight in self.weights:
			ac = sigmoid_value(numpy.dot(weight, ac))
		return ac

	def bkprop(self, data, alpha, iteration):
		starttime = time()
		for i in range(0, iteration):
			print "iteration", i
			self.weights = [nw + random.uniform(0.0, 0.00001) for nw in self.weights]
			temp_w = [numpy.zeros(w.shape) for w in self.weights]
			for x in data.tr_data:
				if x[0] == 0:
					tag = numpy.array([1, 0, 0, 0])
				elif x[0] == 90:
					tag = numpy.array([0, 1, 0, 0])
				elif x[0] == 180:
					tag = numpy.array([0, 0, 1, 0])
				elif x[0] == 270:
					tag = numpy.array([0, 0, 0, 1])
				inpt = numpy.zeros(shape=(data.t_d, 1), dtype=float)
				numpy.copyto(inpt, x[1:,None])

				activations = [inpt]
				zs = []
				for weight in self.weights:
					z = numpy.dot(weight, inpt)
					zs.append(z)
					inpt = sigmoid_value(z)
					activations.append(inpt)

				delta = (activations[-1] - tag[:,None])*sigmoid_derivative(z)
				temp_w[-1] = numpy.dot(delta, activations[-2].T)
				for layer in xrange(2, self.num_layers):
					delta = numpy.dot(self.weights[-layer+1].transpose(), delta) * sigmoid_derivative(zs[-layer])
					temp_w[-layer] = numpy.dot(delta, activations[-layer-1].T)
				self.weights = [weight-(alpha)*new_weight for weight, new_weight in zip(self.weights, temp_w)]
			self.evaluate_result(data)
		print "Time taken for training", time() - starttime
		return self.weights



	def evaluate_result(self, data):
		start_time = time()
		inpt = numpy.zeros(shape=(data.t_d, 1), dtype=float)
		correct = 0
		for row in data.tr_data:
			inpt = numpy.asarray(row[1:])
			result = self.feed_Forward(inpt[:,None])
			maximum = 0
			maxv = 0
			for i in range(0,4):
				if maxv < result[i][0]:
					maxv = result[i][0]
					maximum = i

			ans = maximum * 90
			if ans == row[0]:
				correct += 1

		print "accuracy in this iteration for training data: ", float(correct)/float(data.t_s), data.t_s

	def test(self):
		inpt = numpy.zeros(shape=(data.t_d, 1), dtype=float)
		correct = 0
		confusion = numpy.zeros(shape=(5,5), dtype=int)
		for i in range(0,4):
			confusion[0][i+1] = i*90
			confusion[i+1][0] = i*90
		f = open("nnet_output.txt","wb")
		for key in data.te_data:
			inpt = numpy.asarray(data.te_data[key][1:])
			result = self.feed_Forward(inpt[:,None])
			maximum = 0
			maxv = 0
			for i in range(0,4):
				if maxv < result[i][0]:
					maxv = result[i][0]
					maximum = i

			ans = maximum * 90
			confusion[data.te_data[key][0]/90+1][maximum+1] += 1
			f.write(key+" "+str(ans)+"\n")
			if ans == data.te_data[key][0]:
				correct += 1

		f.close()
		f = open("confusion_matrix_nnet.txt", "wb")
		f.write(str(confusion))
		f.close()
		print "accuracy is: ", float(correct)/float(len(data.te_data))*100, len(data.te_data)
		print "Confusion matrix is -"
		print confusion

class Data:

	def __init__(self, filename, test_file):
		self.t_s = 0
		self.t_d = 0
		self.tr_data = None
		self.te_data = {}
		with open(filename, 'r') as f:
			first_line = f.readline()
			self.t_d = len(first_line.split())-2

		with open(filename, 'r') as f:
			for _ in f:
				self.t_s += 1

		with open(filename, 'r') as fp:
			self.tr_data = numpy.zeros(shape=(self.t_s, self.t_d + 1)).astype(float)
			i = 0
			for row in fp:
				self.tr_data[i] = map(int, row.split()[1:])
				i += 1
		self.tr_data[:,1:] /= 256

		num_values = 0
		with open(test_file,'r') as fp:
			for row in fp:
				self.te_data[row.split()[0]] = map(int, row.split()[1:])
				num_values += 1

		for key in self.te_data:
			inp = self.te_data[key]
			for i in range(1,193):
				inp[i] = float(inp[i])/float(256)


def sigmoid_value(z):
	return 1.0/(1.0+numpy.exp(-z))

def sigmoid_derivative(z):
	return sigmoid_value(z)*(1-sigmoid_value(z))


class Classifier:

	def getdiff(self,tedata,trdata):
		value = 0
		for i in xrange(1,24,4):
			value += (tedata[i]-trdata[i])*(tedata[i]-trdata[i])
		for i in xrange(170,192,4):
			value += (tedata[i]-trdata[i])*(tedata[i]-trdata[i])
		for i in xrange(0,169,48):
			value += (tedata[i]-trdata[i])*(tedata[i]-trdata[i])
		for i in xrange(23,192,48):
			value += (tedata[i]-trdata[i])*(tedata[i]-trdata[i])

		return value

	def knn(self,test_file,k,data):
		start_time = time()
		orientation = {}
		bbtt = 0
		for x in data.te_data:
			result = []
			num = 0
			for i in range(0, data.t_s):
				value = self.getdiff(data.te_data[x][1:],data.tr_data[i][1:])
				if num < k:
					num += 1
					result.append([data.tr_data[i][0], value])
				else:
					for c in result:
						if c[1] > value:
							c[0] = data.tr_data[i][0]
							c[1] = value
							break
			bbtt += 1
			print "Done with", bbtt,"time elapsed", time() - start_time
			table2 = result
			orient = PQDict.maxpq()
			for j in range(0,k):
				count = 0
				key = table2[j][0]
				if key in orient:
					orient[key] += 1
				else:
					orient[key] = 1
			orientation[x] = orient.pop()

		count_correct = 0

		f = open('knn_output.txt','wb')
		confusion = numpy.zeros(shape=(5,5), dtype=int)
		for i in range(0,4):
			confusion[0][i+1] = i*90
			confusion[i+1][0] = i*90
		for x in data.te_data:
			f.write(str(x) + ' ' + str(int(orientation[x])) + '\n')
			confusion[int(data.te_data[x][0])/90 + 1][int(orientation[x])/90 + 1] += 1
			if data.te_data[x][0] == orientation[x]:
				count_correct += 1
		f.close()
		accuracy = float(float(count_correct)/float(len(data.te_data))) * 100
		end_time = time()
		time_taken = end_time - start_time
		print "confusion matrix"
		print confusion
		print "time taken for k = "  + str(k) +" is " + str(time_taken) + " seconds and accuracy is " + str(accuracy)


if __name__ == "__main__":
	if len(sys.argv) != 5 and len(sys.argv) != 4:
		print "Usage: python orient.py [train_file.txt] [test_file.txt] [algo name] [parameter]"
		sys.exit()
	train_file = sys.argv[1]
	test_file = sys.argv[2]

	data = Data(train_file,test_file)

	if sys.argv[3] == 'knn':
		k = int(sys.argv[4])
		Classifier().knn(test_file, k, data)
	elif sys.argv[3] == "nnet":
		k = int(sys.argv[4])
		o_file = "nnet_%s_model.txt" % k
		n_file = "nnet_%s_tmp_model.txt" % k
		v_file = "nnet_%s_validity.txt" % k
		if not path.isfile(o_file):
			f = open(o_file, "w+")
			wts = [numpy.random.randn(y, x) for x, y in zip([192, k, 4][:-1], [192, k, 4][1:])]
			pickle.dump(wts, f)
			f.close()
		if not path.isfile(n_file):
			f = open(n_file, "w+")
			f.close()
		if not path.isfile(v_file):
			f = open(v_file, "wb")
			f.write("0")
			f.close()

		with open(v_file, "r") as f:
			validity = int(f.read())

		if validity == 1:
			copyfile(n_file, o_file)
			f = open(v_file, "wb")
			f.write("0")
			f.close()

		with open(o_file, "r") as f:
			wts = pickle.load(f)

		neural_net = Neural(wts)

		new_weights = neural_net.bkprop(data, 0.1, 3)
		f = open(n_file, "wb")
		pickle.dump(new_weights, f)
		f.close()
		f = open(v_file, "wb")
		f.write("1")
		f.close()
		neural_net.test()
	elif sys.argv[3] == "best":
		k = 23
		o_file = "nnet_%s_model.txt" % k
		if not path.isfile(o_file):
			f = open(o_file, "w+")
			wts = [numpy.random.randn(y, x) for x, y in zip([192, k, 4][:-1], [192, k, 4][1:])]
			pickle.dump(wts, f)
			f.close()
		with open(o_file, "r") as f:
			wts = pickle.load(f)
		neural_net = Neural(wts)
		neural_net.test()
