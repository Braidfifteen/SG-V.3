import random




ROOM_EXIT_DICT = {
    "backrow": ["up", "left", "right"],
    "backleftcorner": ["up", "right"],
    "backrightcorner": ["up", "left"],
    "middle": ["up", "left", "down", "right"],
    "rightside": ["up", "left", "down"],
    "leftside": ["up", "right", "down"],
    "toprow": ["right", "left", "down"],
    "topleftcorner": ["right", "down"],
    "toprightcorner": ["left", "down"]
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
        self.floor_dict = {i: [] for i in range(20)}
        self.rooms_on_floor = []
        self.temp_room_dict = {}
        self.create_floor()
           
    def get_room_info(self, room_number):
        self.temp_room_dict.clear()
        for room_loc, room_nums in ROOM_LOCATION_DICT.items():
            if room_number in room_nums:
                self.temp_room_dict[room_number] = random.sample(ROOM_EXIT_DICT[room_loc],
                    random.randint(1, len(ROOM_EXIT_DICT[room_loc])))
                break
                
    def get_exit_rooms(self, room_number):
        exit_list = set()      
        exit_to_room_no = {
            "up": room_number + 5,
            "down": room_number - 5,
            "left": room_number - 1,
            "right": room_number + 1
            }        
        for exit_direction, exit_room_no in exit_to_room_no.items():
            if exit_room_no in self.rooms_on_floor:
                exit = (exit_direction, exit_room_no)
                exit_list.update([exit])
        for exits in self.temp_room_dict.values():
            for exit in exits:
                exit = (exit, exit_to_room_no[exit])
                exit_list.update([exit])
        self.floor_dict[room_number] = exit_list
        self.temp_room_dict[room_number] = exit_list
    
    def get_next_room_numbers(self, room_number):
        next_room_numbers = []
        for exits in self.temp_room_dict[room_number]:
            exit_directions, room_numbers = exits
            next_room_numbers.append(room_numbers)
        return next_room_numbers
                       
    def get_rooms(self, room_number):
        if room_number not in self.finished_rooms:
            self.rooms_on_floor.append(room_number)    
        self.finished_rooms.update([room_number]) 
        self.get_room_info(room_number)
        self.get_exit_rooms(room_number)
        for next_room_number in self.get_next_room_numbers(room_number):
            if next_room_number not in self.finished_rooms and \
                    next_room_number not in self.next_room:
                self.next_room.append(next_room_number)


    def create_floor(self):
        self.next_room = []
        self.finished_rooms = set()
        count = 0
        while count <= random.randint(6, 15):
            if len(self.next_room) <= 0:
                self.get_rooms(random.randint(0, 19))
                count += 1
            else:
                for room_number in self.next_room.copy():
                    self.get_rooms(room_number)
                    count += 1
                    
                    
                    
def test():
    room_number = 5
  
    count = 0
    room_list = []
    none_list = []
    room_list.append(room_number)
    next_room = 0
    boolean = False

    while count <= 10:
        exit_to_room_no = {
        "up": room_list[-1] + 5,
        "down": room_list[-1] - 5,
        "left": room_list[-1] - 1,
        "right": room_list[-1] + 1
        }  

        room_number = room_list[-1]

        for room_loc, room_nums in ROOM_LOCATION_DICT.items():
            if room_number in room_nums:
                next_room = random.choice(ROOM_EXIT_DICT[room_loc])
                next_room = (exit_to_room_no[next_room])
                print(room_list)
                print(room_number)
                print(next_room)
                if next_room not in room_list:
                    room_list.append(next_room)
                    count += 1


                else:
                


                
    test = set()
    for i in room_list:
        test.update([i])
        


    return test
            
            
                    
            
            
                    
                    
        
def get_room_no_list():

    while count <= 10:
        rn = room_list[-1]
        dir_list = [rn + 5, rn + 1, rn - 1, rn - 5]
        rn = random.choice(dir_list)
        if rn in in_list and rn not in room_list:
            print(rn)

            room_list.append(rn)
            count += 1
        else:
            print(rn)
            continue
        
    return room_list
        
print(test())