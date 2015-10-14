# -*- coding: utf-8 -*-
import sys
from game import game

if __name__ == "__main__":
    G=game()
    G.importfile('mat1.txt')

    print("My algorithm")
        
    strongcomp = G.levels()
        
    print(strongcomp)
    
    reduced = G.reducedgraph(strongcomp)
    
    print(reduced.edges())
    
    print(reduced.successors(2))
    print(reduced.out_degree(2))

    print(reduced.generatematrix())
    
    longpath = G.longestpath(3,2)
    
    print(longpath)