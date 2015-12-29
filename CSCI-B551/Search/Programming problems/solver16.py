#!/usr/bin/python
'''
Problem Formulation:
	In this problem we have been given a 16 puzzle in which we have to design a program where we find a solution for the puzzle using astar algorithm.

Initial state:
	Any state of the puzzle with tiles arranged in a fashion such that they are mismatched and are not in there proper position can be initial state. It can be any state of the state space.

Action: Action in this problem is movement of tile in Left, Right, Up, or down by one position.

Transition Model: 	Transition model of this problem depends on action taken in the problem. As we know there are 4 actions on the tiles. 
			1. R2 --> This action will generate a result in which complete 2end row is shifted to right.
			2. D2 --> This action will generate a result in which complete 2end column is shifted down.
			3. U2 --> This action will generate a result in which complete 2end column is shifted up.
			4. D2 --> This action will generate a result in which complete 2end row is shifted to left.

State Space:		The state space for this problem is every possible outcome of the puzzle by using any possible move.

Edge Weight :		The edge weight here is considered as 1. Every step costs us 1 hence the edge weight is 1.

Goal State: 		In this puzzle the sorted puzzle where every element is at its correct position is the Goal State of the problem. It is given by:
			1 	2 	3 	4
			5 	6 	7 	8
			9 	10	11	12
			13	14	15	16

Successor Function:	successor function will chose the node having least value of cost+heuristics and explore it
			if it finds solution then it will remember its value and will try to find another efficient solution by exploring node have cost+heuristics less tha current solution value


Heuristic Function:	Its combination of modified manhatten distance and solutions to the subproblem
			
			Sub problem heuristics:
				divided problem into four parts:
					1to5, 5to9, 9to13, 13to16 and 1

				find number of steps required to each problem as:
					c(1to5), c(5to9), c(9to13), c(13to1)

				and chose only maximum of this as tiles are shifted in batch of 4 its not like 15 puzzle, there u can add cost of two subsolutions to get heuristics, here you cannnot


			thus Heuristic = max(modified manhatten distance,c(1to5), c(5to9), c(9to13), c(13to1))



			We have chosen heuristic as (Manhatten Distance/4). Manhatten distance is distance between the correct position of the tile and current position of tile. In this puzzle 				the heuristic by taking only Manhatten distance cannot be considered as admissible. This is because it may overestimate the cost of reching to goal state. For example:
			4	1	2	3
			5	6	7	8
			9	10	11	12
			13	14	15	16 

			in this the manhatten distance is given by 3+1+1+1. Where 3 is distance between its actual position and current position.
			But only one action which is R1 is enough for accomplishing goal state. Thus the heuristic is 6 and steps required is one. 
			Therefore we have taken (manhatten distance)/4 is admissible because maximum number of misplaced distance can be 4 and not more than dat. Hence it is admissible.

Algorithm:		Simple A* algorithm with heuristics build with combination of modified manhatten distance and solutions to the subproblems

'''

import sys
import copy
import Queue
import cPickle as pickle

class nodestruc:
	def __init__(self):
		self.state=[]
		self.hvalue=0
		self.pathlist=[]
		self.squaresize=0

def stringconvertor1to5(node):
	i=0
	j=0
	k=0
	l=0
	m=0
	for x in range(0,4):
		for y in range(0,4):
			if(node.state[x][y]==1):
				i=x*4+y
			if(node.state[x][y]==2):
				j=x*4+y
			if(node.state[x][y]==3):
				k=x*4+y
			if(node.state[x][y]==4):
				l=x*4+y
			if(node.state[x][y]==5):
				m=x*4+y
	return str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)

def stringconvertor1to5(node):
	i=0
	j=0
	k=0
	l=0
	m=0
	for x in range(0,4):
		for y in range(0,4):
			if(node.state[x][y]==1):
				i=x*4+y
			if(node.state[x][y]==2):
				j=x*4+y
			if(node.state[x][y]==3):
				k=x*4+y
			if(node.state[x][y]==4):
				l=x*4+y
			if(node.state[x][y]==5):
				m=x*4+y
	return str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)

def stringconvertor5to9(node):
	i=0
	j=0
	k=0
	l=0
	m=0
	for x in range(0,4):
		for y in range(0,4):
			if(node.state[x][y]==5):
				i=x*4+y
			if(node.state[x][y]==6):
				j=x*4+y
			if(node.state[x][y]==7):
				k=x*4+y
			if(node.state[x][y]==8):
				l=x*4+y
			if(node.state[x][y]==9):
				m=x*4+y
	return str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)

def stringconvertor9to13(node):
	i=0
	j=0
	k=0
	l=0
	m=0
	for x in range(0,4):
		for y in range(0,4):
			if(node.state[x][y]==9):
				i=x*4+y
			if(node.state[x][y]==10):
				j=x*4+y
			if(node.state[x][y]==11):
				k=x*4+y
			if(node.state[x][y]==12):
				l=x*4+y
			if(node.state[x][y]==13):
				m=x*4+y
	return str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)

def stringconvertor13to1(node):
	i=0
	j=0
	k=0
	l=0
	m=0
	for x in range(0,4):
		for y in range(0,4):
			if(node.state[x][y]==13):
				i=x*4+y
			if(node.state[x][y]==14):
				j=x*4+y
			if(node.state[x][y]==15):
				k=x*4+y
			if(node.state[x][y]==16):
				l=x*4+y
			if(node.state[x][y]==1):
				m=x*4+y
	return str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)

def huri1to5(node):
	return data1_5[stringconvertor1to5(node)]


def huri5to9(node):
	temp=shiftup(node)
	return data1_5[stringconvertor5to9(temp)]


