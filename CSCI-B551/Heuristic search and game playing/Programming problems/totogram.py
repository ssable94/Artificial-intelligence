"""
Elements of Artificial Intelligence
Assignment 2
Question 2.2:

~~~Problem Statement~~~

    A Totogram is a puzzle played on a board that has a graph structure, with edges connecting some pairs
    of vertices. The edges of the graph form a rooted tree with a particular structure: the root has exactly
    three children, every other non-leaf node has exactly two children, and the leaves are all at the same
    depth k in the tree. This graph has the property that every vertex has exactly 1 or 3 neighbors. A
    sample board with k = 3 is shown in Figure 1. (Note that a Totogram is almost a balanced binary tree,
    except that the root has three subtrees instead of two.) To play the Totogram, the player arranges a
    set of N tiles numbered from 1 to N , where N is the number of vertices in the graph (which, in turn,
    is a function of k), on the vertices of the board. Their score is equal to the maximum absolute value of
    the difference between any pair of adjacent vertices, and the goal is to find an arrangement that makes
    the score as low as possible. For example, the Totogram in Figure 1 shows an arrangement with score
    4 (since tiles 7 and 3 are adjacent to one another).
    Your goal is to write a program that finds the best (lowest-cost) solution that it can for a given k. The
    program should run on the command line like:
    python totogram.py k
    The final two lines of output should be (1) the space-delimited tile arrangement, in breadth-first search
    order, and (2) the score for this arrangement. For example, for Figure 1, the output would be:
    4
    5 4 7 8 1 2 3 6 9 10
    In addition to describing in detail how your approach works, the comments section at the top of your
    code should give a brief analysis of your results, including (1) the best solution your code was able to
    find for k = 3, 4, 5, 6, and 7, including both the score and the actual tile arrangement, and (2) the
    amount of time it took to find each solution.

================================================================================================================================

~~~Algorithm~~~

    In this problem we are using 'Local Search Algorithm' for finding solution. Local Search algorithm does not
    keep track of old states of the system but finds the next best state and takes that. In this problem, our
    Solution Matrix which represent the solution tree, changes its state but does not depend on previous states.
    It finds the next best state to move in with having minimum of cost.

    We have created initial state using "totogram" function.

    Initial state then modified using "arrange" and "arrange2" function

    We take care that we will not lead wo worse state than before and after the end we put the solution.

========================================================================================================================

~~~Solution~~~

    Approach:
    The following problem has a specific arrangement of numbers for a particular depth 'n'. In this arrangement
    the root node has 3 childs and the further every node has 2 childs. All other nodes except the root node is
    like a balanced binary tree. Inorder to calculate the total nummber of elements which will be present in a
    particular totogram tree at depth 'n' we have used a formula as:

    Total number of nodes = 3*(2^(n-1)-1)+1

    It can be derived easily from the formula of total nodes of binary tree which is (2^n-1).Which has one root
    node.Here we have 3 binary trees and one root node.

    Initially we created 2 Matrices.
    First Matrix is the main matrix which initially stores 3 columns: value of the node which is taken '-1' as
    default, index of parent node, and the distance between the current node and its parent. This will be the matrix
    where we are going to store our final tree.

    Second Matrix is Childmatrix which stores the current index and the indices of it child.

    for the very small depth which is n=2 we can easily find the combination with minimum distance but as the value of 'n' increases the
    tree becomes difficult to evaluate.
    For trees with value of 'n'  we have used following algorithm.
    We find the middle element of the total numbers and initialise it as the root note.
    Next is we also assign the 3rd node i.e the first node of second binary tree. We assign this value with the very next node of the root node as the distance beetween root node and very next node is minimum.
    Now we have to create 4 binary trees such that one tree is left tree of root node second tree is the left binary tree of the middle node assigned after root node, third tree is the right binary tree of the middle node, and fourth tree is the right binary tree of the root node.

    For the very left binary tree we assign the numbers in a particular fashion. Initially we find a particular distance according to the depth using an approximate function to initialise matrix.
    Using this calculated difference we assign proper value to the nodes of each tree.

____________________________________________________________________________________________________________________________________


~~~For the particular values of 'n' our algorithm works in following way:~~~

    For n=3:
    Total number of nodes= 3*(2^(n-1)-1)+1 = 10
    we assign root node as 5
    and the middle i.e 2nd node as 6.
    now we calculate the difference between two nodes for extreme left and right depending upon its depth which is 3.
    We can find it in an iterative manner such that starting from the root node we need to find such difference to its left
    and right in which the left tree leads to negative number in exactly its depth iteration and the right tree leads to a
    number greater than the upper limit exactly in its depth iteration. As soon as we get negative number or number greater
    than upper bound we increament or decreament to fall in the limits.

    we get this value as 3.

    Thus initially we form the left binary tree as:

                                5

              2                 6

        1           3


    In the next step we form the right binary tree as:

                                5

              2                 6                   8

        1           3                       9               10


    and now similarly we form center left binaryt tree and right binary tree:

                                         5

              2                          6                          8

        1           3           4                 7          9               10

    Thus the maximum distance between two nodes in this tree is 3.


    ------------------------------------------------------------
    -----------------------Time Required------------------------
    ------------------------------------------------------------
    NOTE: You can uncomment last commented sentence to see output of time required by yourself

    Time required 0.0 Sec

                        
----------------------------------------------------------------------------------------------------------------------------------------------------


    Similarly,
    For n=4:
    Total number of nodes= 3*(2^(n-1)-1)+1 = 22

    The tree we get:
    maximum distance between two nodes we get: 4
    The tree in breadth first fashion we get as;

    11 7 12 15 3 4 8 16 19 18 1 2 5 6 9 10 14 13 22 21 20 17

    ------------------------------------------------------------
    -----------------------Time Required------------------------
    ------------------------------------------------------------
    NOTE: You can uncomment last commented sentence to see output of time required by yourself

    Time required 0.0 Sec


----------------------------------------------------------------------------------------------------------------------------------------------

    For n=5:
    Total number of nodes= 3*(2^(n-1)-1)+1 = 46

    The tree we get:
    maximum distance between two nodes we get: 6

    The tree in breadth first fashion we get nodes as;

    23 17 24 29 11 12 18 30 35 34 5 6 7 8 15 19 32 28 41 40 39 38 1 2 3 4 9 10 13 14 16
    20 21 22 31 27 26 25 46 45 44 43 42 37 36 33

    ------------------------------------------------------------
    -----------------------Time Required------------------------
    ------------------------------------------------------------
    NOTE: You can uncomment last commented sentence to see output of time required by yourself

    Time required 0.00100016593933 Sec


----------------------------------------------------------------------------------------------------------------------------------------------

    For n=6:
    Total number of nodes= 3*(2^(n-1)-1)+1 = 94

    The tree we get:
    maximum distance between two nodes we get: 10

    The tree in breadth first fashion we get nodes as;

    47 37 48 57 27 28 38 58 67 66 17 18 19 20 31 34 64 61 77 76 75 74 7 8 9 10 11 12 24
    23 32 35 36 39 63 60 59 56 87 86 85 84 69 82 81 70 1 2 3 4 5 6 15 16 21 14 22 13 25
    26 29 30 33 40 41 42 43 44 45 46 62 55 54 53 52 51 50 49 94 93 92 91 90 89 88 79 78
    73 72 80 71 83 68 65

    ------------------------------------------------------------
    -----------------------Time Required------------------------
    ------------------------------------------------------------
    NOTE: You can uncomment last commented sentence to see output of time required by yourself

    Time required 0.00600004196167 Sec

----------------------------------------------------------------------------------------------------------------------------------------------

    For n=7:
    Total number of nodes= 3*(2^(n-1)-1)+1 = 190

    The tree we get:
    maximum distance between two nodes we get: 17

    The tree in breadth first fashion we get nodes as;

    95 79 96 111 63 64 80 112 127 126 47 48 49 50 65 67 128 124 143 142 141 140 31 32
    33 34 35 36 37 38 61 68 69 70 130 123 122 121 159 158 157 156 155 154 153 139 15
    16 17 18 19 20 21 22 23 24 25 46 45 43 42 44 62 71 72 73 74 75 76 77 129 120 119
    118 117 116 115 114 175 174 173 172 171 170 169 168 167 166 165 164 145 144 146
    147 1 2 3 4 5 6 7 8 9 10 11 12 13 14 27 28 39 29 40 30 41 26 51 52 53 54 55 56 57
    58 59 60 66 78 81 82 83 84 85 86 87 88 89 90 91 92 93 94 125 113 110 109 108 107
    106 105 104 103 102 101 100 99 98 97 190 189 188 187 186 185 184 183 182 181 180
    179 178 177 176 162 151 161 150 160 149 163 148 152 138 137 136 135 134 133 132 131


    ------------------------------------------------------------
    -----------------------Time Required------------------------
    ------------------------------------------------------------
    NOTE: You can uncomment last commented sentence to see output of time required by yourself

    Time required 0.0439999103546 Sec

--------------------------------------------------------------------------------------------------------------------------------------------

"""

