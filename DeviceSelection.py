from TdP_collections.graphs.graph import *
from TdP_collections.graphs.bfs import *
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
            self._graph.insert_edge(vertex1, self._start, 0)
            vertex2 = self._graph.insert_vertex(('secondPartition', elem, data[elem]))
            self._graph.insert_edge(vertex2, self._end, 1)
            self._graph.insert_edge(self._end, vertex2, 0)
            
        for vertex1 in self._graph.vertices():
            if vertex1.element()[0] == 'firstPartition':
                for vertex2 in self._graph.vertices():
                    if vertex2.element()[0] == 'secondPartition':
                        if self.__dominates(vertex1.element()[2], vertex2.element()[2]):
                            self._graph.insert_edge(vertex1, vertex2, 1)
                            self._graph.insert_edge(vertex2, vertex1, 0)
           
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
        
        maxMatching = self.__FordFulkerson(self._graph, self._start, self._end)
        
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

        for k,v in maxMatching.items():
            if k not in curr.keys():
                for k2,v2 in maxMatching.items():
                    if k == v2:
                        self._subsets[curr[k2]][v] = self._data[v]
            else:
                self._subsets[curr[k]][v] = self._data[v]        
        
        return count
    
    def _BFS(self, source, sink, path):

        visited = dict()
        for vertex in self._graph.vertices():
            visited[vertex] = False
        queue = []
        queue.append(source)
        visited[source] = True
        
        while queue:
            u = queue.pop(0)
            
            for e in self._graph.incident_edges(u):
                v = e.opposite(u)
                if not visited[v] and e.element() > 0:
                    queue.append(v)
                    visited[v] = True
                    path[v] = u
                    if v == sink:
                        return True

        return False
    
    def __FordFulkerson(self, G, source, sink):
            
        path = dict()
        max_matching = dict()
        
        for vertex in G.vertices():
            path[vertex] = -1
        
        while self._BFS(source, sink, path):
            b = self.__bottleneck(G, path, source, sink)
            self.__augment_path(G, path, source, sink, b, max_matching)
                
        return max_matching
            
    def __bottleneck(self, G, path, source, sink):
        
        path_flow = float("Inf")
        
        s = sink
        while s != source:
            path_flow = min(path_flow, G.get_edge(path[s], s).element())
            s = path[s]
            
        return path_flow
    
    def __augment_path(self, G, path, source, sink, b, max_matching):
    
        v = sink
        
        while (v != source):
            u = path[v]
            e = G.get_edge(u, v)
            e._element -= b
            if (u.element()[0] == 'firstPartition' and v.element()[0] == 'secondPartition'):
                max_matching[u.element()[1]] = v.element()[1]
            G.get_edge(v, u)._element += b
            v = u
            
    """
        Takes in input an integer i between 0 and C-1, and returns the string identifying the 
        device with highest rank in the i-th subset that has been not returned before, or None 
        if no further device exists (e.g., the first call of nextDevice(0) returns the device 
        with the highest rank in the first subset, i.e., the one that dominates all the remaining 
        devices in this subset, the second call returns the device with the second highest rank,
        and so on). The method throws an exception if the value in input is not in the range [0, C-1].
    """
    def nextDevice(self,i):

        tree = self._subsets[i]
        if not tree.is_empty():
            max = tree.first()
            tree.delete(max)
            return max.key()
        
        return None

class RedBlackTreeMap(RedBlackTreeMap):
    
    def __le__(self, other):
        for i in range(len(self.value())):
            if self.value()[i] >= other.value()[i]:
                return False
        return True