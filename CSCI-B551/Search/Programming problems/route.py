#!/user/bin/python
'''
Problem Formulation:
Current problem is path finding problem. In this problem user will be giving certain set of input and based on that input the program finds particular path to reach to the goal state.

Initial stage---> 	Initial state in this problem is the location of of any city given in the state space. This is the state which represents the start city.

Action---> 		Action is this problem can be given as movement from one city to another city. 

Transition Model---> 	the transition model of this problem is the result of implementing the action on the current state of the problem. Here, the result of implementing the 			transition model leads to change of state of the problem. The city of changes from current city to next city. The state can only transition from one city to 				another only if there is direct path available between the two cities otherwise we have to carry out this transition is sequence of steps.

State space ---> 	The State Space for the current problem is location of all the nummber of possible cities which can be reached from a starting city either through a single transition 		or multiple transtions.

Goal state---> 		The goal state of the problem is the second argument provided by the user in the input. This argument is treated as the destination city or goal city where we 				want to reach from initial state.

*Succesor Function ---> Successor function for this problem is defined as
			Next state = Current State + Cost required to go to the next state

Edge Weight --> 	In our problem we have to find path to particular node for 3 different parameters: 1.Distance 2.Time 3.Edges Travelled
			Thus inorder to satisfy the 3 parameters, we defined edge weight differently for all the 3 parameters. When the path was to be found using minimum distance, we 			used distance between 2 cities as edge weight of the graph. Although we also kept track of rest of the 2 parameters but path was found using the required 				parameter. Similarly for finding path using time we used  the formula (time = Distance/Speed) where Distance and speed is given to us in the text file and this 			'time' was used as edge weight. And for edges the edge weight was kept as integer 1 inorder to keep count of the edges travelled by us. 

Heuristic Function ---> A* algorithm required a well defined heuristic function for implementation. The City-Gps.txt file consisted of longitudes and latitudes of cities. We treated the 				longitude and latitude of the city as its coordinates and using Euclidian's Distance formula we calculated the straight line distance between 2 cities. This 				straight line distance was used as Heuristics in our problem. This straight line distance is an admissible heuristic and this can be proved as follow:
			Any admissible heuristic is a heuristic which doesn't over estimates the cost of path between the starting City and the ending city. In our heuristic we have 				calculated straight line distance. Any distance between two points can never be less than the straight distance between them. This distance is the straight 				distance between two points where the two points are 2 cities. Thus the distance or the path can cost more than our heuristic or straight line distance but can 			never be less than this heuristic. Thus, our heuristic is an admissible heuristic.
			Our Heuristic function can be represented as:
			
			H(n) = Square root((longitude_of_city1 -longitude_of_city2)^2 - (latitude_of_city1 -latitude_of_city2)^2)
			
Working of Breadth first search Algorithm:
			This algorithm here creates a special node for every particular city we visit and store all its details in that node. We accept start and destination , along 				with routing option. it works like a normal bfs algorithm where a list of sorted child node is generated in a different function and return it. Now this list is 				appended in queue and one city is dequeued. Every dequeud city is checked if it is end city and if yes the path is returned. if not then all its childrens are 				checked and expanded.

Working of Depth first search Algorithm:
			This algorithm here creates a special node for every particular city we visit and store all its details in that node. We accept start and destination , along 				with routing option. it works like a normal dfs algorithm where a list of sorted child node is generated in a different function and return it. Now this list is 				pushed in stack and one city is popped. Every popped city is checked if it is end city and if yes the path is returned. if not then the city is expanded unless 			we get the goal city or no other city can be searched.

Working of Astar search Algorithm:
			This algorithm here creates a special node for every particular city we visit and store all its details in that node. We accept start and destination , along 				with routing option. In astar we initially find the child node with minimum value of function i.e. f(n), which is given by f(n) = g(n)+h(n). And expand that node 				until we find the goal city. aster finding the goal city we display the path.

Rest of the work---> 	Initially, a very first challenge was to create a datastructure such that we can store contents of the file in that and which can be accessed efficiently for 				operstions. Python provides list, list class, tuples and other datstructure. We used lists and classes mainly. After developing the algorithm and code we 				realised there were many inconsistancies in the given data and had to resolve them such that inspite of its presence our code must work properly. In this, very 			important was calculating heuristic of cities which aren't present in city-gps.txt. Because we did not have longitude and latitude of those cities. Therefore we 				found the nearest city whose heuristic was available and reduced the distance between current city and nearest city from the heuristic of nearest city. This made 				us available the approximate straight line distance of the city from goal.  



===============================================================================================
Data sets
	city-gps.txt - Provided by prof. David Crandall
	raod-segemts.txt - Provided by prof. David Crandall
'''



