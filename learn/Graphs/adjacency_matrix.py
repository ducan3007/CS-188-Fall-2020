
import numpy as np


'''
    Adjacency List Graph in python

+ A N.N Matrix representation of a graph is not efficient in terms of space.

+ Edges = [(1, 2, 3), (1, 3, 4), (2, 3, 5), (2, 4, 6), (3, 4, 7), (3, 5, 8), (4, 5, 9)]

=> Matrix = [[0, 3, 4, 0, 0],
            [0, 0, 5, 6, 0],
            [0, 0, 0, 7, 8],
            [0, 0, 0, 0, 9]]

+ Directed: a graph is directed if the edges have a direction
+ Undirected: a graph is undirected if the edges have no direction
+ Weighted: a graph is weighted if the edges have a weight

'''


class AdjacencyMatrix:
    def __init__(self, numer_of_nodes, directed=True):
        self.nodes = numer_of_nodes
        self.directed = directed
        self.ajd_matrix = np.zeros((numer_of_nodes, numer_of_nodes))

    # Add edges
    def add_edge(self, u, v, weight=1):
        self.ajd_matrix[u][v] = weight

        if not self.directed:
            self.ajd_matrix[v][u] = weight

    # Remove edges
    def remove_edge(self, u, v):
        self.ajd_matrix[u][v] = 0

        if not self.directed:
            self.ajd_matrix[v][u] = 0

    # print graph
    def print_graph(self):
        print(self.ajd_matrix)


Graph = AdjacencyMatrix(5)
Graph.add_edge(0, 1, 3)
