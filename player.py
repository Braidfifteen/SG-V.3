import pygame as pg
import constants as c
from guns import Gun
from gui import HealthBar, DrawText
from math import sqrt

        
class Player(pg.sprite.DirtySprite):
    def __init__(self, game, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert()
        self.image.fill((c.BLACK))
        self.rect = self.image.get_rect(center=pos)
        self.game = game
        #self.room = 
        self.stats = PlayerStats(self)          
        self.gun = Gun(self)        
        self.all_sprites_container = pg.sprite.Group()
        self.all_sprites_container.add(self)
        self.gui = PlayerGui(self)
        self.logic = PlayerLogic(self)
        self.is_dead = False

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.logic.reload_gun()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.gun.is_shooting = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.gun.is_shooting = False
    
    def update(self, keys, walls, enemies, dt):      
        self.check_if_dead()
        self.logic.update(keys, walls, enemies, dt)
        self.gun.update(dt)
        self.gui.update()
   
    def check_if_dead(self):
        if self.stats.health <= 0:
            self.kill()
            self.is_dead = True    
            
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
        self.ammo_counter.update(str(self.player.gun.clip)
                                 + "/" + str(self.player.gun.ammo_held))
        

class PlayerStats():
    def __init__(self, player):
        self.player = player
        #self.room = self.player.room
        self.health = 100
        self.health_capacity = 100
        self.speed = 5
        self.damage_multiplier = 1.5
        self.luck = 0
        
    def speed_info(self):
        pass
        
    def damage_info(self):
        pass
        
        
class PlayerLogic():
    def __init__(self, player):
        self.player = player
        self.stats = self.player.stats
        self.gun = self.player.gun
        #self.room = self.player.game.room
        self.setup_health_logic()

        
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
            
    def setup_health_logic(self):
        self.health_timer = 401
        self.health_down_speed = 400
        
    def move_player(self, keys, walls, enemies):
        old_pos = self.player.rect.topleft
        self.velocity = [0, 0]
        for key in c.CONTROLS:
            if keys[key]:
                self.velocity[0] += c.CONTROLS[key][0]
                self.velocity[1] += c.CONTROLS[key][1]
                if all(self.velocity):
                    self.velocity[0] /= sqrt(2)
                    self.velocity[1] /= sqrt(2) 
        self.player.rect.x += (self.velocity[0] * self.stats.speed)
        self.handle_wall_collision(self.velocity, walls)  
        self.handle_enemy_collision(self.velocity, enemies)        
        self.player.rect.y += (self.velocity[1] * self.stats.speed)
        self.handle_wall_collision(self.velocity, walls)     
        self.handle_enemy_collision(self.velocity, enemies)        
        if self.player.rect.topleft != old_pos:
            self.player.dirty = 1    
            
    def handle_enemy_collision(self, direction, enemies):
        enemy_hit_list = pg.sprite.spritecollide(self.player, enemies, False)
        for enemy in enemy_hit_list:
            if direction[0] > 0:
                self.player.rect.right = enemy.rect.left
            elif direction[0] < 0:
                self.player.rect.left = enemy.rect.right
            elif direction[1] > 0:
                self.player.rect.bottom = enemy.rect.top
            elif direction[1] < 0:
                self.player.rect.top = enemy.rect.bottom
            if self.health_timer > self.health_down_speed:
                self.stats.health -= enemy.damage
                #self.health_timer = 0
                
    def handle_wall_collision(self, direction, walls):
        wall_hit_list = pg.sprite.spritecollide(self.player, walls, False)
        for wall in wall_hit_list:
            if direction[0] > 0:
                self.player.rect.right = wall.rect.left
            elif direction[0] < 0:
                self.player.rect.left = wall.rect.right
            elif direction[1] > 0:
                self.player.rect.bottom = wall.rect.top
            elif direction[1] < 0:
                self.player.rect.top = wall.rect.bottom
            break
    
    def reload_gun(self):
        if self.gun.clip < self.gun.clip_size and self.gun.ammo_held > 0:
            ammo_for_full_clip = self.gun.clip_size - self.gun.clip
            if ammo_for_full_clip <= self.gun.ammo_held:
                self.gun.clip += ammo_for_full_clip
                self.gun.ammo_held -= ammo_for_full_clip
            elif ammo_for_full_clip > self.gun.ammo_held:
                self.gun.clip += self.gun.ammo_held
                self.gun.ammo_held = 0
            
            
            
    def update(self,keys, walls, enemies, dt):
        self.move_player(keys, walls, enemies)


        