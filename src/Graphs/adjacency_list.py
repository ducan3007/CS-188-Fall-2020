'''
    Adjacency List Graph in python
    
    NxN Matrix representation of a graph is not efficient in terms of space.
'''

# Weighted Graph
Edges = [(1, 2, 3), (1, 3, 4), (2, 3, 5), (2, 4, 6), (3, 4, 7), (3, 5, 8), (4, 5, 9)]


class AdjacencyList:
    def __init__(self):
