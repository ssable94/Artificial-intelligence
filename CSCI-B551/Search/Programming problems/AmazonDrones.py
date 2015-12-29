#!/usr/bin/python
"""
    ~~~How formulated the problem~~~
    
        ~~~Problem Formulation~~~
            We have give the conditions and some data on delivery done by amazon parrots, using that data we have to find who ordered which packet and what he received and his location.
            
        ~~~Initial State~~~
            Initial represents all the data given in the problem, in the list of list (abstraction of two dimensional array)
            
        ~~~Action~~~
            Replace the variable by valid value.
            
        ~~~Transition Model~~~
            When variable is replaced by value. new state will be generated which maybe a valid state or non-valid state, we need to check for its validity
        
        ~~~Validity~~~
            State is valid if it do not violet following two conditions:
                1) for any user what he ordered should not be equal to what he received.
                2) There should be only one to one mapping between name of person, what he ordered, what he received, and his location.
                    Ex:
                    
                                state containing following two rows in not a valid state.
                          Name    ordered        got         location
                    1)    None    Candelabrum    Banister    None
                    2)    None    Candelabrum    Doorknob     None
                    
                    As candelabrum is mapped to banister and doorknob both
                            
        Data provided in the problem is used to from matrix representation of the state.
        Each condition in the problem is represented as a one or more rows in the matrix.
        Matrix contains four rows first one is name of person, second is what the person ordered, third is what he received, and fourth one is where he lives.
        Example:
            
            The customer who ordered the Candelabrum received the Banister.
            
            Above statement represented as
                  Name    ordered        got         location
            1)    None    Candelabrum    Banister    None
        
        Thus initial state already contains all the restrains and conditions given in the problem.
        (Numerical values are used as variables)
        
        Used variable where exact values were not given
        Example:
            George's package went to kirkwood street
                        Name    Ordered     got    location
            1)        George        1        None    None
            2)        None        None        1    Kirkwood Street
            
        ~~~State Space~~~
        
            S contain s:
                where s contain zero or more rows with four touple
                    each touple contains two elements
                        first element is integer and second element is either string or number
                        if first element is 0:
                            Sencond element should be "None"
                        if first element is 1:
                            Second element should be any valid value for name or product or location Ex: "Doorknob"
                        if first element is 2:
                            second element should be integer value which represents variable
                            
            State Space contain infinite number of states
            but if we do some operations like:
                eliminating redundant rows
                    Ex:
                                Name    ordered        got         location
                        1)    George    1            None        None
                        2)    George    1            None        None
                        
                        here we can keep only one row from row 1 and row 2
                    
                rows which do no make sense
                    Ex:
                    
                            Name    ordered        got         location
                        1)    None    None            None        None
                        2)    2        1                5            4
                        
                        We can eliminate both row 1 and row 2 as they do not make any sense
                        
            after doing elimination operations state space will contain limited number of states
            
        ~~~Successor Function~~~
            
            Successor function will take state, variable, and value for the variable to ba placed in the state
            
            It will replace the value given by previous successor function in the variable in given state
            this will create new rules using this rules it will again prune the solution space,
            then it will merge the rows in the the state,
            then it will remove duplicates.
            
            Now again it will search for the variable to be replaced by value, it will chose the variable which has least number of minimum possible solution. Because it will be less costly if we need to backtrack the solution, because of invalid state
            it will pass the state, variable chosen, and variable to be replaced.
            
        ~~~edge weight~~~
            Edge weight is not considered
            
        ~~~Goal State~~~
            Goas state is a valid state with 5 rows and it do not contain any variables and None values.
            Ex:
            
                |-----------------------------------------------------------------------|
                | Name            | Order           | received        | location        |
                |-----------------|-----------------|-----------------|-----------------|
                | Irene           | Candelabrum     | Banister        | Kirkwood Street |
                | George          | Banister        | Candelabrum     | Lake Avenue     |
                | Frank           | Elephant        | Doorknob        | Orange Drive    |
                | Heather         | Amplifier       | Elephant        | North Avenue    |
                | Jerry           | Doorknob        | Amplifier       | Maxwell Street  |
                |-----------------------------------------------------------------------|
                
                Above is the example of goal state
                
        ~~~Completeness of the algorithm~~~
            If input state is valid then algorithm will generate a solution, else it will give message that its not a valid state.
            Hence, algorithm is complete
            
        ~~~complexity~~~
            Its similar to deapth first search.
            
**************************************************************************************************************************************************
**************************************************************************************************************************************************
  
    ~~~Feature of the algorithm~~~
        It's general program, it will work for all the cases of the same problem.
        Even if you give empty state as a input, it will generate and give a valid output

"""
import copy
from copy import deepcopy


#def uniq(state):
"""
    Deleting Duplicate rows from the state table, as they are useless
"""
def uniq(state):
    nstate=[]
    for c in state:
        if c not in nstate:
            nstate.append(c)
    return nstate


