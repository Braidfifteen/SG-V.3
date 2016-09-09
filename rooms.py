import pygame as pg
import prepare
import constants as c


class Wall(pg.sprite.DirtySprite):
    image = pg.Surface(c.TILE_SIZE)
    image.fill(c.DARKRED)
    pg.draw.rect(image, c.FIREBRICK, ((0, 0), c.TILE_SIZE), 2)
    def __init__(self, topleft, size, *groups):
        super().__init__(*groups)
        self.rect = self.image.get_rect(topleft=topleft)
        self.dirty = 1
        
        
class Door(pg.sprite.DirtySprite):
    def __init__(self, room_number, direction, topleft, size, *groups):
        super().__init__(*groups)
        self.exit_to = room_number
        self.direction = direction
        self.rect = pg.Rect(topleft, size)
        self.image = pg.Surface(size)
        self.image.fill(c.PURPLE)
        self.dirty = 1
        
        
class Room():
    def __init__(self, room_number, topleft, exits, room_size, wall_size):
        self.rect = pg.Rect(topleft, room_size)
        self.wall_size = wall_size
        self.doors = pg.sprite.Group()
        self.make_doors(exits)
        door_toplefts = [door.rect.topleft for door in self.doors]
        self.walls = pg.sprite.Group()
        self.make_walls(wall_size, door_toplefts)
        
    def make_walls(self, wall_size, door_toplefts):
        wall_spots = [(x, y)
                            for x in range(0, self.rect.w, wall_size[0])
                            for y in (0, self.rect.h - wall_size[1])]
        vert_spots = [(x, y)
                            for x in (0, self.rect.w - wall_size[0])
                            for y in range(wall_size[1], self.rect.h, wall_size[1])]
        wall_spots.extend(vert_spots)
        for spot in wall_spots:
            if spot not in door_toplefts:
                Wall(spot, wall_size, self.walls)
                
    def make_doors(self, exits):
        w, h = self.wall_size
        cells_wide = self.rect.w // w
        cells_high = self.rect.h // h
        door_spots = {
            "left": (self.rect.left, (cells_high // 2) * h),
            "right": (self.rect.right - w, (cells_high // 2) * h),
            "up": ((cells_wide // 2) * w, self.rect.top),
            "down": ((cells_wide // 2) * w, self.rect.bottom - h)}
        for exit_direction, room_num in exits:
            Door(room_num, exit_direction, door_spots[exit_direction], (w, h), self.doors)