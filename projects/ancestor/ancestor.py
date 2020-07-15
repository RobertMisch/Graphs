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

def earliest_ancestor(ancestors, starting_node):
    #our graph
    verticies={}
    result=None
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

    #save the longest paths
    possible_solutions=[[]]
    

    #initialization
    starting_path=[starting_node]
    queue.enqueue(starting_path)

    while queue.size() > 0:
        path= queue.dequeue()
        current_pos= path[-1]
        if current_pos not in visited:
            visited.add(current_pos)
            if current_pos not in verticies:
                # path_to_add= path + [current_pos]
                # #if we find a longer path, wipe saved paths and continue search
                # if len(path_to_add) > len(possible_solutions[0]):
                #     possible_solutions = path_to_add
                # #if we find an equal length path, save to list of possible longest paths
                # elif len(path_to_add) == len(possible_solutions[0]):
                #     possible_solutions.append(path_to_add)
                # # possible_solutions.append(current_pos)
                continue
            for ancestor in verticies[current_pos]:
                    path_to_add= path + [ancestor]
                    queue.enqueue(path_to_add)
                    # if we find a longer path, wipe saved paths and continue search
                    if len(path_to_add) > len(possible_solutions[0]):
                        possible_solutions = [path_to_add]
                    #if we find an equal length path, save to list of possible longest paths
                    elif len(path_to_add) == len(possible_solutions[0]):
                        possible_solutions.append(path_to_add)
    #once our queue is depleted, check our list of possible answers, and pick the one with the largest [-1]
    if len(possible_solutions[0]) < 1:
        return -1

    result = possible_solutions[0][-1]
    for solution in possible_solutions:
        if solution[-1] < result:
            result = solution[-1]
    # print(result)
    return result
    # print(possible_solutions)
    # print(possible_solutions[-1])
"""
generally what we have to do

-need to build the 1d verts, we've actually been doing this, but the tests have always made a vert each way 
so we just need the same node with a list of it's ancestors

-after we build our graph of ancestors, we want to travel to it's verticies. 
-we should save the path as we continue down
-bfs vs dfs. dfs would get us deep, but we know for a fact that the last things found in bfs are older
"""

# test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
# print(earliest_ancestor(test_ancestors, 1))
# print(earliest_ancestor(test_ancestors, 2))
# print(earliest_ancestor(test_ancestors, 9))