"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id]= set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print('v1 dne')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        queue = Queue()
        visited = set()
        queue.enqueue(starting_vertex)
        while queue.size() > 0:
            v= queue.dequeue()
            if v not in visited:
                visited.add(v)
                print(f'{v}')
                for neighbor in self.get_neighbors(v):
                    queue.enqueue(neighbor)


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        stack = Stack()
        visited = set()
        stack.push(starting_vertex)
        while stack.size() > 0:
            v= stack.pop()
            if v not in visited:
                visited.add(v)
                print(f'{v}')
                for neighbor in self.get_neighbors(v):
                    stack.push(neighbor)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        #set up
        stack=Stack()
        visited=set()
        # result=[]
        def dft_inner(current_vertex):
            if current_vertex == None:
                return
            else:
                if current_vertex not in visited:
                    print(current_vertex)
                    # result.append(current_vertex)
                    visited.add(current_vertex)
                    for neighbor in self.get_neighbors(current_vertex):
                        stack.push(neighbor)
                    # stack.pop()
                    dft_inner(stack.pop())
                else:
                    dft_inner(stack.pop())
        dft_inner(starting_vertex)
        # return print(result)
        


    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        queue = Queue()
        visited = set()
        #for mental clarity
        starting_path=[starting_vertex]

        queue.enqueue(starting_path)
        while queue.size() > 0:
            path= queue.dequeue()
            current_pos=path.pop()
            path.append(current_pos)
            if current_pos not in visited:
                visited.add(current_pos)
                #check if it's the guy
                if current_pos == destination_vertex:
                    return path

                for neighbor in self.get_neighbors(current_pos):
                    path_to_add= path + [neighbor]
                    queue.enqueue(path_to_add)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        stack = Stack()
        visited = set()
        #for mental clarity
        starting_path=[starting_vertex]

        stack.push(starting_path)
        while stack.size() > 0:
            path= stack.pop()
            current_pos=path.pop()
            path.append(current_pos)
            if current_pos not in visited:
                visited.add(current_pos)
                #check if it's the guy
                if current_pos == destination_vertex:
                    return path

                for neighbor in self.get_neighbors(current_pos):
                    path_to_add= path + [neighbor]
                    stack.push(path_to_add)

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        stack=Stack()
        visited=set()
        starting_path=[starting_vertex]
        stack.push(starting_path)
        def dft_inner(current_path):
            current_vertex = current_path.pop()
            current_path.append(current_vertex)
            # print(f'in loop {current_path}')
            # print(current_vertex)
            #end case
            if current_vertex == destination_vertex:
                # print(current_path)
                return current_path
            #continue case
            else:
                if current_vertex not in visited:
                    visited.add(current_vertex)
                    for neighbor in self.get_neighbors(current_vertex):
                        path_to_add= current_path + [neighbor]
                        stack.push(path_to_add)
                    return dft_inner(stack.pop())
                else:
                    return dft_inner(stack.pop())

        return dft_inner(starting_path)
        

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
