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
        maxMatch, residual, maxflow = self.__FordFulkerson(self._graph)
        
        # all the nodes not taking part to the maximum matching are in separate subsets
        subsets = dict()
        involved = set()
        i = 0
        for m in maxMatch:
            first, second = m.endpoints()
            subsets[i] = {first.element()[1], second.element()[1]}
            involved.add(first.element()[1])
            involved.add(second.element()[1])
            i += 1
        
        for i in range(len(subsets)-1):
            if not subsets[i].isdisjoint(subsets[i+1]):
                subsets[i] = subsets[i].union(subsets[i+1])
                del subsets[i+1]
                
        for n in self._N:
            if n not in involved:
                subsets[len(subsets)] = {n}
                
        self._subsets = subsets
        
        self._max = {}
 
        for i in range (len(subsets)):
            self._max[i] = RedBlackTreeMap()
            for elem in subsets[i]:
                self._max[i][elem] = self._data[elem]

        return len(subsets)
    
    def __FordFulkerson(self, graph : Graph):
        flow = dict()
        maxMatch = []
        maxflow = 0
        for edge in graph.edges():
            flow[edge] = 0
            
        residual = self.__residual(graph, flow)
        
        paths = self.__buildPaths()
        
        for i in range (len(paths)):
            b = self.__bottleneck(paths[i])
            if b == 1:
                maxMatch.append(paths[i][1])
            maxflow += b
            flow = self.__augment(flow, paths[i], b)
            residual = self.__residual(graph, flow)
            paths = self.__buildPaths()
            
        return maxMatch, residual, maxflow

    def __buildPaths(self):
        paths = dict()
        i=0
        for e in self._graph.incident_edges(self._start):
            v = e.opposite(self._start)
            if self._graph.degree(v) > 0:
                paths[i] = [e]
                other = False
                for e2 in self._graph.incident_edges(v):
                    if other:
                        i += 1
                        paths[i] = [e]
                    else:
                        other = True
                    paths[i].append(e2)
                    v2 = e2.opposite(v)
                    paths[i].append(self._graph.get_edge(v2, self._end))
                i += 1    
        return paths 
        
    def __residual(self, graph, flow):
        residual = dict()
        for edge in graph.edges():
            residual[edge] = edge.element() - flow[edge]
        return residual
       
    def __augment(self, f, P, b):
        for edge in P:
            # since we only have forward edges in our graph 
            edge._element -= b
            f[edge] += b
        return f       
        
    def __bottleneck(self, P):
        min = P[0].element()
        for i in range (1, len(P)):
            if P[i].element() < min:
                min = P[i].element()
        return min

    """
        Takes in input an integer i between 0 and C-1, and returns the string identifying the 
        device with highest rank in the i-th subset that has been not returned before, or None 
        if no further device exists (e.g., the first call of nextDevice(0) returns the device 
        with the highest rank in the first subset, i.e., the one that dominates all the remaining 
        devices in this subset, the second call returns the device with the second highest rank,
        and so on). The method throws an exception if the value in input is not in the range [0, C-1].
    """
    def nextDevice(self,i):

        tree = self._max[i]
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