import sys

class Graph:

    def __init__(self, graph):

        self.graph = graph
        self.V = len(self.graph)

        self.node_weight = []
        self.crit_list = []

        self.start = 0
        self.end = self.V - 1

        self.start_node = None
        self.end_node = None

        self.expected_output = [[0, 5, 8, 4, 16, 0, 0, 6, 0, 0], [7, 0, 0, 10, 5, 0, 0, 0, 0, 0], [6, 0, 0, 0, 8, 3, 0, 0, 0, 0],
                                [0, 10, 0, 0, 4, 0, 3, 1, 0, 0], [16, 7, 6, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 6, 4, 0],
                                [0, 0, 0, 3, 0, 0, 0, 0, 0, 2], [0, 0, 0, 1, 6, 6, 0, 0, 1, 8], [0, 0, 0, 0, 0, 0, 2, 8, 0, 10],
                                [0, 0, 0, 0, 0, 4, 0, 1, 10, 0]]

    def node_sort(self, *args):
        if len(args) != self.V:
            print("Number of node names isn't equal to number of nodes specified")
            sys.exit("Re-enter data")

        print('Node Name\tNumber')

        for entry, name in enumerate(args):
            temp_list = [entry, name]
            self.node_weight.append(temp_list)
            print(name, '\t\t\t', entry)

        self.start_node = int(input("what is the start node number: "))
        self.end_node = int(input("what is the end node number: "))
        print(self.start_node)
        print(self.end_node)

        # swapping rows

        self.graph[0], self.graph[self.start_node] = self.graph[self.start_node], self.graph[0]
        self.graph[-1], self.graph[self.end_node] = self.graph[self.end_node], self.graph[-1]

        # swapping column entries in switched rows

        for x in range(len(self.graph)): # x=0
            self.graph[x][0], self.graph[x][self.start_node] = self.graph[x][self.start_node], self.graph[x][0]
            self.graph[x][-1], self.graph[x][self.end_node] = self.graph[x][self.end_node], self.graph[x][-1]
        print(self.graph == self.expected_output)

    def printSolution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initialize minimum distance for next node
        min = 1e7
        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            # dist[v] is the node we're currently looking at
            # min is the smallest weight out of all the ones looked at so far,
            # so out of all the adjacent nodes to the current one, if one has the smallest total weight,
            # and hasn't been visited yet (sptSet[v] == False), then it is demmed to be the next node it will work from
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    # Function that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        if len(self.graph) != self.V:
            print("Number of nodes specified isn't equal to number of nodes in matrix")
            sys.exit("Re-enter data")

        # sets all the nodes as having weights of 1e7 ('infinitely big') so all compared weights to a new node
        # will be smaller
        dist = [1e7] * self.V
        # sets the  first node as having a weight of 0
        dist[src] = 0

        # list to track what nodes have already been processed, if processed, value is changed to True
        sptSet = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                        sptSet[v] == False and
                        dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]
                    # dist[u] is the weight of the node we're working from, and graph[u][v] is the weight between u and
                    # v, so dist[v] is the new weight of the node, the previous total weight so far + the weight between
                    # the two.
                    # print(f'dist_v:{dist[v]}, dist_u:{dist[u]}, graph_uv:{self.graph[u][v]}')

        self.node_weight = dist
        self.printSolution(dist)

    def crit_path(self):
        # print(f"node_weight: {self.node_weight}")
        u = self.end
        print(len(self.graph[u]))
        while True:
            for v in range(len(self.graph[u])):
                if self.graph[u][v] != 0 and self.node_weight[u] - self.node_weight[v] == self.graph[u][v]:
                    self.crit_list.append(self.node_weight[u])
                    u = v

            if u == 0:
                self.crit_list.append(self.node_weight[u])
                break
        print(self.crit_list)

        ## will print out all connecting nodes to a chosen node 'v'
        # for u in range(self.V-1, -1, -1):  # TODO u represents the node were currently at
        #     for v in range(self.V):  # TODO v represents the node we're comparing to the current one
        #         if self.graph[u][v] !=0 and v<u:  # TODO 'self.graph[u][v]' represents the weight of the branch
        #             print(self.graph[u][v])
        #     print("*" * 20)


# Driver program

# g = Graph([
#     [0,5,8,4,16,0,0,6,0,0],
#     [5,0,0,10,7,0,0,0,0,0],
#     [8,0,0,0,6,3,0,0,0,0],
#     [4,10,0,0,0,0,3,1,0,0],
#     [16,7,6,0,0,0,0,0,0,0],
#     [0,0,3,0,0,0,0,6,0,4],
#     [0,0,0,3,0,0,0,0,2,0],
#     [6,0,0,1,0,6,0,0,8,1],
#     [0,0,0,0,0,0,2,8,0,10],
#     [0,0,0,0,0,4,0,1,10,0]
# ])  # start and end nodes are now D and H respectively


# g = Graph([
#     [0, 6, 9, 0, 0, 0, 0, 0, 0, 0],
#     [6, 0, 1, 2, 5, 0, 0, 0, 0, 0],
#     [9, 1, 0, 0, 2, 3, 0, 0, 0, 0],
#     [0, 2, 0, 0, 4, 0, 0, 0, 0, 10],
#     [0, 5, 2, 4, 0, 3, 2, 4, 0, 8],
#     [0, 0, 3, 0, 3, 0, 0, 5, 0, 0],
#     [0, 0, 0, 0, 2, 0, 0, 6, 2, 5],
#     [0, 0, 0, 0, 4, 5, 6, 0, 5, 0],
#     [0, 0, 0, 0, 0, 0, 2, 5, 0, 2],
#     [0, 0, 0, 10, 8, 0, 5, 0, 2, 0]
# ])


# g = Graph([[0, 4, 0, 0, 0, 0, 0, 8, 0],
#            [4, 0, 8, 0, 0, 0, 0, 11, 0],
#            [0, 8, 0, 7, 0, 4, 0, 0, 2],
#            [0, 0, 7, 0, 9, 14, 0, 0, 0],
#            [0, 0, 0, 9, 0, 10, 0, 0, 0],
#            [0, 0, 4, 14, 10, 0, 2, 0, 0],
#            [0, 0, 0, 0, 0, 2, 0, 1, 6],
#            [8, 11, 0, 0, 0, 0, 1, 0, 7],
#            [0, 0, 2, 0, 0, 0, 6, 7, 0]
#            ])

g = Graph([[0, 7, 6, 0, 16, 0, 0, 0, 0, 0], [7, 0, 0, 10, 5, 0, 0, 0, 0, 0], [6, 0, 0, 0, 8, 3, 0, 0, 0, 0],
           [0, 10, 0, 0, 4, 0, 3, 1, 0, 0], [16, 5, 8, 4, 0, 0, 0, 6, 0, 0], [0, 0, 3, 0, 0, 0, 0, 6, 4, 0],
           [0, 0, 0, 3, 0, 0, 0, 0, 0, 2], [0, 0, 0, 1, 6, 6, 0, 0, 1, 8], [0, 0, 0, 0, 0, 4, 0, 1, 0, 10],
           [0, 0, 0, 0, 0, 0, 2, 8, 10, 0]])

g.node_sort('d', 'a', 'b', 'c', 's', 'e', 'f', 'g', 't', 'h')

g.dijkstra(0)

g.crit_path()
