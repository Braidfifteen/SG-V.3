import pygame as pg
import constants as c
from guns import Gun
from gui import HealthBar, DrawText
import math

def divfmod(x, y):
    fmod = math.fmod(x, y)
    div = (x-fmod)//y
    return div, fmod

        
class Player(pg.sprite.DirtySprite):
    def __init__(self, game, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((size)).convert_alpha()
        self.image.fill(c.YELLOW)        
        self.rect = self.image.get_rect(center=pos)
        self.mask = self.make_mask()
        self.game = game

        #self.room = 
        self.stats = PlayerStats(self)          
        self.gun = Gun(self)        
        self.all_sprites_container = pg.sprite.Group()
        self.all_sprites_container.add(self)
        self.gui = PlayerGui(self)
        self.logic = PlayerLogic(self)
        self.is_dead = False
    
        
    def make_mask(self):
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill((0, 0, 0, 0))
        mask_surface.fill(c.WHITE, (0, 0, 16, 16))
        mask = pg.mask.from_surface(mask_surface)
        return mask
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.logic.add_direction(event.key)
            self.logic.reload_gun(event.key)
        elif event.type == pg.KEYUP:
            self.logic.pop_direction(event.key)
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
        self.old_direction = None
        self.direction_stack = []
        self.direction = pg.K_RIGHT
        self.remainder = [0, 0]
    
    def add_direction(self, key):
        if key in c.CONTROLS:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            self.direction_stack.append(key)
            self.direction = self.direction_stack[-1]
            
    def pop_direction(self, key):
        if key in c.CONTROLS:
            if key in self.direction_stack:
                self.direction_stack.remove(key)
            if self.direction_stack:
                self.direction = self.direction_stack[-1]
        
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
    
    def reload_gun(self, key):
        if key == pg.K_r:
            if self.gun.clip < self.gun.clip_size and self.gun.ammo_held > 0:
                ammo_for_full_clip = self.gun.clip_size - self.gun.clip
                if ammo_for_full_clip <= self.gun.ammo_held:
                    self.gun.clip += ammo_for_full_clip
                    self.gun.ammo_held -= ammo_for_full_clip
                elif ammo_for_full_clip > self.gun.ammo_held:
                    self.gun.clip += self.gun.ammo_held
                    self.gun.ammo_held = 0
                    
    def movement(self, walls, offset, i):
        self.player.rect[i] += offset
        collisions = pg.sprite.spritecollide(self.player, walls, False)
        callback = pg.sprite.collide_mask
        while pg.sprite.spritecollideany(self.player, collisions, callback):
            self.player.rect[i] += (1 if offset<0 else -1)
            self.remainder[i] = 0

            
            
    def update(self, keys, walls, enemies, dt):
        #self.move_player(keys, walls, enemies)
        vector = [0, 0]
        for key in self.direction_stack:
            vector[0] += c.CONTROLS[key][0]
            vector[1] += c.CONTROLS[key][1]
            if all(vector):
                vector[0] /= math.sqrt(2)
                vector[1] /= math.sqrt(2)
        self.remainder[0] += vector[0]*self.stats.speed
        self.remainder[1] += vector[1]*self.stats.speed
        vector[0], self.remainder[0] = divfmod(self.remainder[0], 1)
        vector[1], self.remainder[1] = divfmod(self.remainder[1], 1)
        if vector != [0, 0]:
            old_pos = self.player.rect.center
            self.movement(walls, vector[0], 0)
            self.movement(walls, vector[1], 1)
            if self.player.rect.center != old_pos:
                self.player.dirty = 1
            
            




        