from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# visited[player.current_room.id]={'n': '?', 's': '?', 'w': '?', 'e': '?'}
# player.current_room.get_exits()
# player.travel(direction)
# player.current_room.get_room_in_direction(direction)

# OBJECTIVES
"""
find an unexplored direction, and follow it until df finds an end with explored directions
"""
def df_travel(length):
    path=[]
    visited={}
    #dive phase
    #it needs to look for a non-visited room, and go that direction
    # stack = Stack()
    # stack.push(player.current_room)
    running=True
    diving=True
    searching=False

    prev_room=() #stores as a tuple, (id, direction to flip)
    while running:
        running=False
        #diving for the farthest node to the north
        while diving:
            diving=False
            location = player.current_room
            directions = location.get_exits()
            if location.id not in visited:
                visited[location.id]={}
                #builds the possible directions
                for direction in directions:
                    visited[location.id][direction]='?'
                #updates the new visited room with the id of the room we were just in to get there
                if prev_room != ():
                    if prev_room[1] == 'n':
                        visited[location.id]['s'] = prev_room[0]
                    if prev_room[1] == 's':
                        visited[location.id]['n'] = prev_room[0]
                    if prev_room[1] == 'e':
                        visited[location.id]['w'] = prev_room[0]
                    if prev_room[1] == 'w':
                        visited[location.id]['e'] = prev_room[0]
            for key, value in visited[location.id].items():
                if value == '?':
                    diving=True
                    path.append(key)
                    prev_room=(location.id, key)
                    visited[location.id][key]=location.get_room_in_direction(key).id
                    player.travel(key)
                    # print(player.current_room.id)
                    # print(location.id)
                    break
            print(visited)
        #check if we're done
        #if we arent done, find the next place that we need to dive
        if len(visited) < length:
            # running=True

            queue = Queue()
            checked = {}
            #starting id
            solution_path=[(location.id, None)] #(ids, direction to add to path)
            # solution_path=[]
            queue.enqueue(solution_path)
            while queue.size() > 0:
                bfs_path= queue.dequeue()
                current_id= bfs_path[-1][0]
                if current_id not in checked:
                    checked[current_id] = bfs_path
                    for direction, room_id in visited[current_id].items():
                        if room_id == '?':
                            solution_path = bfs_path
                            break
                        path_to_add = bfs_path + [(room_id, direction)]
                        queue.enqueue(path_to_add)
            print(solution_path)
                #what do I need. 
                # I need a path of id's to follow
                # to make that path of id's I have to put in an id, and then queue up checking all the ids it has                    

    return path

# df_travel()
        

def bfs(starting_room):
    pass
# traversal_path = ['n', 'n']
traversal_path = df_travel(len(room_graph))



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