#def prun(state,Solution):
"""
    Pruning possible solutions for the variables, to reduce efforts made in determining the actual value of variable
"""
def prun(state,Solution):


    #comparing the pairs in data structure
    """ 
            if we have 
                1) [0,"None"],[1,"Candelabrum"],[1,"Banister"],[0,"None"]
                2) [0,"None"],[1,"Doorknob"],[1,"X"],[0,"None"]
            Meaning X!=Banister
                thus Banister in excluded from possible solutions of X

            As we can see here we need to consider only pairs Candelabrum:Banister::Doorknob:X
                thus comparing every possible pairs in state with each other to eliminate solutions which are not possible.

    """
    for c in state:
        for i in range (0,4):
            for j in range (0,4):
                if(c[i][0]==1 and c[j][0]==2):
                    for k in range(len(state)):
                        if(state[k][i][0]==1 and state[k][j][0]==1):
                            if(state[k][i][1]!=c[i][1]):
                                try:
                                    Solution[(c[j][1]-1)].remove(state[k][j][1])
                                except:
                                    pass
                            if(state[k][i][1]==c[i][1]):
                                del Solution[(c[j][1]-1)][:]
                                Solution[(c[j][1]-1)].append(state[k][j][1])



    #making use of the fact that product ordered != product recevied
    """ 
            if we have 
                1) [0,"None"],[1,"X"],[1,"Banister"],[0,"None"]
            Meaning X!=Banister
                thus Banister in excluded from possible solutions of X
    """
    for c in state:
        if(c[1][0]==1 and c[2][0]==2):
            try:
                Solution[(c[2][1]-1)].remove(c[1][1])
            except:
                pass
    for c in state:
        if(c[2][0]==1 and c[1][0]==2):
            try:
                Solution[(c[1][1]-1)].remove(c[2][1])
            except:
                pass



#def prun2 (state,Solution):
"""
    case:
          Name             order             got             location

        1)    Henry           doorknob         banister         orange drive
        2)    None             x(variable)     None             None        


        in the above case if x takes value of doorknob then it will be merged with line 1), hence it makes no sense to give it doorknob value, we can try some other value on it
    Thus makeing,
        
        x(variable)  !=    doorknob
"""
def prun2 (state,Solution):
    prun=1
    for c in state:
        prun=1
        for d in c:
            if(d[0]!=1):
                prun=0
        if(prun==1):
            for i in state:
                for j in range(0,4):
                    if(i[j][0]==2):
                        try:
                            Solution[i[j][1]-1].remove(c[j][1])
                        except:
                            pass

#def merge(state):
"""
    case:
          Name             order             got             location

        1)    Henry        doorknob    None        None
        2)    None        doorknob    banister    None        

    clearly we can merge row 1 and row 2 as
        
        Henry        doorknob    banister    None

    Hence merging the two rows with each other
    (after that uniq function will be applied to remove same rows)

     
"""
def merge(state):
    #merging with the common one
    """if we have 
        1) [0,"None"],[1,"Candelabrum"],[1,"Banister"],[0,"None"]
        2) [0,"None"],[1,"Candelabrum"],[1,"X"],[0,"None"]

        Thus it means that X=banister;
        Hence we can merge two rows with each other

    """
    for i in range(len(state)):
        for j in range(len(state)):
            for k in range(0,4):
                if (state[i][k][0]==1 and state[j][k][0]==1):
                    if (state[i][k][1]==state[j][k][1]):
                        for x in range(0,4):
                            if(state[i][x][0]==0):
                                state[i][x]=state[j][x]
                            elif(state[i][x][0]==2):
                                if(state[j][x][0]==1):
                                    state[i][x]=state[j][x]
    state=uniq(state)
    return state


#def checking(state):
"""
    Checking if the state is consistant or not
"""
def checking(state):
    #comparing the pairs in data structure
    """ 
            if we have 
                1) [0,"None"],[1,"Candelabrum"],[1,"Banister"],[0,"None"]
                2) [0,"None"],[1,"Doorknob"],[1,"X"],[0,"None"]
            Meaning X!=Banister
                thus Banister in excluded from possible solutions of X

            As we can see here we need to consider only pairs Candelabrum:Banister::Doorknob:X
                thus comparing every possible pairs in state with each other to eliminate solutions which are not possible.

    """
    valid=1
    for c in state:
        for i in range(0,4):
            for j in range(0,4):
                if(c[i][0]==1 and c[j][0]==1):
                    for k in state:
                        if(k[i][0]==1 and k[j][0]==1):
                            if(k[i][1]!=c[i][1]):
                                if(k[j][1]==c[j][1]):
                                    valid=-1
                            if(k[i][1]==c[i][1]):
                                if(k[j][1]!=c[j][1]):
                                    valid=-1
                                    
    if(valid!=1):
        return valid
    
    for c in state:
        if(c[1][0]==1 and c[2][0]==1):
            if(c[1][1]==c[2][1]):
                valid=-1
                
    return valid


