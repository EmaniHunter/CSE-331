"""
Name: Emani Hunter
CSE 331 SS20 (Onsay)
"""

import queue, heapq, math, itertools
from collections import OrderedDict
import matplotlib.pyplot as plt, matplotlib.patches as patches, matplotlib.cm as cm
import numpy as np
import time
import random


class Vertex:
    """
    Class representing a Vertex object within a Graph
    """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, idx, x=0, y=0):
        """
        DO NOT MODIFY
        Initializes a Vertex
        :param idx: A unique string identifier used for hashing the vertex
        :param x: The x coordinate of this vertex (used in a_star)
        :param y: The y coordinate of this vertex (used in a_star)
        """
        self.id = idx
        self.adj = OrderedDict()  # dictionary {id : weight} of outgoing edges
        self.visited = False      # Boolean flag used in search algorithms
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        DO NOT MODIFY
        Overloads equality operator for Graph Vertex class
        :param other: vertex to compare
        """
        return (self.id == other.id
                and self.adj == other.adj
                and self.visited == other.visited
                and self.x == other.x
                and self.y == other.y)

    def __repr__(self):
        """
        DO NOT MODIFY
        Represents Vertex as string
        :return: string representing Vertex object
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]

        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    def __str__(self):
        """
        DO NOT MODIFY
        Represents Vertex as string
        :return: string representing Vertex object
        """
        return repr(self)

    def __hash__(self):
        """
        DO NOT MODIFY
        Hashes Vertex into a set; used in unit tests
        :return: hash value of Vertex
        """
        return hash(self.id)

    def degree(self):
        '''
        Returns the number of outgoing edges from this vertex
        :return: [int] number of outgoing edges
        '''
        return len(self.adj)

    def visit(self):
        '''
        Sets the boolean visited flag to true
        '''
        self.visited = True

    def reset(self):
        '''
        Sets the boolean visited flag to false
        '''
        self.visited = False

    def get_edges(self):
        '''
        Returns a list of tuples representing outgoing edges from this vertex
        :return: [list] list of tuples representing edges
        '''
        edge_list = []
        if len(self.adj) == 0:
            return edge_list
        else:
            for edge in self.adj:
                edges = (edge, self.adj.get(edge))
                edge_list.append(edges)
            return edge_list

    def euclidean_distance(self, other):
        '''
        Returns the euclidean distance [based on two dimensional coordinates]
        between this vertex and vertex other
        :return: [int] euclidean distance
        '''
        x1 = self.x
        x2 = other.x
        y1 = self.y
        y2 = other.y
        euc = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))
        return euc


