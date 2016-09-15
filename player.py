import pygame as pg
import constants as c
from guns import Gun
from gui import HealthBar, DrawText

        
class Player(pg.sprite.DirtySprite):
    def __init__(self, game, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert()
        self.image.fill((c.BLACK))
        self.rect = self.image.get_rect(center=pos)
        self.room = None
        self.game = game
        self.stats = PlayerStats(self)  
        self.all_sprites_container = pg.sprite.Group()
        self.all_sprites_container.add(self)
        self.gui = PlayerGui(self)
        self.logic = PlayerLogic()
        self.velocity = [0, 0]
        self.gun = Gun(self)
        self.is_dead = False


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in c.CONTROLS:
                direction = c.CONTROLS[event.key]
                self.velocity = c.DIRECT_DICT[direction]
        if event.type == pg.KEYUP:
            self.velocity = [0, 0]
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.gun.is_shooting = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.gun.is_shooting = False
    
    def update(self, walls, dt):      
        self.check_if_dead()
        self.move_player(walls)
        self.gun.update(dt)
        self.gui.update()
   
    def move_player(self, walls):
        old_pos = self.rect.topleft
        move = self.velocity[0] * self.stats.speed, self.velocity[1] * self.stats.speed
        self.rect.move_ip(move)
        self.wall_hit_logic(move, walls)
        if self.rect.topleft != old_pos:
            self.dirty = 1    
           
    def check_if_dead(self):
        if self.stats.health <= 0:
            self.kill()
            self.is_dead = True    
            
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
            
    def ammo_pickup(self, amount):
        if amount + self.gun.ammo <= self.gun.ammo_capacity:
            self.gun.ammo += amount
        else:
            self.gun.ammo = self.gun.ammo_capacity
            
    def health_pickup(self, amount):
        if amount + self.stats.health <= self.stats.health_capacity:
            self.stats.health += amount
        else:
            self.stats.health = self.stats.health_capacity
        
        
class PlayerGui():
    def __init__(self, player):
        self.player = player
        self.ammo_counter = DrawText(self.player, (self.player.game.screen_rect.midtop),
                                     self.player.all_sprites_container)
        self.health_bar = HealthBar(self, (self.player.stats.health, 25), (50, 50),
                                    c.BLUE, self.player.all_sprites_container)
        
    def update(self):
        self.health_bar.update(self.player.stats.health)   
        self.ammo_counter.update(str(self.player.gun.ammo))
        
            
class PlayerStats():
    def __init__(self, player):
        self.player = player
        self.health = 100
        self.health_capacity = 100
        self.speed = 5
        self.damage_multiplier = 1.5
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
        

        