import sys
from time import time


# To initialize matrix1
def initmatrix(n):
    matrix1=[]
    matrix1.append([-1,-1,-1,1])
    for j in range(0,3):
        matrix1.append([-1,0,-1,2])
    count=1
    for i in range(4,(3*(pow(2,n-1)-1)+1)):
        matrix1.append([-1,count,-1,0])
        if(i%2!=0):
            count+=1

    for i in range(1, len(childmat)):
        matrix1[childmat[i][1]][3] = matrix1[i][3] + 1
        matrix1[childmat[i][2]][3] = matrix1[i][3] + 1

    return matrix1


# to initialize childmat which contains mapping to the childs
def initchilds(n):
    n=n
    matrix2=[]
    frst=4
    second=5
    matrix2.append([0,1,2,3])
    count=(3*(pow(2,n-2)-1)+1)
    for i in range(1,count):
        matrix2.append([i,frst,second])
        frst+=2
        second+=2
    return matrix2


# generate initial state on which local search will be applied
def totogram(n):

    matrix1[0][0]=(number)/2
    matrix1[2][0]=((number)/2)+1
    matrix1[2][2]=abs(matrix1[2][0]-matrix1[0][0])

    diff = getk(n)
    list1 = getl1('l',n)
    buildlbtree(list1,diff)

    del list1[:]
    list1 = getl1('r',n)
    buildrbtree(list1,diff)

    del list1[:]
    list1 = getl1('ml',n-1)
    buildlbtree(list1,diff)

    del list1[:]
    list1 = getl1('mr',n-1)
    buildrbtree(list1,diff)

    for i in range(1,len(matrix1)):
        parent = matrix1[i][1]
        matrix1[i][2]=abs(matrix1[parent][0]-matrix1[i][0])