import copy
import sys
import Queue
import math


class city:

	def __init__(self,string,longi, lati):	
		self.name = string
		self.longitude = longi
		self.latitude = lati
		self.h = 0		
		self.cost=0	

	def adh(self,h):
		self.h = h



fc = open('city-gps.txt','r')
citystr = fc.read()
citydetail = citystr.split('\n')

totalcities = len(citydetail)

cit = []

i=0
while (i<totalcities-1):
	citydetailsplit=citydetail[i].split(' ')
	scity = city(citydetailsplit[0],citydetailsplit[1],citydetailsplit[2])
	cit.append(scity)
	i = i+1

'''
Now City details
'''

class road:

	def __init__(self,start,dest,dist,speed,road):	
		self.start=start
		self.dest=dest
		self.dist=dist
		self.speed=speed
		self.road=road
	


fp = open('road-segments.txt','r')
citystr = fp.read()
roaddetail = citystr.split('\n')
roaddetail.pop()
roadlst = []
i = 0
for i in roaddetail:
	lst = i.split(' ')
	roadt = road(lst[0],lst[1],lst[2],lst[3],lst[4])
	roadlst.append(roadt)
	roadt = road(lst[1],lst[0],lst[2],lst[3],lst[4])
	roadlst.append(roadt)



'''
The bfs implementation
'''


fringe = Queue.Queue()
visited = []

class generalnode:
	def __init__(self,start,cost,path,time,edge):
		self.start = start
		self.cost = cost
		self.path = path
		self.time = time
		self.edge = edge

def findchild(node,param):
	child = []
	pathl = []
	time =0
	for i in range(0,len(roadlst)):
		if (roadlst[i].start==node.start):
			if roadlst[i].dest in visited:
				pass
			else:
				pathl=copy.deepcopy(node.path)
				pathl.append(node.start)
				try:
					time = (float(roadlst[i].dist)/float(roadlst[i].speed))
				except:
					if(roadlst[i].dist=='0'):
						time = 0
					elif(roadlst[i].speed=='' and roadlst[i].dist!='0'):
						break
					
				child.append(generalnode(roadlst[i].dest,node.cost+int(roadlst[i].dist),pathl,node.time+time,node.edge+1))

	if param=='distance':
		child.sort(key=lambda x: x.cost, reverse=True)
	elif param =='time':
		child.sort(key=lambda x: x.time, reverse=True)
	if param=='segments':
		child.sort(key=lambda x: x.cost, reverse=True)
	
	return child

		
def bfs(start,end,param):

	fringe = Queue.Queue()
	node = generalnode(start,0,copy.deepcopy([]),0,0)
	mini=-1
	while(node.start!=end):
		for i in range(0,len(roadlst)):
			if(roadlst[i].start==node.start):
				child=findchild(node,param)
				for n in child:
					fringe.put(n)
		node = fringe.get()
		visited.append(node.start)
	node.path.append(end)
	print 'path =', node.path, 'Cost =', node.cost, 'time =',round(node.time,2),'Hrs','Edges: ',node.edge+1

'''
DFS Implementation
'''

	
def dfschild(node,param):
	child = []
	pathl = []
	time =0
	for i in range(0,len(roadlst)):
		if (roadlst[i].start==node.start):
			if roadlst[i].dest in visited:
				pass
			else:
				pathl=copy.deepcopy(node.path)
				pathl.append(node.start)
				try:
					time = (float(roadlst[i].dist)/float(roadlst[i].speed))
				except:
					if(roadlst[i].dist=='0'and roadlst[i].speed=='0'):
						time = 0
					elif(roadlst[i].speed=='0' and roadlst[i].dist!='0'):
						break
					elif(roadlst[i].speed!='0'and roadlst[i].dist=='0'):
						time=0					

				child.append(generalnode(roadlst[i].dest,node.cost+int(roadlst[i].dist),pathl,node.time+time,node.edge+1))

	if param=='distance':
		child.sort(key=lambda x: x.cost, reverse=False)
	elif param =='time':
		child.sort(key=lambda x: x.time, reverse=False)
	elif param=='segments':
		child.sort(key=lambda x: x.cost, reverse=False)

	return child


