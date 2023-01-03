from TdP_collections.graphs.graph import *
from TdP_collections.graphs.bfs import *
from TdP_collections.graphs.bfs import BFS_complete
from TdP_collections.map.red_black_tree import *

class DeviceSelection:

    """
        N is a tuple of strings identifying the devices, 
        X is an integer, and data is a dictionary whose keys are the elements of N, and whose 
        values are tuples of X-2 elements describing the performances of the corresponding 
        device over sentences from 3-term to X-term.
    """
    
    def __init__(self,N, X, data):
        self._N = N
        self._X = X
        self._data = data
        
        self._graph = Graph(True)
        self._start = self._graph.insert_vertex('start')
        self._end = self._graph.insert_vertex('end')
        
        for elem in self._N:
            vertex1 = self._graph.insert_vertex(('firstPartition', elem, data[elem]))
            self._graph.insert_edge(self._start, vertex1, 1)
            vertex2 = self._graph.insert_vertex(('secondPartition', elem, data[elem]))
            self._graph.insert_edge(vertex2, self._end, 1)
            
        for vertex1 in self._graph.vertices():
            if vertex1.element()[0] == 'firstPartition':
                for vertex2 in self._graph.vertices():
                    if vertex2.element()[0] == 'secondPartition':
                        if self.__dominates(vertex1.element()[2], vertex2.element()[2]):
                            self._graph.insert_edge(vertex1, vertex2, 1)
           
    def __dominates(self, t1, t2):
        for i in range (self._X-2):
            if t2[i] >= t1[i]:
                return False
        return True

    """
        Returns the minimum number C of devices for which we need to run the expensive tests. 
        That is, C is the number of subsets in which the devices are partitioned so that every 
        subset satisfies the non-interleaving property.
    """
    def countDevices(self,):
        
        maxFlow = self.__FordFulkerson(self._graph, self._start, self._end)
        
        maxMatching = dict()
        # conta = 0
        # for e in self._graph.edges():
        #     first, second = e.endpoints()
        #     if (first.element()[0] == 'firstPartition' and second.element()[0] == 'secondPartition'):
        #         print(first.element()[1], second.element()[1])
        #         conta += 1
                
        # print(maxFlow, conta)
        
        self._subsets = dict()
        curr = dict()
        
        count = 0
        
        for n in self._N:
            if n not in maxMatching.values():
                self._subsets[count] = RedBlackTreeMap()
                self._subsets[count][n] = self._data[n]
                if n in maxMatching.keys():
                    curr[n] = count
                count += 1
                
        # for k,v in self._subsets.items():
        #     print(k, v.first().key())
            
        # print(maxFlow)

        # for k,v in maxMatching.items():
        #     if k not in curr.keys():
        #         for k2,v2 in maxMatching.items():
        #             if k == v2:
        #                 self._subsets[curr[k2]][v] = self._data[v]
        #     else:
        #         self._subsets[curr[k]][v] = self._data[v]        
        
        return 1
    
    def bfs(self, s, t, parent):

        # Mark all the vertices as not visited
        visited = [False] * self.row

        # Create a queue for BFS
        queue = collections.deque()

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS loop
        while queue:
            u = queue.popleft()

            # Get all adjacent vertices of the dequeued vertex u
            # If an adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if (visited[ind] == False) and (val > 0):
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        # If we reached sink in BFS starting from source, then return
        # true, else false
        return visited[t]

    # Returns the maximum flow from s to t in the given graph
    def edmonds_karp(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1] * self.row

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.bfs(source, sink, parent):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow
    
    # def __FordFulkerson(self, G, source, sink):
            
    #     max_flow = 0
        
    #     path = self.__bfs(G, source, sink, [])

    #     while path:
    #         # path = path[1:-1]
    #         # b = self.__bottleneck(G, path)
    #         # self.__augment_path(path, G, b)
    #         # max_flow += b
    #         path = self.__bfs(G, source, sink, [])
                
    #     return max_flow
    
    # def __bfs(self, graph, source, sink, path):
        
    #     if source == sink:
    #         return path
        
    #     for e in graph.incident_edges(source):
            
    #         if e not in path:
    #             if e.element() > 0:
    #                 print(e.element())
    #                 return self.__bfs(graph, e.opposite(source), sink, path + [e])
        
    #     return None
            
    # def __bottleneck(self, graph, path):
        
    #     path_flow = float("Inf")

    #     i = 0
    #     while(i < len(path)-1):
    #         e = graph.get_edge(path[i], path[i+1])
    #         if e.element() < path_flow:
    #             path_flow = e.element()
    #         i += 1

    #     return path_flow
    
    # def __augment_path(self, path, graph, b):
        
    #     i = 0
    #     while(i < len(path)-1):
    #         e = graph.get_edge(path[i], path[i+1])
    #         e._element -= b
    #         if graph.get_edge(path[i+1], path[i]) == None:
    #             graph.insert_edge(path[i+1], path[i], 0)
    #         graph.get_edge(path[i+1], path[i])._element += b
    #         i += 1
            
    """
        Takes in input an integer i between 0 and C-1, and returns the string identifying the 
        device with highest rank in the i-th subset that has been not returned before, or None 
        if no further device exists (e.g., the first call of nextDevice(0) returns the device 
        with the highest rank in the first subset, i.e., the one that dominates all the remaining 
        devices in this subset, the second call returns the device with the second highest rank,
        and so on). The method throws an exception if the value in input is not in the range [0, C-1].
    """
    def nextDevice(self,i):

        # tree = self._subsets[i]
        # if not tree.is_empty():
        #     max = tree.first()
        #     tree.delete(max)
        #     return max.key()
        
        return None

class RedBlackTreeMap(RedBlackTreeMap):
    
    def __le__(self, other):
        for i in range(len(self.value())):
            if self.value()[i] >= other.value()[i]:
                return False
        return True