import pygame as pg
import prepare
import constants as c
import collider
import random as r
from enemies import ChasingEnemy
import prepare

WALL_LIST = [[0,0,32,32], [32,0,32,32], [64,0,32,32], [96,0,32,32],
             [128,0,32,32], [160,0,32,32], [192,0,32,32]]    
             
FLOOR_LIST = [[224,0,32,32], [256,0,32,32], [288,0,32,32], [320,0,32,32],
              [352,0,32,32], [384,0,32,32], [416,0,32,32], [448,0,32,32]]
             
class Wall(pg.sprite.DirtySprite):
    def __init__(self, topleft, size, *groups):
        super().__init__(*groups)
        self.spritesheet = prepare.WALLS
        self.random_wall = r.randint(0, 6)        
        self.image = self.get_images(size)
        self.rect = self.image.get_rect(topleft=topleft)
        self.mask = pg.mask.from_surface(self.image)
        self.dirty = 1

        
    def get_images(self, size):
        image = pg.Surface(size).convert_alpha()
        image.blit(self.spritesheet, (0,0), WALL_LIST[self.random_wall])
        return image
        
        
class Background(pg.sprite.DirtySprite):
    def __init__(self, topleft, size, *groups):
        super().__init__(*groups)
        self.spritesheet = prepare.WALLS
        self.image = self.get_images(size)
        self.rect = self.image.get_rect(topleft=topleft)
        self.dirty = 1

        
    def get_images(self, size):
        image = pg.Surface(size).convert()
        image.blit(self.spritesheet, (0,0), r.choice(FLOOR_LIST))
        return image
        

class Door(pg.sprite.DirtySprite):
    def __init__(self, room_number, direction, topleft, size, *groups):
        super().__init__(*groups)
        self.topleft = topleft
        self.size = size
        self.locked_color = c.RED
        self.unlocked_color = c.NAVY
        self.exit_to = room_number
        self.direction = direction
        self.rect = pg.Rect(self.topleft, self.size)
        self.image = pg.Surface(self.size)
        self.image.fill(self.locked_color)
        self.dirty = 1

    def unlock_door(self):
        self.door_locked_collider.kill()
        self.dirty = 1
        self.image.fill(self.unlocked_color)
        
    def make_door_locked_collider(self, group):
        self.door_locked_collider = collider.Collider(self.topleft, self.size, group)
        
        
class SetupRoom():
    def __init__(self, room_number, topleft, exits, room_size, wall_size):
        self.rect = pg.Rect(topleft, room_size)
        self.wall_size = wall_size        
        self.make_containers()
        self.make_background(wall_size)
        self.make_doors(exits)
        self.make_borders(wall_size)   
        #self.make_random_walls(wall_size)
        
    def make_background(self, wall_size):
        background_list = []
        for y in range(0, self.rect.h, wall_size[1]):
            for x in range(0, self.rect.w, wall_size[0]):
                background_list.append((x, y))
        for spot in background_list:
            Background(spot, wall_size, self.background_container)
                
        
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
            Door(room_num, exit_direction, door_spots[exit_direction],
                (w, h), self.door_container).make_door_locked_collider(self.wall_container)
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
        self.background_container = pg.sprite.Group()
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

    def make_all_sprites_container(self):
        self.all_sprites_container = pg.sprite.Group()    
        all_containers = [self.collider_container, self.door_container, 
                          self.wall_container, self.enemy_container,
                          self.pickup_container, self.bullet_container,  
                          self.teleporter_container, self.gun_container,
                          self.powerup_container, self.health_bar_container
                         ]
        self.all_sprites_container.add(all_containers)
        return self.all_sprites_container


class Room(SetupRoom):
    def __init__(self, room_number, topleft, exits, room_size, wall_size, game, player):
        super().__init__(room_number, topleft, exits, room_size, wall_size)
        self.game = game
        self.player = player
        self.teleporter = None
        self.pickups = None
        self.powerups = None

        self.enemies = ChasingEnemy(self.game, self.player, (500, 300), (32, 32),
                                    self.enemy_container)

        self.make_all_sprites_container()
        
    def update(self, dt):
        self.bullet_container.update()
        self.enemies.update(self, dt)
        