def dfs(start,end,param):

	fringe = []
	node = generalnode(start,0,copy.deepcopy([]),0,0)
	while(node.start!=end):
		for i in range(0,len(roadlst)):
			if(roadlst[i].start==node.start):
				child=dfschild(node,param)
				for n in child:
					fringe.append(n)
		node = fringe.pop()
		visited.append(node.start)
	node.path.append(end)
	print 'path =', node.path, 'Cost =', node.cost, 'time =',round(node.time,2),'Hrs','Edges: ',node.edge+1
	




'''
Now astar
'''
def huri(start,current):
	hval=0


	pstart=-1
	pcurrent=-1
	for i in range(0,len(cit)):
		if cit[i].name==start:
			pstart=i
	for i in range(0,len(cit)):
		if cit[i].name==current:
			pcurrent=i
	if pstart!=-1 and pcurrent!=-1:
		hval = math.sqrt(pow((float(cit[pstart].longitude)-float(cit[pcurrent].longitude)),2)+pow((float(cit[pstart].latitude)-float(cit[pcurrent].latitude)),2))
		hval = round(hval,2)
		return hval

	if pstart==-1 and pcurrent!=-1:
		minim=-1
		node = road('','','','','')
		for k in roadlst:
			for c in cit:
				if c.name==k.dest:
					if(minim==-1):
						if(k.start==n.start):
							minim=float(k.dist)
							node = k
					elif(minim>int(k.dist)):
						if(k.start==n.start):
							minim=float(k.dist)
							node = k
		return (huri(node,current)-node.dist)

	if pstart!=-1 and pcurrent==-1:
		minim=-1
		node = road('','','','','')
		for k in roadlst:
			for c in cit:
				if c.name==k.dest:
					if(minim==-1):
						if(k.start==current):
							minim=float(k.dist)
							node = k
					elif(minim>int(k.dist)):
						if(k.start==current):
							minim=float(k.dist)
							node = k
		return (huri(start,node)-node.dist)
	if pstart!=-1 and pcurrent!=-1:
		minim=-1
		node = road('','','','','')
		for k in roadlst:
			for c in cit:
				if c.name==k.dest:
					if(minim==-1):
						if(k.start==current):
							minim=float(k.dist)
							node = k
					elif(minim>int(k.dist)):
						if(k.start==current):
							minim=float(k.dist)
							node = k
		return (huri(start,node)-node.dist)


class astarnode():
	def __init__(self,start,cost,huri,pathlist):
		self.start=start
		self.cost=cost
		self.huri=huri
		self.pathlist=pathlist


def child(start,node):
	childs=[]
	for n in roadlst:
		if n.start==node.start:
			pathl=copy.deepcopy(node.pathlist)
			pathl.append(node.start)
			childs.append(astarnode(n.dest,node.cost+int(n.dist),huri(start,node.start),pathl))
	return childs
		
def astar(start,end):
	solution=astarnode(None,-1,-1,None)
	huri=0
	for n in cit:
		if n.name==start:
			huri=n.h

	startnode=astarnode(start,0,huri,copy.deepcopy([]))
	nodelist=[]
	nodelist.append(startnode)
	i=0
	mini=0
	childs=[]
	while bool(nodelist):
		currentnode=nodelist[mini]
		nodelist.remove(currentnode)
		if(currentnode.start==end):
			if solution.cost==-1:
				solution=copy.deepcopy(currentnode)
			elif solution.cost>currentnode.cost:
				solution=copy.deepcopy(currentnode)
		if(solution.cost==-1 or solution.cost>(currentnode.cost+currentnode.huri)):
			nodelist=nodelist+copy.deepcopy(child(start,currentnode))
		if bool(nodelist):
			mini = 0	
			for i in range(0,len(nodelist)):
				if((nodelist[mini].cost+nodelist[mini].huri)>(nodelist[i].cost+nodelist[i].huri)):
					mini=i
	solution.pathlist.append(end)
	print solution.pathlist,' ', solution.cost

arg = sys.argv
start = arg[1]
end = arg[2]
routing = arg[3]
algo = arg[4]

if algo == "astar":
	astar(start,end)
elif algo == "bfs":
	bfs(start, end,routing)
elif algo == "dfs":
	dfs(start, end,routing)

