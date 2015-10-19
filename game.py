# -*- coding: utf-8 -*-
import io, re
from networkx import MultiDiGraph

class game(MultiDiGraph):

    def __init__(self):
        '''The class game inherit from the class DiGraph and initialize a new game'''

        super().__init__()


    def importfile(self, graphfile):
        '''This method take the name of the file in input, then parse it and convert it into a directed graph'''
        
        with io.open(graphfile, 'r') as graphtxt: #Open the file
            if graphtxt.readable(): #Check if we can read it
                size = int(graphtxt.readline()[0]) #Get the first line which is the size of the array
                self.add_nodes_from(range(1,size+1)) #Create as much node as the size of the array
                rx = re.compile('[^0-9]') #Regular expression to keep only the numbers
                for i in range(1,size+1): #Then parse the file line by line to create the edges
                    curline = graphtxt.readline()
                    curline = rx.sub('', curline).strip() #Apply the regular expression on the current line
                    for j in range(1,size+1):
                        connect = int(curline[j-1])
                        if connect:
                            self.add_edge(i, j)


    def levels(self):
        '''Algorithm who create the list of levels we will use the Kosaraju’s algorithm
        This is is how it works : 
            1- We do a dfs of the graph and we put all the vertexes at the end on an empty stack
            2- We reverse the direction of the edges (so this new graph have the same strongly connected components)
            3- We do an other dfs on this new graph beginning with the node on the top of the stack
            4- When we reach an end, all the traversed nodes are strongly connected. We pop them out of the stack'''
        
        stack = self.dfs(1) #Do a first dfs
        self.reverse(False) #Reverse the graph
        components = self.strongdetection(stack) #Launch the detection of strongly connected components
        self.reverse(False) #Reverse the graph again to have the same
        return components


    def dfs(self, startnode, stack = None, revstack = None):
        '''Recursive depth-first traversal, it store the nodes on a stack'''
        
        if stack == None:
            stack = list() #Initialise an empty stack if none is provided
        if revstack == None:
            revstack = list()
        successors = self.successors(startnode) #Get the successors
        stack.append(startnode) #Add this node to the stack
        if len(successors) != 0: #Go as deepest as possible for each node
            for succ in successors:
                if stack.count(succ) == 0:
                    revstack = self.dfs(succ, stack, revstack)
        revstack.append(startnode) #If we reach this line that mean we are blocked at a end
        return revstack


    def strongdetection(self, dfs_stack, stack=None):
        '''List all the strongly components while they are nodes'''
        
        if stack == None:
            stack = list()
        while len(dfs_stack) > 0: #While the stack is not empty there are strongly connected components
            stack.append(self.strongcomponent(dfs_stack.pop(), dfs_stack))
        
        return stack


    def strongcomponent(self, startnode, dfs_stack, currstrong=None):
        '''Find a strongly connected component containing the given vertex'''
        
        if currstrong == None:
            currstrong = list()

        currstrong.append(startnode)
        for succ in self.successors(startnode): #All the successors that are still in the stack are strongly connected
            if dfs_stack.count(succ) > 0:
                self.strongcomponent(dfs_stack.pop(dfs_stack.index(succ)), dfs_stack, currstrong)
        
        return currstrong


    def reducedgraph(self, strongcomponents = None):
        '''Generate the reduced graph from the strong components
           This create a new graph were each node represent a strongly connected component'''
        
        if strongcomponents == None:
            strongcomponents = self.levels()
        newgraph = game()
        i = 1
        for currcomponent in strongcomponents:
            newgraph.add_node(i)
            for currnode in currcomponent:
                j = 1
                for nextcomponent in strongcomponents:
                    for nextnode in nextcomponent:
                        if nextnode in self.successors(currnode) and i!= j:
                            newgraph.add_edge(i, j)
                    j+=1
            i+=1
            
        return newgraph


    def generatematrix(self):
        '''Generate a matrix for any given graph'''
        
        size = len(self.nodes())
        matrix = [[0 for j in range(size)] for i in range(size)]
        
        for edge in self.out_edges_iter():
            i = edge[0]
            j = edge[1]
            matrix[i-1][j-1] += 1
                
        return matrix


    def longestpath(self, startnode, endnode, path = None):
        '''Find the longest path by testing all the possibilities'''
        
        if path == None:
            path = list()
        if path.count(startnode) == 0: #Check if the current node has already been traversed
            path.append(startnode) #We append the current node to the stack
            if startnode != endnode: #Check if we are at the end
                maxlen = 0 #if not, find the longest path that begin with the current node
                maxpath = path
                for succ in self.successors(startnode): #Recursive call to get the longest path that begin with each successors
                    newpath = self.longestpath(succ, endnode, path[:])
                    if newpath != False: #If there is a path beggining with this successors
                        newlen = len(newpath) #We get the size
                        if newlen > maxlen: #Check if it is longer than any previous attempt
                            maxlen = newlen
                            maxpath = newpath
                            
                path = maxpath #Save the longest path
                
        if path[-1] == endnode: #Check if the last node is effectively the right node (so if the path is valid)
            return path
        else:
            return False #If not return false