#def newpb(state):
"""
    if we have incomplete information originally then it is not possible to get solution using that information.
    Thus creating another problem in which empty places are given variables, whose value we will again calculate.
"""
def newpb(state):
    variable=1
    Solution=[]
    while(len(state)<5):
        state.append([[0,"None"],[0,"None"],[0,"None"],[0,"None"]])
    for i in range(len(state)):
        for j in range(0,4):
            if state[i][j][0]!=1:
                state[i][j][0]=2
                state[i][j][1]=variable
                variable=variable+1
                if(j==0):
                    Solution.append(["Irene","Frank","George","Jerry","Heather"])
                if(j==1 or j==2):
                    Solution.append(["Banister","Doorknob","Elephant","Amplifier","Candelabrum"])
                if(j==3):
                    Solution.append(["Kirkwood Street","Lake Avenue","Orange Drive","North Avenue","Maxwell Street"])
    return Solution

#def successor(pstate,pSolution,variable,value):
"""
    it will put value give by previous node for a variable into that variable, then calculate new state and get next variable to be evaluated, if no variables left then takes appropriate action.
"""
def successor(pstate,pSolution,variable,value):
    state=copy.deepcopy(pstate)
    Solution=copy.deepcopy(pSolution)
    valid=1
    #if we have value for variable and its value
    if(variable!=None):
        #setting valid variable value to 0 meaning not valid state
        valid=0
        
        #merging the received value with the state of the current function
        for x in state:
                    for y in x:
                        if(y[0]==2 and y[1]==variable):
                            y[0]=1
                            y[1]=value
                
        #fusing solution found with state data structure
        prun(state, Solution)
        state=merge(state)    
    prun(state, Solution)
    state=merge(state)    
    prun2(state, Solution)
    minlenindex=-1

    #searching for the next variable to be replaced by value
    #next variable chosen according to minimum number of possible solutions
    for i in range(len(Solution)):
        if (len(Solution[i])>0):
            if(minlenindex==-1):
                minlenindex=i
            elif(len(Solution[minlenindex])>len(Solution[i])):
                minlenindex=i
    
    #if we do not found next variable in which we can put possible solution
    if(minlenindex==-1):
        global ogstate
        ogstate=copy.deepcopy(state)
        for c in state:
            for d in c:
                if d[0]==2:
                    return -1
        return 1
    
    #if we find variable in which we can put possible solution
    else:
        for c in Solution[minlenindex]:
            Solution[minlenindex].remove(c)
            if(successor(state, Solution, minlenindex+1, c)!=1):
                Solution[minlenindex].append(c)
            else:
                return 1
    return -1


#building requried data structures
ogstate=state=[[[0,"None"],[1,"Candelabrum"],[1,"Banister"],[0,"None"]],
[[0,"None"],[1,"Banister"],[2,1],[0,"None"]],
[[1,"Irene"],[2,1],[0,"None"],[0,"None"]],
[[1,"Frank"],[0,"None"],[1,"Doorknob"],[0,"None"]],
[[1,"George"],[2,2],[0,"None"],[0,"None"]],
[[0,"None"],[2,3],[2,2],[1,"Kirkwood Street"]],
[[0,"None"],[0,"None"],[2,3],[1,"Lake Avenue"]],
[[1,"Heather"],[2,5],[2,4],[0,"None"]],
[[0,"None"],[2,4],[0,"None"],[1,"Orange Drive"]],
[[0,"None"],[0,"None"],[1,"Elephant"],[1,"North Avenue"]],
[[1,"Jerry"],[0,"None"],[2,5],[0,"None"]],
[[2,6],[1,"Elephant"],[2,7],[0,"None"]],
[[0,"None"],[2,7],[1,"Amplifier"],[1,"Maxwell Street"]]]


Solution=[["Banister","Doorknob","Elephant","Amplifier","Candelabrum"],
["Banister","Doorknob","Elephant","Amplifier","Candelabrum"],
["Banister","Doorknob","Elephant","Amplifier","Candelabrum"],
["Banister","Doorknob","Elephant","Amplifier","Candelabrum"],
["Banister","Doorknob","Elephant","Amplifier","Candelabrum"],
["Irene","Frank","George","Jerry","Heather"],
["Banister","Doorknob","Elephant","Amplifier","Candelabrum"]]


if(checking(ogstate)==1):
    successor(ogstate,Solution,None,None)
    del Solution[:]
    Solution=newpb(ogstate)
    if(checking(ogstate)==1):
        successor(ogstate,Solution,None,None)
        for line in ogstate:
            for item in line:
                while(len(item[1])<15):
                    item[1]=item[1]+" "
        header=["Name           ","Order          ","received       ","location       "]
        print "|-----------------------------------------------------------------------|"
        print "|",header[0],"|",header[1],"|",header[2],"|",header[3],"|"
        print "|-----------------|-----------------|-----------------|-----------------|"
        for row in ogstate:
            print "|",row[0][1],"|",row[1][1],"|",row[2][1],"|",row[3][1],"|"
        print "|-----------------------------------------------------------------------|"
    else:
        print "Invalid input"
else:
    print "Invalid input"
