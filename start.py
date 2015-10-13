# -*- coding: utf-8 -*-
import sys
sys.path.append('networkx-1.10-py2.7.egg')
sys.path.append('decorator-4.0.4-py2.py3-none-any.whl')
import networkx
from game import game

if __name__ == "__main__":
    G=game()
    G.importfile('mat1.txt')

    print("Integrated algorithm :")

    test = networkx.strongly_connected_components(G)
    for c in test:
        print(c)
        
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