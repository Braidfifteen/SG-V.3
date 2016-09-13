import pygame as pg
import constants as c
from guns import Gun
from gui import HealthBar

        
class Player(pg.sprite.DirtySprite):
    def __init__(self, game, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert()
        self.image.fill((c.BLACK))
        self.rect = self.image.get_rect(center=pos)
        self.room = None
        self.game = game
        self.stats = PlayerStats(self)        
        self.health_bar = HealthBar(self, (self.stats.health, 25), (50, 50),
                                    c.BLUE, self.game.all_sprites)
        self.logic = PlayerLogic()
        self.velocity = [0, 0]
        self.gun = Gun(self)
        self.dead = False

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in c.CONTROLS:
                direction = c.CONTROLS[event.key]
                self.velocity = c.DIRECT_DICT[direction]
            elif event.key == pg.K_t:
                self.stats.health -= 10
        if event.type == pg.KEYUP:
            self.velocity = [0, 0]
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.gun.is_shooting = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.gun.is_shooting = False
    
    def update(self, walls, dt):
        self.health_bar.update(self.stats.health, self.dead)        
        if self.stats.health <= 0:
            self.kill()
            self.dead = True
        self.move_player(walls)
        self.gun.update(dt)
   
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
    def __init__(self, player):
        self.player = player
        self.health = 100
        self.speed = 5
        self.damage_multiplier = 0
        self.luck = 0
        self.health_info()
        
    def health_info(self):
        self.health_timer = 0
        self.health_cooldown = 400
        
    def speed_info(self):
        pass
        
    def damage_info(self):
        pass
        
        
        
class PlayerLogic():
    def __init(self):
        pass
        

        