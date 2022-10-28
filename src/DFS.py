from Graphs.adjacency_list import AdjacencyList
from numpy import np

'''
    The DFS algorithm is a recursive algorithm that uses the idea of backtracking.
    DFS is used to traverse a graph or tree data structure.


ATTENTION
    
    Try to avoid using recursion as much as possible because it can be very memory intensive.
    
    Try not to fall into infinity loops by revisiting the same nodes over and over, that usually happen
    with graphs which have cycles.

'''


class BFS:
    def __init__(self, Grahp: AdjacencyList):
        self.Graph = Grahp

        self.path_found = False
        self.par