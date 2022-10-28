import queue
import numpy as np


'''
    Adjacency List Graph in python using a Dictionary.

    Each node will be represented as a list of array,
    each array contains a adjacent node and the weight of the edge.

    List = {0:[(1, 3), 1:(2, 4)},

    Queue:
        put(): insert item
        get(): get item and remove
        empty(): check if queue is empty
'''


class AdjacencyList:

    def __init__(self, num_of_nodes, directed=True):
        self.m_num_of_nodes = num_of_nodes

        self.m_nodes = range(self.m_num_of_nodes)

        # Define the type of a graph
        self.isDirected = directed

        # Create a dictionary to store the adjacency list, []
        self.list = {node: [] for node in self.m_nodes}

        # BFS
        self.path_found = False
        self.parents = dict()
        self.visited = set()
        self.queue = queue.Queue()

    def add_edge(self, node1, node2, weight=1):
        for v in self.list[node1]:
            if (v[0] == node2):
                v[1] = weight
                return

        self.list[node1].append([node2, weight])

        if self.isDirected == False:
            self.list[node2].append([node1, weight])

    def print_adj_list(self):
        print('Adjacency List:')
        for key in self.list.keys():
            print("node", key, ": ", self.list[key])

    def BFS(self, START, TARGET):

        # START NODE DONT HAVE PARENT (mean it's root node)

        # parent is like [{node: node}]
        self.parents[START] = None

        # queue is like []
        self.queue.put(START)
        
        

        self.visited.add(START)

        while not self.queue.empty():

            current_node = self.queue.get()

            # Sẽ duyệt đến khi lần đầu tiên gặp TARGET thì dừng
            if (current_node == TARGET):
                self.path_found = True
                break

            for (node, weight) in self.list[current_node]:

                print('current_node: ', current_node, '| node: ', node, '| visited: ', self.visited, '| queue: ',
                      self.queue.queue, "| parent", self.parents)

                # check if the node has been visited
                if node not in self.visited:

                    # Đẩy CÁC node KỀ current_node vào queue

                    self.queue.put(node)

                    # add current_not to 'key' node
                    self.parents[node] = current_node

                    self.visited.add(node)

        # Now reconstruct the path from start_node to target_node
        path = []

        print('----------Reconstructing path----------')

        '''
            6 -> 4 (TARGET)
            parent {6->None, 2->6, 1->6, 0->2, 3->2, 5->2, 4->0}
            
            Duyệt ngược từ TARGET -> START
            => parent[TARGET] -> parent[parent[TARGET]] -> parent[parent[parent[TARGET]]] -> ...
        '''

        if self.path_found:

            path.append(TARGET)

            while self.parents[TARGET] is not None:
                print("target_node : ", TARGET, "self.parents[target_node]: ", self.parents[TARGET])

                TARGET = self.parents[TARGET]

                path.append(TARGET)

            path.reverse()

        return path


graph = AdjacencyList(9, directed=False)
graph.add_edge(0, 1)
graph.add_edge(0, 4)
graph.add_edge(4, 5)
graph.add_edge(0, 2)
graph.add_edge(3, 4)
graph.add_edge(0, 3)
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(6, 2)
graph.add_edge(2, 5)
graph.add_edge(3, 5)
graph.add_edge(6, 1)
graph.add_edge(7, 8)


graph.print_adj_list()

path = []
start = 6
end = 4
path = graph.BFS(start, end)

print("Path from", start, "to", end, "is", path)
print("visited nodes:", graph.visited)
print("parents:", graph.parents)


# graph.BFS(0, 4)
