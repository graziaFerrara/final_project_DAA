from TdP_collections.graphs.graph import *

class DeviceSelection:

    """
    A class used for the selection of the devices to be tested.
    
    Attributes
    ----------
    _graph : Graph
        A graph whose vertices are the devices and whose edges represent the dominance relation.
    _start : Vertex
        The vertex representing the start of the graph.
    _end : Vertex
        The vertex representing the end of the graph.
    _subsets : dict
        A dictionary whose keys are integer indices and whose values are lists of devices in order of dominance.
        
    Methods
    -------
    countDevices()
        Returns the minimum number C of devices for which we need to run the expensive tests.
    nextDevice()
        Returns the next device to be tested.
    """
    
    def __init__(self, N, X, data):
        """
        Initializes the DeviceSelection object.
        
        Parameters
        ----------
        N : tuple
            A tuple of strings identifying the devices.
        X : int
            Number of elements in the tuple of performances + 2
        data : dict()
            A dictionary whose keys are the elements of N, 
            and whose values are tuples of X-2 elements describing
            the performances of the corresponding device over
            sentences from 3-term to X-term.
            
        Time complexity
        ---------------
        Since first we have a for loop all over the n devices, and then we have to iterate both
        over the first and the second partition's vertices, then the time complexity is O(n^2).
        """
        
        self._graph = Graph(True)
        self._start = self._graph.insert_vertex('start')
        self._end = self._graph.insert_vertex('end')
        
        firstPartition = set()
        secondPartition = set()
        
        for elem in N:
            vertex1 = self._graph.insert_vertex(('firstPartition', elem))
            firstPartition.add(vertex1)
            self._graph.insert_edge(self._start, vertex1, 1)
            vertex2 = self._graph.insert_vertex(('secondPartition', elem))
            secondPartition.add(vertex2)
            self._graph.insert_edge(vertex2, self._end, 1)
            
        for vertex1 in firstPartition:
            for vertex2 in secondPartition:
                if self.__dominates(data[vertex1.element()[1]], data[vertex2.element()[1]], X-2):
                    self._graph.insert_edge(vertex1, vertex2, 1)
           
    def __dominates(self, t1, t2, size):
        """ 
        Function to check if a device dominates one another.
        
        Parameters
        ----------
        t1 : tuple
            A tuple of performances of the first device.
        t2 : tuple
            A tuple of performances of the second device.
        size : int
            The number of elements in the tuple.
        
        Returns
        -------
        True if t1 dominates t2, False otherwise.
        
        Time complexity
        ---------------
        This function runs at most in O(size) time.
        """
        for i in range(size):
            if t1[i] <= t2[i]:
                return False
        return True

    def countDevices(self):
        """
        Returns the minimum number C of devices for which we need to run the expensive tests. 
        That is, C is the number of subsets in which the devices are partitioned so that every 
        subset satisfies the non-interleaving property.
        
        Returns
        -------
        count : int
            The minimum number of devices for which we need to run the expensive tests.

        Time complexity
        ---------------
        Thif function calls the Ford-Fulkerson algorithm on the graph, which runs in O(m*n). Then
        if loops through the edges incident to the sink vertex, which runs in O(n). Finally, it loops
        all over the dominators (which have been computed in the previous loop so they have to be
        less than n) and for each of them it creates a new subset and loops through the dominators
        in the maxMatching dictionary starting from the current dominator. This takes at most O(n^2).
        So the time complexity of this function is O(n^2*m).
        """
        maxMatching = self.__FordFulkerson(self._graph, self._start, self._end)
        
        dominators = []
        for edge in self._graph.incident_edges(self._end, False):
            if edge.element() == 1:
                dominators.append(edge.opposite(self._end).element()[1])
        
        self._subsets = dict()
        count = 0
        for d in dominators:
            self._subsets[count] = [d]
            try:
                while maxMatching[d]:
                    value = maxMatching[d]
                    self._subsets[count].append(value)
                    d = value
            except:
                count += 1
        
        return count
    
    def __BFS(self, source, sink, path):
        """
        This function performs a BFS on the graph to find an augmenting path from source to sink. An augmenting path
        contains only edges with non-zero weight.
        
        Parameters
        ----------
        source : Vertex
            The source vertex.
        sink : Vertex
            The sink vertex.
        path : dict
            A dictionary whose keys are the vertices of the graph and whose values are their predecessor vertex in the path from source to sink.
            
        Returns
        -------
        true if a path from source to sink exists, false otherwise.
        
        Time complexity
        ---------------
        Let n = |X| = |Y| and m = |E| be the number of vertices and edges in the graph. We assume that there is at least one edge
        incident to each node in the original problem and hence m >= n/2. Made this assumption, the time complexity of the BFS
        O(n+m) is the same as O(m) in such a case. 
        """

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
        """ 
        This function performs the Ford-Fulkerson algorithm on the graph. 
        It works on a network flow (which has been previously initialized) adding a sorurce and a sink to the original biparite
        graph and a weigth of 1 on each edge. The algorithm finds the maximum matching in the graph. A maximum matching is a
        set of edges such that no two edges share a vertex and the number of edges in the set is maximum. 
        
        Parameters
        ----------
        G : Graph
            The graph on which the algorithm is performed.
        source : Vertex
            The source vertex.
        sink : Vertex
            The sink vertex.
        
        Returns
        -------
        max_matching : dict
            A dictionary whose keys are the vertices of the first partition and whose values are the vertices of the second partition.
        
        Time complexity
        ---------------
        Let n = |X| = |Y| and m = |E| be the number of vertices and edges in the graph. We assume that there is at least one edge
        incident to each node in the original problem and hence m >= n/2. The time to compute a maximum matching is dominated by 
        the time to compute an integer valued maximum flow in the residual graph. For the flow problem we have that C is the sum 
        of the weights of the edges out of the source (which are equal to 1) and go into each node of X, so the total is n.
        For this reasons the total complexity is O(m*n).
        """
        
        path = dict()
        max_matching = dict()
        
        while self.__BFS(source, sink, path):
            self.__augment(G, path, source, sink, max_matching)
                
        return max_matching
            
    def __bottleneck(self, G, path, source, sink):
        """ 
        The __bottleneck function scans the path from the sink to the source
        and finds the minimum weight of the edges in the path. 
        
        Parameters
        ----------
        G : Graph
            The graph on which the algorithm is performed.
        path : dict
            A dictionary whose keys are the vertices of the graph and whose values are their predecessor vertex in the path from source to sink.
        source : Vertex
            The source vertex.
        sink : Vertex
            The sink vertex.
            
        Returns 
        -------
        path_flow : int
            The minimum weight of the edges in the path.
            
        Time complexity
        ---------------
        Since the function scans the path from the sink to the source, the time complexity is proportional to the length of the path.
        The time complexity is O(n), as the path has at most n-1 edges.
        """
        
        path_flow = float("Inf")
        
        s = sink
        while s != source:
            path_flow = min(path_flow, G.get_edge(path[s], s).element())
            s = path[s]
            
        return path_flow
    
    def __augment(self, G, path, source, sink, max_matching):
        """ 
        The __augment function calls the __bottleneck function to find the bottleneck of the path.
        It scans the path from the sink to the source and updates the weights of the edges in the path.
        It also updates the maximum matching.
        
        Parameters
        ----------
        G : Graph
            The graph on which the algorithm is performed.
        path : dict
            A dictionary whose keys are the vertices of the graph and whose values are their predecessor vertex in the path from source to sink.
        source : Vertex
            The source vertex.
        sink : Vertex
            The sink vertex.
        max_matching : dict
            A dictionary whose keys are the vertices of the first partition and whose values are the vertices of the second partition.
            
        Time complexity
        ---------------
        Since we call the __bottleneck function which scans the path from the sink to the source, and we do the same in this function,
        the time complexity is proportional to the length of the path.
        The time complexity is O(n), as the path has at most n-1 edges.
        """
    
        b = self.__bottleneck(G, path, source, sink)
        
        v = sink
        while (v != source):
            u = path[v]
            G.get_edge(u, v)._element -= b
            # if the edge is not in the graph, we add it
            if G.get_edge(v, u) is None:
                G.insert_edge(v, u, 0)
            e = G.get_edge(v, u)
            e._element += b
            # if the flow is 1, then the 'middle' edge is in the maximum matching
            if (u.element()[0] == 'firstPartition' and v.element()[0] == 'secondPartition' and e.element() == 1):
                max_matching[u.element()[1]] = v.element()[1]
            v = u
            
    def nextDevice(self,i):
        """
        Takes in input an integer i between 0 and C-1, and returns the string identifying the 
        device with highest rank in the i-th subset that has been not returned before, or None 
        if no further device exists. The method throws an exception if the value in input is 
        not in the range [0, C-1].
        
        Parameters
        ----------
        i : int
            The index of the subset.
            
        Returns
        -------
        first : str
            The string identifying the device with highest rank in the i-th subset that has been not returned before.
            
        Raises
        ------
        Exception
            If the value in input is not in the range [0, C-1].
            
        Time complexity
        ---------------
        The time complexity is O(1), as we pop the first element of the list.
        """
        if i < 0 or i >= len(self._subsets):
            raise Exception('Index out of range')

        list = self._subsets[i]
        if not len(list) == 0:
            first = list.pop(0)
            return first
        
        return None
