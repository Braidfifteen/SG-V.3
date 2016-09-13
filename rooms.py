import pygame as pg
import prepare
import constants as c
import collider
import random as r


class Wall(pg.sprite.DirtySprite):
    image = pg.Surface(c.TILE_SIZE)
    image.fill(c.DARKRED)
    pg.draw.rect(image, c.TEAL, ((0, 0), c.TILE_SIZE), 2)
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
        self.make_containers()
        self.make_doors(exits)
        self.make_borders(wall_size)
        #self.make_random_walls(wall_size)
        self.room_assets = None
        
    def make_borders(self, wall_size):
        door_toplefts = [door.rect.topleft for door in self.door_container]        
        border_spots = [(x, y)
                            for x in range(0, self.rect.w, wall_size[0])
                            for y in (0, self.rect.h - wall_size[1])]                
        vert_border_spots = [(x, y)
                            for x in (0, self.rect.w - wall_size[0])
                            for y in range(wall_size[1], self.rect.h, wall_size[1])]                        
        border_spots.extend(vert_border_spots)
        for spot in border_spots:
            if spot not in door_toplefts:
                Wall(spot, wall_size, self.wall_container)
                
    def make_random_walls(self, wall_size):

        self.inner_wall_rect = pg.Rect((self.rect.x+(wall_size[0]*3),
                                       self.rect.y+(wall_size[1]*3)),
                                       (self.rect.w-(wall_size[0]*3),
                                       self.rect.h-(wall_size[1]*3)))
        for i in range(r.randint(1, 10)):
            wall_list = [(x, y)
                            for x in range(r.randrange(self.inner_wall_rect.x),
                                           r.randrange(self.inner_wall_rect.w), wall_size[0])
                            for y in range(r.randrange(self.inner_wall_rect.y),
                                           r.randrange(self.inner_wall_rect.h), wall_size[1])]
                                                      
        for spot in wall_list:
            wall = Wall(spot, wall_size, self.wall_container)           
            check_if_blocks_door = pg.sprite.spritecollide(wall, self.collider_container, False)
            for i in check_if_blocks_door:
                wall.kill()
            
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
            Door(room_num, exit_direction, door_spots[exit_direction], (w, h), self.door_container)
            self.make_colliders(exit_direction, door_spots[exit_direction], (w, h))
 
    def make_colliders(self, direction, door_spot, size):
        """
        Makes invisible sprites in front of doors so that
        walls can't spawn in front of them.
        """
        collider_dict = {
            "left": ((door_spot[0] + size[0]), door_spot[1]),
            "right": ((door_spot[0] - size[0]), door_spot[1]),
            "up": (door_spot[0], (door_spot[1] + size[1])),
            "down": (door_spot[0], (door_spot[1] - size[1]))
            }
        collider.Collider(collider_dict[direction], size, self.collider_container)
               
    def make_containers(self):
        self.collider_container = pg.sprite.Group()
        self.door_container = pg.sprite.Group()
        self.wall_container = pg.sprite.Group()
        self.enemy_container = pg.sprite.Group()
        self.pickup_container = pg.sprite.Group()
        self.bullet_container = pg.sprite.Group()
        self.teleporter_container = pg.sprite.Group()
        self.gun_container = pg.sprite.Group()
        self.powerup_container = pg.sprite.Group()
        self.health_bar_container = pg.sprite.Group()
    
    def update(self, dt):
        for bullet in self.bullet_container:
            bullet.update()
        
class RoomAssets():
    def __init__(self, room):
        self.room = room
        self.teleporter = None
        self.pickups = None
        self.powerups = None
        self.guns = None
        self.enemies = None
        