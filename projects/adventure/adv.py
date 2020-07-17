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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
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
def main_travel(length):
    path=[]
    visited={}
    #dive phase
    #it needs to look for a non-visited room, and go that direction
    stack = Stack()
    stack.push(player.current_room)
    running=True
    # diving=True
    # temp_visited, temp_path = df_stack(visited, path)
    # prev_room=() #stores as a tuple, (id, direction to flip)
    while running <5 :
        running=False
        # temp_visited, temp_path = df_stack(visited, path)
        # df_stack(visited, path)
        stack=Stack()
        # # location = player.current_room
        # # directions = location.get_exits()

        # pos_path=[]
        # exits={}
        # for item in player.current_room.get_exits():#[n, s, w, e]
        #     exits[item]="?"
        exits = player.current_room.get_exits()
        prev_node=() #stored as (id, direction)
        df_start= (player.current_room.id, prev_node, exits) #[(id#, (), {n:"?",s:"?",e:"?",w:"?"}, [])]
        stack.push(df_start)

        # # dft
        while stack.size() > 0:
            location = player.current_room
            current_pos = stack.pop()
            current_id, prev_node, available_directions= current_pos #possibly add a pos_path for path recording
            if current_id not in visited:
                visited[current_id]={}
                for direction in available_directions:
                    visited[location.id][direction]='?'
                #get as much free info in the node as possible
                if prev_node != ():
                    if prev_node[1] == 'n':
                        visited[location.id]['s'] = prev_node[0]
                    if prev_node[1] == 's':
                        visited[location.id]['n'] = prev_node[0]
                    if prev_node[1] == 'e':
                        visited[location.id]['w'] = prev_node[0]
                    if prev_node[1] == 'w':
                        visited[location.id]['e'] = prev_node[0]
                for key, value in visited[location.id].items():
                    if location.get_room_in_direction(key).id in visited:
                        visited[location.id][key]=location.get_room_in_direction(key).id
                        if key == 'n':
                            visited[location.get_room_in_direction(key).id]['s'] = location.id
                        if key == 's':
                            visited[location.get_room_in_direction(key).id]['n'] = location.id
                        if key == 'e':
                            visited[location.get_room_in_direction(key).id]['w'] = location.id
                        if key == 'w':
                            visited[location.get_room_in_direction(key).id]['e'] = location.id
                for key, value in visited[location.id].items():
                    if value == "?":
                        prev_node=(location.id, key)
                        path.append(key)
                        visited[location.id][key]=location.get_room_in_direction(key).id
                        player.travel(key)
                        location=player.current_room
                        # path_to_add= pos_path + [key]
                        #[(id#, None, {n:"?",s:"?",e:"?",w:"?"}, [path])]
                        stack.push((location.id, prev_node, location.get_exits()))
                        break
        #diving for the farthest node to the north
        # while diving:
        #     diving = False
        
        #     #slow solution, started just doing the whole thing over again so moved above
        #     location = player.current_room
        #     directions = location.get_exits()
        #     if location.id not in visited:
        #         visited[location.id]={}
        #         #builds the possible directions
        #         for direction in directions:
        #             visited[location.id][direction]='?'
        #         #updates the new visited room with the id of the room we were just in to get there
        #         if prev_room != ():
        #             if prev_room[1] == 'n':
        #                 visited[location.id]['s'] = prev_room[0]
        #             if prev_room[1] == 's':
        #                 visited[location.id]['n'] = prev_room[0]
        #             if prev_room[1] == 'e':
        #                 visited[location.id]['w'] = prev_room[0]
        #             if prev_room[1] == 'w':
        #                 visited[location.id]['e'] = prev_room[0]

        #         for key, value in visited[location.id].items():
        #             # print(key)
        #             if location.get_room_in_direction(key).id in visited:
        #                 visited[location.id][key]=location.get_room_in_direction(key).id
        #                 # visited[location.get_room_in_direction(key).id]
        #                 if key == 'n':
        #                     visited[location.get_room_in_direction(key).id]['s'] = location.id
        #                 if key == 's':
        #                     visited[location.get_room_in_direction(key).id]['n'] = location.id
        #                 if key == 'e':
        #                     visited[location.get_room_in_direction(key).id]['w'] = location.id
        #                 if key == 'w':
        #                     visited[location.get_room_in_direction(key).id]['e'] = location.id
        #     possible_directions=[]
        #     for key, value in visited[location.id].items():
        #         if value == '?':
        #             possible_directions.append(key)
        #     if len(possible_directions) > 0:
        #         choice = random.choice(possible_directions)
        #         diving=True
        #         path.append(choice)
        #         prev_room=(location.id, choice)
        #         visited[location.id][choice]=location.get_room_in_direction(choice).id
        #         player.travel(choice)
        #         print(player.current_room.id)
        #         print(location.id)
        #         break
            # print(visited)
            # print(path)
        #check if we're done
        #if we arent done, find the next place that we need to dive
        if len(visited) < length:
            # running+=1
            running=True
            diving=True
            backtrack_path = bfs(visited)
            print(path)
            
            # now that I have the back tracking path, I need to execute those moves and go back to the top of the loop
            for node in backtrack_path:
                if node[1] == None:
                    continue
                else:
                    # print('this is looping')
                    path.append(node[1])
                    player.travel(node[1])
        # print(len(visited))
        # print(player.current_room.id)
    # print(f'{temp_visited}, {temp_path}')
    return path