class Graph:
    """
    Class implementing the Graph ADT using an Adjacency Map structure
    """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show=False):
        """
        DO NOT MODIFY
        Instantiates a Graph class instance
        :param: plt_show : if true, render plot when plot() is called; else, ignore calls to plot()
        """
        self.size = 0
        self.vertices = OrderedDict()
        self.plot_show = plt_show
        self.plot_delay = 0.2

    def __eq__(self, other):
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class
        :param other: graph to compare
        """
        return self.vertices == other.vertices and self.size == other.size

    def __repr__(self):
        """
        DO NOT MODIFY
        :return: String representation of graph for debugging
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    def __str__(self):
        """
        DO NOT MODFIY
        :return: String representation of graph for debugging
        """
        return repr(self)

    def plot(self):
        """
        Modify if you'd like - use for debugging!
        :return: Plot a visual representation of the graph using matplotlib
        """
        if self.plot_show:
            # seed random generator to reproduce random placements if no x,y specified
            random.seed(2020)

            # show edges
            max_weight = max([edge[2] for edge in self.get_edges()])
            colormap = cm.get_cmap('cool')
            for edge in self.get_edges():
                origin = self.get_vertex(edge[0])
                destination = self.get_vertex(edge[1])
                weight = edge[2]

                # if no x, y coords are specified, randomly place in (0,1)x(0,1)
                if not origin.x and not origin.y:
                    origin.x, origin.y = random.random(), random.random()
                if not destination.x and not destination.y:
                    destination.x, destination.y = random.random(), random.random()

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y), (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2", color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text((origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         (origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_vertices()])
            y = np.array([vertex.y for vertex in self.get_vertices()])
            labels = np.array([vertex.id for vertex in self.get_vertices()])
            colors = np.array(['yellow' if vertex.visited else 'black' for vertex in self.get_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for i in range(len(x)):
                plt.text(x[i] - 0.03 * max(x), y[i] - 0.03 * max(y), labels[i])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

    def reset_vertices(self):
        '''
        Resets visited flags of all vertices within the graph
        '''
        for v in self.vertices:
            if self.vertices[v].visited:
                self.vertices[v].visited = False

    def get_vertex(self, vertex_id):
        '''
        Returns the Vertex object with id vertex_id if it exists in the graph
        :param vertex_id: vertex object that exists in graph
        :return: [vertex] vertex object
        '''
        if vertex_id in self.vertices:
            return self.vertices.get(vertex_id)
        else:
            return None

    def get_vertices(self):
        '''
        Returns a list of all Vertex objects held in the graph
        :return: [list] list of all vertices in graph
        '''
        vertex_lst = []
        if len(self.vertices) == 0:
            return vertex_lst
        else:
            for v in self.vertices:
                vertex_lst.append(self.vertices[v])
            return vertex_lst

    def get_edge(self, start_id, dest_id):
        '''
        Returns the edge connecting the vertex with id start_id to the vertex with
        id dest_id in a tuple of the form (start_id, dest_id, weight)
        :param start_id: starting vertex
        :param dest_id: destination vertex
        :return: [tuple] edge connecting starting and destination vertex
        '''
        if start_id not in self.vertices or dest_id not in self.vertices:
            return None
        if dest_id not in self.vertices.get(start_id).adj:
            return None
        else:
            edge = (start_id, dest_id, self.vertices.get(start_id).adj[dest_id])
            return edge

    def get_edges(self):
        '''
        Returns a list of tuples representing all edges within the graph
        :return: [list] list of edges in graph
        '''
        edge_list = []
        if len(self.vertices) == 0:
            return edge_list
        for start_id in self.vertices:
            for dest_id in self.vertices.get(start_id).adj:
                edge = (start_id, dest_id, self.vertices.get(start_id).adj[dest_id])
                edge_list.append(edge)
        return edge_list

    def add_to_graph(self, start_id, dest_id=None, weight=0):
        '''
        Adds a vertex / vertices / edge to the graph
        :param start_id: starting vertex
        :param dest_id: destination vertex
        :param weight: weight of edge between start and dest vertex
        '''
        if self.get_vertex(start_id) is None and start_id is not None: # add startid vertex
            v = Vertex(start_id)
            self.vertices[start_id] = v
            self.size += 1
        if self.get_vertex(dest_id) is None and dest_id is not None: # add destid vertex
            v = Vertex(dest_id)
            self.vertices[dest_id] = v
            self.size += 1
        if self.get_edge(start_id, dest_id) is not None and start_id is not None and dest_id is not None:
            self.vertices.get(start_id).adj[dest_id] = weight
        if self.get_edge(start_id, dest_id) is None and start_id is not None and dest_id is not None:
            self.vertices.get(start_id).adj[dest_id] = weight

    def construct_from_matrix(self, matrix):
        '''
        Constructs a graph from a given adjacency matrix representation
        :param matrix: 2D list to turn into a graph
        '''
        if len(matrix[0]) == 0:
            return matrix
        for row in range(len(matrix)):
            for col in range(0, len(matrix)):
                if matrix[row][col]:
                    self.add_to_graph(matrix[row][0], matrix[0][col], matrix[row][col])

    def construct_from_csv(self, csv):
        '''
        EXTRA CREDIT
        '''
        pass

    def construct_matrix_from_graph(self):
        '''
        EXTRA CREDIT
        '''
        pass

    def bfs(self, start_id, target_id):
        '''
        Perform a breadth-first search beginning at vertex with id start_id
        and terminating at vertex with id end_id
        :param start_id: starting vertex
        :param target_id: starting vertex
        :return: [tuple] return path of vertices and distance of path
        '''
        path = []
        distance = 0
        q = queue.Queue()
        if start_id not in self.vertices or target_id not in self.vertices:
            bfs_tuple = (path, distance)
            return bfs_tuple

        path.append(start_id)
        q.put(path)
        while q.empty() is False:
            bfs_path = q.get()
            last_node = bfs_path[len(bfs_path)-1]
            if last_node != target_id:
                for v in self.vertices:
                    if v not in path:
                        path += v
                        q.put(path)
                        bfs_path = q.get()
                        if v == start_id:
                            distance += 0
                        else:
                            distance += self.vertices.get(last_node).adj[v]
                            if v == target_id:

                                bfs_tuple = (path, distance)
                                return bfs_tuple
                        last_node = bfs_path[len(bfs_path) - 1]

    def dfs(self, start_id, target_id):
        '''
        Wrapper function for _dfs_recursive
        :param start_id: starting vertex
        :param target_id: target vertex
        :return: [tuple] path vertices reversed and sum of weights
        '''
        dfs_recurse = self._dfs_recursive(start_id, target_id)
        dfs_list = dfs_recurse[0]
        weight = dfs_recurse[1]
        return (dfs_list[::-1], weight)

    def _dfs_recursive(self, current_id, target_id, path=[], dist=0):
        '''
        Performs the recursive work of depth-first search by searching for a path
        from vertex with id current_id to vertex with id target_id
        :param current_id: current vertex
        :param target_id: target vertex
        :param path: list of vertices in path
        :param dist: sum of weights in path
        :return: [tuple] list of path vertices and sum of weights
        '''
        if current_id not in self.vertices or target_id not in self.vertices:
            bfs_tuple = (path, dist)
            return bfs_tuple
        if current_id not in path:
            path.append(current_id)
        if current_id != target_id:

            for i in self.vertices[current_id].adj:
                if i not in path:
                    path.append(i)
                    path.reverse()
                    self._dfs_recursive(current_id, target_id, path, dist)
            dist += self.vertices.get(current_id).adj[target_id]
            bfs_tuple = (path, dist)
            return bfs_tuple

    def a_star(self, start_id, target_id):
        '''
        Perform a A* search beginning at vertex with id start_id
        and terminating at vertex with id end_id
        :param start_id: starting vertex
        :param target_id: target vertex
        :return: [tuple] list of path vertices and sum of weights
        '''
        # Was not able to start
        pass

    def make_equivalence_relation(self):
        '''
        EXTRA CREDIT
        '''
        pass



class AStarPriorityQueue:
    """
    Priority Queue built upon heapq module with support for priority key updates
    Created by Andrew McDonald
    Inspired by https://docs.python.org/2/library/heapq.html
    """

    __slots__ = ['__data', '__locator', '__counter']

    def __init__(self):
        """
        Construct an AStarPriorityQueue object
        """
        self.__data = []                        # underlying data list of priority queue
        self.__locator = {}                     # dictionary to locate vertices within priority queue
        self.__counter = itertools.count()      # used to break ties in prioritization

    def __repr__(self):
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        lst = [f"[{priority}, {vertex}], " if vertex is not None else "" for priority,
              count, vertex in self.__data]
        return "".join(lst)[:-1]

    def __str__(self):
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        return repr(self)

    def empty(self):
        """
        Determine whether priority queue is empty
        :return: True if queue is empty, else false
        """
        return len(self.__data) == 0

    def push(self, priority, vertex):
        """
        Push a vertex onto the priority queue with a given priority
        :param priority: priority key upon which to order vertex
        :param vertex: Vertex object to be stored in the priority queue
        :return: None
        """
        count = next(self.__counter)
        # list is stored by reference, so updating will update all refs
        node = [priority, count, vertex]
        self.__locator[vertex.id] = node
        heapq.heappush(self.__data, node)

    def pop(self):
        """
        Remove and return the (priority, vertex) tuple with lowest priority key
        :return: (priority, vertex) tuple where priority is key,
        and vertex is Vertex object stored in priority queue
        """
        vertex = None
        while vertex is None:
            # keep popping until we have valid entry
            priority, count, vertex = heapq.heappop(self.__data)
        del self.__locator[vertex.id]                   # remove from locator dict
        vertex.visit()                  # indicate that this vertex was visited
        return priority, vertex

    def update(self, new_priority, vertex):
        """
        Update given Vertex object in the priority queue to have new priority
        :param new_priority: new priority on which to order vertex
        :param vertex: Vertex object for which priority is to be updated
        :return: None
        """
        node = self.__locator.pop(vertex.id)    # delete from dictionary
        node[-1] = None                         # invalidate old node
        self.push(new_priority, vertex)  
