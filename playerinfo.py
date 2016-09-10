import pygame as pg
import constants as c


class Player(pg.sprite.DirtySprite):
    def __init__(self, game, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert()
        self.image.fill((c.BLACK))
        self.rect = self.image.get_rect(center=pos)
        self.room = None
        self.game = game
        self.stats = PlayerStats()
        self.logic = PlayerLogic()
        self.velocity = [0, 0]

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in c.CONTROLS:
                direction = c.CONTROLS[event.key]
                self.velocity = c.DIRECT_DICT[direction]
        elif event.type == pg.KEYUP:
            self.velocity = [0, 0]
    
    def update(self, walls):
        self.move_player(walls)

    
    def move_player(self, walls):
        old_pos = self.rect.topleft
        move = self.velocity[0] * self.stats.speed, self.velocity[1] * self.stats.speed
        self.rect.move_ip(move)
        self.wall_hit_logic(move, walls)
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
            
class PlayerStats():
    def __init__(self):
        self.speed = 5
        self.health = 100
        self.damage = 5
        
class PlayerLogic():
    def __init(self):
        pass
        
    