def df_stack(visited, path):
    #dft initialization
    stack=Stack()
    visited=visited
    # location = player.current_room
    # directions = location.get_exits()

    path=path
    # pos_path=[]
    # exits={}
    # for item in player.current_room.get_exits():#[n, s, w, e]
    #     exits[item]="?"
    exits = player.current_room.get_exits()
    prev_node=() #stored as (id, direction)
    df_start= (player.current_room.id, prev_node, exits) #[(id#, None, {n:"?",s:"?",e:"?",w:"?"}, [])]
    stack.push(df_start)

    # # dft
    while stack.size() > 0:
        location = player.current_room
        current_pos = stack.pop()
        current_id, prev_node, available_directions= current_pos #possibly add a pos_path for path recording
        if current_id not in visited:
            visited[current_id]={}
            for direction in available_directions:
                visited[location.id][direction]='?'
            #get as much free info in the node as possible
            if prev_node != ():
                if prev_node[1] == 'n':
                    visited[location.id]['s'] = prev_node[0]
                if prev_node[1] == 's':
                    visited[location.id]['n'] = prev_node[0]
                if prev_node[1] == 'e':
                    visited[location.id]['w'] = prev_node[0]
                if prev_node[1] == 'w':
                    visited[location.id]['e'] = prev_node[0]
            for key, value in visited[location.id].items():
                if location.get_room_in_direction(key).id in visited:
                    visited[location.id][key]=location.get_room_in_direction(key).id
                    if key == 'n':
                        visited[location.get_room_in_direction(key).id]['s'] = location.id
                    if key == 's':
                        visited[location.get_room_in_direction(key).id]['n'] = location.id
                    if key == 'e':
                        visited[location.get_room_in_direction(key).id]['w'] = location.id
                    if key == 'w':
                        visited[location.get_room_in_direction(key).id]['e'] = location.id
            for key, value in visited[location.id].items():
                if value == "?":
                    prev_node=(location.id, key)
                    path.append(key)
                    visited[location.id][key]=location.get_room_in_direction(key).id
                    player.travel(key)
                    location=player.current_room
                    # path_to_add= pos_path + [key]
                    #[(id#, None, {n:"?",s:"?",e:"?",w:"?"}, [path])]
                    stack.push((location.id, prev_node, location.get_exits()))
                    break
    return (visited, path)
            #check if visited
            #add room to stack
            #find all exits and mark with ?
            #pop current room from stack
            #add exits to stack
            #mark room as visited
            #select travel direction
            #replace ? with correct room id
            #set prev room to current room
            #traverse, current room to prev
            #set reverse direction to prev id
            #loop
        

def bfs(visited):
    queue = Queue()
    checked = {}
    location = player.current_room
    # directions = location.get_exits()
    #starting id
    backtrack_path=[(location.id, None)] #(ids, direction to add to path)
    # solution_path=[]
    queue.enqueue(backtrack_path)
    while queue.size() > 0:
        bfs_path= queue.dequeue()
        current_id= bfs_path[-1][0]
        if current_id not in checked:
            checked[current_id] = bfs_path
            for direction, room_id in visited[current_id].items():
                if room_id == '?':
                    backtrack_path = bfs_path
                    break
                path_to_add = bfs_path + [(room_id, direction)]
                queue.enqueue(path_to_add)
    return backtrack_path

# traversal_path = ['n', 'n']
traversal_path = main_travel(len(room_graph))
print(traversal_path)



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
