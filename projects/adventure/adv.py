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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
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
    path = []
    visited = {}
    running = True
    # running = 0
    while running:
        running = False
        # print(visited)
        df_stack(visited, path)
        # print(player.current_room.id)
        # print(path)
        if len(visited) < len(room_graph):
            running = True
            backtrack_path = bfs(visited)
            # print(path)
            # now that I have the back tracking path, I need to execute those moves and go back to the top of the loop
            for node in backtrack_path:
                if node[1] == None:
                    continue
                else:
                    path.append(node[1])
                    player.travel(node[1])

    return path

def df_stack(visited, path):
    # dft initialization
    stack = Stack()

    exits = player.current_room.get_exits()
    prev_node = ()  # stored as (id, direction)
    # [(id#, None, {n:"?",s:"?",e:"?",w:"?"}, [])]
    df_start = (player.current_room.id, prev_node, exits)
    stack.push(df_start)
    # # dft
    while stack.size() > 0:
        location = player.current_room
        current_pos = stack.pop()
        current_id, prev_node, available_directions = current_pos
        if current_id not in visited:
            visited[current_id] = {}
            for direction in available_directions:
                visited[location.id][direction] = '?'

            # get as much free info in the node as possible
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
                looking_at = location.get_room_in_direction(key)
                visited[location.id][key] = looking_at.id
                if key == 'n':
                    visited[looking_at.id]['s'] = location.id
                if key == 's':
                    visited[looking_at.id]['n'] = location.id
                if key == 'e':
                    visited[looking_at.id]['w'] = location.id
                if key == 'w':
                    visited[looking_at.id]['e'] = location.id
                    
        possible_directions=[]
        for key, value in visited[location.id].items():
            if value == '?':
                possible_directions.append(key)
        # print(possible_directions)
        if len(possible_directions) > 0:
            choice = random.choice(possible_directions)
            prev_node = (location.id, choice)
            path.append(choice)
            visited[location.id][choice] = location.get_room_in_direction(choice).id
            player.travel(choice)
            location = player.current_room
            stack.push((location.id, prev_node, location.get_exits()))
            
        # for key, value in visited[location.id].items():
        #     if value == "?":
        #         prev_node = (location.id, key)
        #         path.append(key)
        #         visited[location.id][key] = location.get_room_in_direction(
        #             key).id
        #         player.travel(key)
        #         location = player.current_room
        #         stack.push((location.id, prev_node, location.get_exits()))
        #         break
    return (visited, path)

def bfs(visited):
    queue = Queue()
    checked = {}
    location = player.current_room
    backtrack_path = [(location.id, None)]  # (ids, direction to add to path)
    queue.enqueue(backtrack_path)
    while queue.size() > 0:
        bfs_path = queue.dequeue()
        current_id = bfs_path[-1][0]
        if current_id not in checked:
            checked[current_id] = bfs_path
            for direction, room_id in visited[current_id].items():
                if room_id == '?':
                    backtrack_path = bfs_path
                    break
                path_to_add = bfs_path + [(room_id, direction)]
                queue.enqueue(path_to_add)
    return backtrack_path

# def look_around(looking_at):
#     if location.get_room_in_direction(key).id in visited:
#         looking_at = location.get_room_in_direction(key).id
#         visited[location.id][key] = looking_at
#         if key == 'n':
#             visited[looking_at]['s'] = location.id
#         if key == 's':
#             visited[looking_at]['n'] = location.id
#         if key == 'e':
#             visited[looking_at]['w'] = location.id
#         if key == 'w':
#             visited[looking_at]['e'] = location.id

traversal_path = main_travel(len(room_graph))
# print(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
