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
def path_driver(player):
    pass
    # result=[]
    # result= test_dft(player)
    # result= rooms_to_path(result)


def test_dft(player):
    stack=Stack()
    path= []
    visited = set()
    stack.push(player.current_room)
    # print(player.current_room)
    while stack.size() > 0:
        current_room = stack.pop()
        # print(f"current {current_room}")
        if current_room.id not in visited:
            visited.add(current_room.id)
            path.append(current_room.id)
            for direction in current_room.get_exits(): #need something to actually get the neighbors
                stack.push(current_room.get_room_in_direction(direction))
    # print(path)
    return path

def bfs(player, target):
    queue = Queue()
    visited = set()
    path=[]
    starting_room=(player.current_room,[])

    queue.enqueue(starting_room)
    while queue.size() > 0:
        current_room, path = queue.dequeue()

        if current_room.id not in visited:
            visited.add(current_room.id)
            #check if it's the guy
            if current_room.id == target:
                return path

            for direction in current_room.get_exits():
                path_to_add= path + [direction]
                queue.enqueue((current_room.get_room_in_direction(direction), path_to_add))


def rooms_to_path(player, rooms):
    path=[]
    current_room = player.current_room
    for i in range(len(rooms)-1):
        possible_directions = {}
        for direction in current_room.get_exits():
            possible_directions[current_room.get_room_in_direction(direction).id] = direction
        if rooms[i+1] in possible_directions:
            path.append(possible_directions[rooms[i+1]])
            player.travel(possible_directions[rooms[i+1]])
            current_room = player.current_room
        else:
            bfs_result = bfs(player, rooms[i+1])
            for bfs_direction in bfs_result:
                player.travel(bfs_direction)
                current_room = player.current_room
            path = path + bfs_result
            # print(bfs_result)
    return path

test_directions = test_dft(player)
# print(test_directions)
# print(bfs(player, 17))
# print(rooms_to_path(player, test_directions))
# print(player.current_room.id)
traversal_path = rooms_to_path(player, test_directions)
# main_travel(len(room_graph))
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
