import random




ROOM_EXIT_DICT = {
    "backrow": [("up", 2), ("left", 1), ("right", 1)],
    "backleftcorner": [("up", 2), ("right", 2)],
    "backrightcorner": [("up", 2), ("left", 2)],
    "middle": [("up", 3), ("left", 2), ("right", 2)], #("down", 1), ("right", 1)],
    "rightside": [("up", 2), ("left", 2)], #("down", 1)],
    "leftside": [("up", 2), ("right", 2)], #("down", 1)],
    "toprow": [("right", 1), ("left", 1)], #("down", 2)],
    "topleftcorner": [("right", 2)], #("down", 1)],
    "toprightcorner": [("left", 2)] #("down", 1)]
    }
    
ROOM_LOCATION_DICT = {
    "backrow": [1, 2, 3],
    "backleftcorner": [0],
    "backrightcorner": [4],
    "middle": [6, 7, 8, 11, 12, 13, 16, 17,
               18, 21, 22, 23, 26, 27, 28,
               31, 32, 33, 36, 37, 38, 41,
               42, 43],
    "rightside": [9, 14, 19, 24, 29, 34, 39, 44],
    "leftside": [10, 5, 15, 20, 25, 30, 35, 40],
    "toprow": [46, 47, 48],
    "toprightcorner": [49],
    "topleftcorner": [45]
    }
    
  
room_number = random.randint(0, 9)


room_list = []
floor_dict = {i: [] for i in range(50)}

room_list.append(room_number)
next_room = 0    
test_list = set()
    


                    
def test():
    count = 0
    while count <= 10:
        exit_to_room_no = {
        "up": room_list[-1] + 5,
        "down": room_list[-1] - 5,
        "left": room_list[-1] - 1,
        "right": room_list[-1] + 1
        }  

        room_number = room_list[-1]
        
        direction_list = []
        for room_loc, room_nums in ROOM_LOCATION_DICT.items():
            if room_number in room_nums:
                for i in ROOM_EXIT_DICT[room_loc]:
                    direct, prob = i
                    for h in range(prob):
                        direction_list.append(direct)
        next_room = random.choice(direction_list)

        next_room = (exit_to_room_no[next_room])

        if next_room not in room_list:
            room_list.append(next_room)
            count += 1
        else:
            random.shuffle(room_list)

        


        for i in room_list:
            test_list.update([i])
        for i in test_list:
            get_exit(i)



    return floor_dict

def get_exit(room_no):
    exit_list = []
    exit_to_room_no = {
    "up": room_no + 5,
    "down": room_no - 5,
    "left": room_no - 1,
    "right": room_no + 1
    }
    for direct, exit_room_no in exit_to_room_no.items():
        if exit_room_no in test_list:
            exit = (direct, exit_room_no)
            exit_list.append(exit)    
    floor_dict[room_no] = exit_list
        
print(test())