def buildlbtree(list1,diff):
    for i in range(0, len(list1)):
        parent = matrix1[list1[i][0]][1]
        if(((matrix1[parent][0]) - diff)>0):
            value = matrix1[parent][0] - diff
            x=0
            while x<len(visited):
                if(value == visited[x]):
                    value+=1
                    x=0
                else:
                    x+=1

            matrix1[list1[i][0]][0] = value
            visited.append(value)

        elif((matrix1[parent][0] - diff)<0):
            value = (matrix1[parent][0] - diff)
            while(value<=0):
                value += 1
                flag = 0
                for j in visited:
                    if(j == value):
                        flag = 1
                        break
            if flag == 0:
                matrix1[list1[i][0]][0] = value
                visited.append(value)

    for i in range(0,len(list1)):
        for j in range(1,list1[i][1]):
            flag = 0
            tmp = j
            k = 0
            while(k<len(visited)):
                if(visited[k] == matrix1[list1[i][0]][0]+tmp):
                    tmp +=1
                    k = 0
                else:
                    k+=1

            matrix1[list1[i][0]+j][0] = matrix1[list1[i][0]][0]+tmp
            visited.append(matrix1[list1[i][0]+j][0])


def buildrbtree(list1,diff):
    for i in range(0, len(list1)):
        parent = matrix1[list1[i][0]][1]
        if(((matrix1[parent][0]) + diff)<number):
            value = matrix1[parent][0] + diff
            x = 0
            while(x<len(visited)):
                if(value == visited[x]):
                    x=0
                    value = value - 1
                else:
                    x+=1

            matrix1[list1[i][0]][0] = value
            visited.append(value)

        elif((matrix1[parent][0] + diff)>number):
            value = (matrix1[parent][0] + diff)
            while(value>number):
                value -= 1
                flag = 0
                for j in visited:
                    if(j == value):
                        flag = 1
                        break
            if flag == 0:
                matrix1[list1[i][0]][0] = value
                visited.append(value)

    for i in range(0,len(list1)):
        for j in range(1,list1[i][1]):
            flag = 0
            tmp = j
            k = 0
            while(k<len(visited)):
                if(visited[k] == matrix1[list1[i][0]][0]-tmp):
                    tmp +=1
                    k = 0
                else:
                    k = k +1
            matrix1[list1[i][0]+j][0] = matrix1[list1[i][0]][0]-tmp
            visited.append(matrix1[list1[i][0]+j][0])


