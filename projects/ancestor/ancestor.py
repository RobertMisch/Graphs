class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# queue = Queue()
# visited = set()
# #for mental clarity
# starting_path=[starting_vertex]

# queue.enqueue(starting_path)
# while queue.size() > 0:
#     path= queue.dequeue()
#     current_pos= path[-1]
#     # current_pos=path.pop() originally had this, but can just do [-1]
#     # path.append(current_pos)
#     if current_pos not in visited:
#         visited.add(current_pos)
#         #check if it's the guy
#         if current_pos == destination_vertex:
#             return path

#         for neighbor in self.get_neighbors(current_pos):
#             path_to_add= path + [neighbor]
#             queue.enqueue(path_to_add)

def earliest_ancestor(ancestors, starting_node):
    #our graph
    verticies={}
    #build our nodes 
    for vert in ancestors:
        #note, recieving tuples in form (parent, child)
        if vert[1] not in verticies:
            verticies[vert[1]]=set()
            verticies[vert[1]].add(vert[0])
        else:
            verticies[vert[1]].add(vert[0])
    #bfs our nodes
    queue = Queue()
    visited = set()

    starting_path=[starting_node]
    queue.enqueue(starting_path)

    #save the paths
    #if we find a longer path, wipe saved paths and continue search
    #if we find an equal length path, save to list of possible longest paths
    #once our queue is depleted, check our list of possible answers, and pick the one with the largest [-1]
    pass
"""
generally what we have to do

-need to build the 1d verts, we've actually been doing this, but the tests have always made a vert each way 
so we just need the same node with a list of it's ancestors

-after we build our graph of ancestors, we want to travel to it's verticies. 
-we should save the path as we continue down
-bfs vs dfs. dfs would get us deep, but we know for a fact that the last things found in bfs are older
"""