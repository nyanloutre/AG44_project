# -*- coding: utf-8 -*-
import sys
from game import game

if __name__ == "__main__":
    G=game()
    G.importfile('mat1.txt')

    print("Strongly connected components :")
    
    strongcomp = G.levels()
        
    print(strongcomp)
    
    print("Reduced matrix :")
    
    reduced = G.reducedgraph()

    for line in reduced.generatematrix():
        print(line)
    
    print("Longest path :")
    
    '''startnode = int(input("Enter the starting node : "))
    endnode = int(input("Enter the ending node : "))'''

    startnode = 1
    endnode = 8
    
    i=1
    
    for comp in strongcomp:
    
        if comp.count(startnode) > 0:
            startnode = i
        if comp.count(endnode) > 0:
            endnode = i
        i+=1
    
    longpath = reduced.longestpath(startnode,endnode)
    
    print(longpath)
