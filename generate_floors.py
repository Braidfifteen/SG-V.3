import random

ROOM_EXIT_DICT = {
    "backrow": [("up", 2), ("left", 1), ("right", 1)],
    "backleftcorner": [("up", 2), ("right", 2)],
    "backrightcorner": [("up", 2), ("left", 2)],
    "middle": [("up", 3), ("left", 2), ("right", 2)],
    "rightside": [("up", 2), ("left", 2)],
    "leftside": [("up", 2), ("right", 2)],
    "toprow": [("right", 1), ("left", 1)],
    "topleftcorner": [("right", 2)],
    "toprightcorner": [("left", 2)]
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
    
    
class GenerateFloor():
    def __init__(self):
        self.floor_dict = {i: [] for i in range(50)}
        self.rooms_on_floor = [random.randint(0, 14)]
        self.create_floor()
        
    def get_info(self, room_no):
        """
        This method returns a dictionary which
        is used for finding rooms on floor and their exits.
        """
        info_dict = {
            "up": room_no + 5,
            "down": room_no - 5,
            "left": room_no - 1,
            "right": room_no + 1
            }
        return info_dict

    def get_rooms(self, room_no):
        direction_list = []
        for room_loc, room_nums in ROOM_LOCATION_DICT.items():
            if room_no in room_nums:
                for direction_choice in ROOM_EXIT_DICT[room_loc]:
                    direct, prob = direction_choice
                    for i in range(prob):
                        direction_list.append(direct)
        next_room = random.choice(direction_list)
        return self.get_info(room_no)[next_room]

    def get_exits(self, room_no):
        exit_list = []
        for direct, exit_room_no in self.get_info(room_no).items():
            if exit_room_no in self.rooms_on_floor:
                exit = (direct, exit_room_no)
                exit_list.append(exit)
        self.floor_dict[room_no] = exit_list

    def create_floor(self):
        count = 0
        while count <= random.randint(6, 14):
            next_room = self.get_rooms(self.rooms_on_floor[-1])
            if next_room not in self.rooms_on_floor:
                self.rooms_on_floor.append(next_room)
                count += 1
            else:
                random.shuffle(self.rooms_on_floor)
        for room in self.rooms_on_floor:
            self.get_exits(room)
            
test = GenerateFloor()
print(test.floor_dict)