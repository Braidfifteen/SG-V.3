import pygame as pg
import prepare as p

DIRECT_DICT = {"UP": (0, -1),
               "RIGHT": (1, 0),
               "DOWN": (0, 1),
               "LEFT": (-1, 0)}
               
CONTROLS = {pg.K_w: "UP", 
            pg.K_d: "RIGHT",
            pg.K_s: "DOWN",
            pg.K_a: "LEFT"
           }
            
            
class Sprite(pg.sprite.DirtySprite):
    """Basic sprite class for all actors."""
    def __init__(self, pos, size, color, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = [0, 0]
        self.speed = 5

class Player(Sprite):
    """Class that represents user controlled sprite."""
    def __init__(self, game, pos, size, color, *groups):
        super().__init__(pos, size, color, *groups)
        self.game = game
        self.room = None
        self.attributes = None
        self.logic = None
        
    def get_event(self, event):
        """Gets events from game and passes them to Player."""
        if event.type == pg.KEYDOWN:
            if event.key in CONTROLS:
                direction = CONTROLS[event.key]
                self.velocity = DIRECT_DICT[direction]
        elif event.type == pg.KEYUP:
            self.velocity = [0, 0]
            
        
    def update(self, room):
        """Update image and position of sprite."""
        old_pos = self.rect.topleft
        move = self.velocity[0] * self.speed, self.velocity[1] * self.speed
        self.rect.move_ip(move)
        self.wall_hit_logic(move, room.walls)
        if self.rect.topleft != old_pos:
            self.dirty = 1
        
    def wall_hit_logic(self, move, walls):
        wall_hit_list = pg.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            if move[0] > 0:
                self.rect.right = wall.rect.left
            elif move[0] < 0:
                self.rect.left = wall.rect.right
            elif move[1] > 0:
                self.rect.bottom = wall.rect.top
            elif move[1] < 0:
                self.rect.top = wall.rect.bottom
            break
                
        
class Enemies(Sprite):
    """Basic enemy class."""
    def __init__(self, player, pos, size, color, *groups):
        super().__init__(pos, size, color, *groups)
        self.player = player
        self.attributes = None
        
    def update(self):
        pass
        
        
    
        