def getl1(c, depth):
    list1 = []
    count = 1
    if(c=='l'):
        child = childmat[0][1]
    elif(c=='r'):
        child = childmat[0][3]
    elif(c=='ml'):
        child = childmat[2][1]
    elif(c=='mr'):
        child = childmat[2][2]

    for i in range(1,depth):
        list1.append([child,count])
        count += count
        if(child<len(childmat)):
            child = childmat[child][1]
    return list1

def getk(n):
    temp = 1
    flag = 0

    while(flag == 0):
        chkval = matrix1[0][0]
        for i in range(0,n-1):
            chkval = chkval - temp
        if(chkval>=0):
            temp += 1
        else:
            flag = 1
    return temp


def findmx():
    m=-1
    index=0
    for i in range(0,len(matrix1)):
        if(m<matrix1[i][2]):
            m=matrix1[i][2]
            index=i
    return(index)


# find leftmost leaf node in tree
def left_most(n):
    return (3*(pow(2,n-1)-1)+1) - (3*(pow(2, n-2)))


# find index of the given number
def index_of_number(num):
    for i in range(0,len(matrix1)):
        if matrix1[i][0] == num:
            return i


# it will check if given number can be replaced by number on given position
# it will return 1 if it is replaced
# it will return -1 if it not replaced
def replaced(number_to_be_replaced,position,dist):
    dis = []
    number_to_replace = matrix1[position][0]
    for i in range(0, len(matrix1)):
        if (matrix1[i][0] == number_to_be_replaced):
            parent = matrix1[matrix1[i][1]][0]
            par = abs(parent - number_to_replace)
            dis.append(par)
            dis.append(abs(number_to_replace-matrix1[childmat[i][1]][0]))
            dis.append(abs(number_to_replace-matrix1[childmat[i][2]][0]))

            if max(dis) <= dist:
                matrix1[i][0] = number_to_replace
                matrix1[i][2] = dis[0]
                matrix1[childmat[i][1]][2] = dis[1]
                matrix1[childmat[i][2]][2] = dis[2]
                matrix1[position][0] = number_to_be_replaced
                matrix1[position][2] = abs(matrix1[position][0]-matrix1[matrix1[position][1]][0])
                return 1
            else:
                return -1
    return -1


