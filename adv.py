from room import Room
from player import Player
from world import World
import os
dirpath = os.path.dirname(os.path.abspath(__file__))

import random
from ast import literal_eval

###Understand
# Write an algorithm that picks a random unexplored direction from the player's current room, 
# travels and logs that direction, 
# then loops, maybe try recurssion here?
# This should cause your player to walk a DFT. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.
###Plan 
# step 1 - record a traversal path, and the paths I've already taken
# step 2 - Need to get the current room I am in, including the exits
# Step 3 - traverse, starting at current room
# Step 4 - go to each room, record it as visited, then bakctrack somehow? Reverse direction?
# Step 5 - function should keep running until all rooms have been visited



# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = dirpath + "maps/test_line.txt"
# map_file = dirpath + "maps/test_cross.txt"
# map_file = dirpath + "maps/test_loop.txt"
# map_file = dirpath + "maps/test_loop_fork.txt"
map_file = dirpath + "/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


traversal_path = []
opposite_dir = {'n':'s','e':'w','s':'n','w':'e'}

def map_traversal(starting_room, visited=set()):
    # step 1 - record a traversal path, and the paths I've already taken
    path_taken = []

    for direction in player.current_room.get_exits(): 
        # step 2 - Need to get the current room I am in, including the exits and then do something for each direction

        
        player.travel(direction) 
        # Step 3 - traverse, starting at current room


        if player.current_room.id not in visited: 
            #if the room has not been visited we enter the loop 

            # Step 4 - go to each room, record it as visited, then bakctrack somehow? Reverse direction?

            visited.add(player.current_room.id)
            #mark the room as visited 

            path_taken.append(direction)
            #add new direction to path taken 

            path_taken = path_taken + map_traversal(player.current_room.id, visited)
            #this is where the recursion is happening now that path taken has been added, we are able to run function from new current room

            player.travel(opposite_dir[direction])
            #backtracking to go to different room

            path_taken.append(opposite_dir[direction])
            #adding back track to path taken to make sure it's accounted for

        else: 
            # Step 5 - function should keep running until all rooms have been visited 

            player.travel(opposite_dir[direction]) # the room is already visited so we must backtrack and go to a different room


    return path_taken

traversal_path = map_traversal(player.current_room.id)




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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
