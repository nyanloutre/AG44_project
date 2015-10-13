# -*- coding: utf-8 -*-
import io, re
from networkx import MultiDiGraph
from oauthlib.uri_validate import path

class game(MultiDiGraph):
    
    #The class game herit from the class DiGraph
    def __init__(self):
        super().__init__()
    
    #This method take the name of the file in input, then parse it and convert it into a directed graph
    def importfile(self, graphfile):
        with io.open(graphfile, 'r') as graphtxt: #Open the file
            if graphtxt.readable(): #Check if we can read it
                size = int(graphtxt.readline()[0]) #Get the first line which is the size of the array
                self.add_nodes_from(range(1,size+1)) #Create as much node as the size of the array
                #print(self.nodes())
                rx = re.compile('[^0-9]') #Regular expression to keep only the numbers
                for i in range(1,size+1): #Then parse the file line by line to create the edges
                    curline = graphtxt.readline()
                    curline = rx.sub('', curline).strip() #Apply the regular expression on the current line
                    #print(curline)
                    for j in range(1,size+1):
                        connect = int(curline[j-1])
                        if connect:
                            #print('pour j =', j, 'et i = ', i, ' connect vaut ' ,connect)
                            self.add_edge(i, j)
        return None
                            
    #Algorithm who create the list of levels we will use the Kosaraju’s algorithm
    #It works very simply : 
    #   1- We do a dfs of the graph and we put all the vertexes at the end on an empty stack
    #   2- We reverse the direction of the edges (so this new graph have the same strongly connected components)
    #   3- We do an other dfs on this new graph beginning with the node on the top of the stack
    #   4- When we reach an end, all the traversed nodes are strongly connected. We pop them out of the stack
    def levels(self):
        stack = self.dfs(1)
        #print(stack)
        #print(self.edges())
        self.reverse(False)
        #print(self.edges())
        components = self.strongdetection(stack)
        self.reverse(False)
        return components

    #Recursive depth-first traversal and store the nodes in the reverse order on a stack
    def dfs(self, startnode, stack = list(), revstack = list()):
        successors = self.successors(startnode)
        stack.append(startnode)
        if len(successors) != 0:
            for succ in successors:
                if stack.count(succ) == 0:
                    self.dfs(succ, stack)
        revstack.append(startnode)
        return revstack
    
    #The two following methods search all the strongly connected components
    def strongdetection(self, dfs_stack, stack=list()):
        while len(dfs_stack) > 0:
            stack.append(self.strongcomponent(dfs_stack.pop(), dfs_stack, []))
        
        return stack

    def strongcomponent(self, startnode, dfs_stack, currstrong):
        currstrong.append(startnode)
        for succ in self.successors(startnode):
            if dfs_stack.count(succ) > 0:
                self.strongcomponent(dfs_stack.pop(dfs_stack.index(succ)), dfs_stack, currstrong)
        
        return currstrong
    
    def reducedgraph(self, strongcomponents):
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
        size = len(self.nodes())
        matrix = [[0 for j in range(size)] for i in range(size)]
        
        for edge in self.out_edges_iter():
            i = edge[0]
            j = edge[1]
            matrix[i-1][j-1] += 1
                
        return matrix
    
    def longestpath(self, startnode, endnode, path = []):
        if path.count(startnode) == 0:
            path.append(startnode)
            if startnode != endnode:
                maxlen = 0
                maxpath = path
                for succ in self.successors(startnode):
                    newpath = self.longestpath(succ, endnode, path[:])
                    if newpath != False:
                        newlen = len(newpath)
                        if newlen > maxlen:
                            maxlen = newlen
                            maxpath = newpath
                            
                path = maxpath
                
        if path[-1] == endnode:
            return path
        else:
            return False
    
    '''def longestpath(self, startnode, endnode, edges = []):
        if len(edges) == 0:
            edges = self.edges()'''
        