def huri9to13(node):
	temp=shiftup(node)
	temp=shiftup(node)
	return data1_5[stringconvertor9to13(temp)]


def huri13to1(node):
	temp=shiftup(node)
	temp=shiftup(node)
	temp=shiftup(node)
	return data1_5[stringconvertor13to1(temp)]	


def huri0(node):
	hvalue=0
	x=0
	y=0
	xh=0
	yh=0
	value=0
	zero=0
	max=0
	for i in range(0,4):
		for j in range(0,4):
			value=node.state[i][j]-1
			y=value%4
			x=int(value/4)
			xh=abs(i-x)
			yh=abs(j-y)
			if(xh==3):
				xh=1
			if(yh==3):
				yh=1
			if(xh==0 and yh==0):
				zero=zero+1
			if(xh+yh)>max:
				max=xh+yh
			hvalue=hvalue+xh+yh
	return hvalue
	
def shiftup(node):
	temp=nodestruc()
	temp=copy.deepcopy(node)
	firstrow=[]
	for c in temp.state[0]:
		firstrow.append(c)
	for i in range(0,3):
		for j in range(0,4):
			temp.state[i][j]=temp.state[i+1][j]
	for i in range(0,4):
		temp.state[3][i]=firstrow[i]
	return temp


def huri(node):
	possible=[]
	possible.append(huri0(node))
	possible.append(huri1to5(node))
	possible.append(huri5to9(node))
	possible.append(huri9to13(node))
	possible.append(huri13to1(node))
	maximum=max(possible)
	return maximum+len(node.pathlist)*4
	
def child(parent):
	squaresize=parent.squaresize
	childs=[]
	i = 0
	vflag=0
	node=parent.state
	while(i<len(visited)):
		if visited[i]==node:
			vflag = 1
			break
		i = i + 1
	if(vflag==0):
		visited.append(node)
		#right row
		for i in range(squaresize,size):
			b=copy.deepcopy(node)
			temp=b[i][size-1]
			j=size-1
			while(j>0):
				b[i][j]=b[i][j-1]
				j=j-1
			b[i][0]=temp
			tempn=nodestruc()
			tempn.state=copy.deepcopy(b)
			tempn.pathlist=copy.deepcopy(parent.pathlist)
			tempn.pathlist.append("r"+str(i+1))
			tempn.hvalue=huri(tempn)
			childs.append(tempn)
		#left row
		for i in range(squaresize,size):
			b=copy.deepcopy(node)
			temp=b[i][0]
			j=0
			while(j<size-1):
				b[i][j]=b[i][j+1]
				j=j+1
			b[i][size-1]=temp
			tempn=nodestruc()
			tempn.state=copy.deepcopy(b)
			tempn.pathlist=copy.deepcopy(parent.pathlist)
			tempn.pathlist.append("l"+str(i+1))
			tempn.hvalue=huri(tempn)
			childs.append(tempn)
		#down column
		for i in range(squaresize,size):
			b=copy.deepcopy(node)
			temp=b[size-1][i]
			j=size-1
			while(j>0):
				b[j][i]=b[j-1][i]
				j=j-1
			b[0][i]=temp
			tempn=nodestruc()
			tempn.state=copy.deepcopy(b)
			tempn.pathlist=copy.deepcopy(parent.pathlist)
			tempn.pathlist.append("d"+str(i+1))
			tempn.hvalue=huri(tempn)
			childs.append(tempn)
		#up column
		for i in range(squaresize,size):
			b=copy.deepcopy(node)
			temp=b[0][i]
			j=0
			while(j<size-1):
				b[j][i]=b[j+1][i]
				j=j+1
			b[size-1][i]=temp
			tempn=nodestruc()
			tempn.state=copy.deepcopy(b)
			tempn.pathlist=copy.deepcopy(parent.pathlist)
			tempn.pathlist.append("u"+str(i+1))
			tempn.hvalue=huri(tempn)
			childs.append(tempn)
	return childs



#main
arg = sys.argv
fname = arg[1]
visited=[]
state=[]
line=[]
size=4
goal=[[1,2,3,4],
[5,6,7,8],
[9,10,11,12],
[13,14,15,16]]


#reading heuristics data from file
data1_5={}
f=open("data1to5.txt","r")
lines=f.read().split("\n")
tmp=[]
for i in lines:
	tmp=i.split(" ")
	if(len(tmp)==2):
		data1_5[tmp[0]]=int(tmp[1])
f.close()

f=open(fname,"r")
lines=f.read().split("\n")
for i in range(0,4):
	state.append(map(int,lines[i].split(" ")))

node=nodestruc()
node.state=copy.deepcopy(state)
nodelist=[]
nodelist.append(node)
"""
childs=child(node)
for c in childs:
	print "***"
	for x in c.state:
		print x
	print pathlist
"""
solfound=0

bound=-1
while len(nodelist)>0:
	node=nodelist.pop()
	if(bound==-1 or bound>node.hvalue):
		childlist=child(node)
		#print "h ", node.hvalue," bound ",bound, len(childlist)
		"""
		print "*"
		for c in node.state:
			print c
		"""
		for c in childlist:
			if c.state==goal:
				solfound=1
				print "found the solution"
				for x in c.state:
					print x
				print c.pathlist
				print c.hvalue
				print len(c.pathlist)
				if(bound==-1):
					bound=c.hvalue
				elif(bound>c.hvalue):
					bound=c.hvalue
		for c in childlist:
			nodelist.append(c)
		nodelist.sort(key=lambda nodestruc: nodestruc.hvalue, reverse=True)