# for the case where leaf node element needs to replaced by smaller value
def d_arrange(matrix1, position, diff):
    p_val = matrix1[matrix1[position][1]][0]
    p_index = matrix1[position][1]

    lower_bound = p_val - diff
    i = matrix1[position][0]
    while i >= lower_bound:
        if abs(p_val - i) <= diff:
            if matrix1[index_of_number(i)][3] == n-1 and index_of_number(i)!=matrix1[position][1]:
                returned = replaced(i,position,diff)
                if returned == 1:
                    return 0
        i -= 1


# for the case where leaf node element needs to replaced by greater value
def i_arrange(matrix1, position, diff):
    p_val = matrix1[matrix1[position][1]][0]
    p_index = matrix1[position][1]

    upper_bound = p_val + diff
    i = matrix1[position][1]
    while i <= upper_bound:
        if abs(p_val - i) <= diff:
            if matrix1[index_of_number(i)][3] == n-1 and index_of_number(i)!=matrix1[position][1]:
                returned = replaced(i,position,diff)
                if returned == 1:
                    return 0
        i += 1


# it will check which leaf node elements need to be replaced
# and if needed to be replaced then whether by greater number or smaller number
def arrange(matrix1, diff):
    starting_point = left_most(n)
    end_point = 3*(pow(2,n-1)-1)+1
    for i in range(starting_point, end_point):
        if matrix1[i][2] > diff:
            if matrix1[i][0] > matrix1[matrix1[i][1]][0]:
                d_arrange(matrix1,i, diff)
            else:
                i_arrange(matrix1,i,diff)


# for the case where leaf node element needs to replaced by smaller value
def d_arrange2(matrix1, position, diff):
    p_val = matrix1[matrix1[position][1]][0]
    p_index = matrix1[position][1]

    lower_bound = p_val - diff
    i = matrix1[position][0]
    while i >= lower_bound:
        if abs(p_val - i) <= diff:
            if matrix1[index_of_number(i)][3] == n-2 and index_of_number(i)!=matrix1[position][1]:
                returned = replaced(i,position,diff)
                if returned == 1:
                    return 0
        i -= 1


# for the case where leaf node element needs to replaced by greater value
def i_arrange2(matrix1, position, diff):
    p_val = matrix1[matrix1[position][1]][0]
    p_index = matrix1[position][1]

    upper_bound = p_val + diff
    i = matrix1[position][1]
    while i <= upper_bound:
        if abs(p_val - i) <= diff:
            if matrix1[index_of_number(i)][3] == n-2 and index_of_number(i)!=matrix1[position][1]:
                returned = replaced(i,position,diff)
                if returned == 1:
                    return 0
        i += 1


# it will check which leaf node elements need to be replaced
# and if needed to be replaced then whether by greater number or smaller number
def arrange2(matrix1, diff):
    starting_point = left_most(n)
    end_point = 3*(pow(2,n-1)-1)+1
    for i in range(starting_point, end_point):
        if matrix1[i][2] > diff:
            if matrix1[i][0] > matrix1[matrix1[i][1]][0]:
                d_arrange2(matrix1,i, diff)
            else:
                i_arrange2(matrix1,i,diff)


# ................... Main Starts here ..................................
if __name__ == '__main__':
    start_time = time()

    n = int(sys.argv[1])
    number = (3*(pow(2,n-1)-1))+1
    childmat=initchilds(n)
    matrix1=initmatrix(n)
    visited = []

    # creating initial state for local search
    totogram(n)
    
    # calculating difference value on which to operate
    difference = getk(n)
    # Arranging to get better state
    arrange(matrix1,difference)
    # Arranging to get better state
    arrange2(matrix1,difference)

    # find the maximum value of distances between node elements
    mx = findmx()

    # printing the solution
    print "The Mximum distance between two nodes for this tree is ...", matrix1[mx][2]
    for i in range(0,len(matrix1)):
        print matrix1[i][0],
    # print "\nTime required", time()-start_time
