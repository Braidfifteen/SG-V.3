import pygame as pg
import math
import constants as c
import random
import vectormath as v
import prepare

class Bullet(pg.sprite.DirtySprite):
    def __init__(self, gun, start_x, start_y, dest_x, dest_y, *groups):
        super().__init__(*groups)
        self.baseimage = prepare.BULLETS.subsurface(64, 0, 32, 32)

        
        self.gun = gun
        self.start_x = start_x
        self.start_y = start_y

        self.floating_point_x = start_x
        self.floating_point_y = start_y
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        norm_dest = v.normalize((x_diff, y_diff))
        new_angle = 180*v.angle(norm_dest, [0,1])/math.pi
        if norm_dest[0] < 0:
            new_angle *= -1
        
        self.angle = math.atan2(y_diff, x_diff)
   
        
        


        self.rect = self.baseimage.get_rect()
        self.rect.center = (start_x, start_y)   
        self.loc = self.rect.center


        
        #self.image_angle = 360-math.atan2(y_diff, x_diff)*180/math.pi
        
        degs = math.degrees(self.angle)%360
        self.velocity = self.gun.bullet_velocity
        arc = self.velocity * 0.05
        self.moveX = math.cos(self.angle) * self.velocity #+ random.random()*2*arc -arc
        self.moveY = math.sin(self.angle) * self.velocity #+ random.random()*2*arc -arc
        self.distance_from_start = None
        
        #Use -degs in transform if base image has == w and h. Otherwise use new_angle.
        self.image = pg.transform.rotate(self.baseimage, -degs).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        
        self.mask = pg.mask.from_surface(self.image)        

    def update(self):


        
        old_pos = self.rect.topleft
        #self.moveX *= 0.98
        #self.moveY *= 0.98

        self.floating_point_x += self.moveX
        self.floating_point_y += self.moveY
        self.rect.center = (int(self.floating_point_x), int(self.floating_point_y))
        if self.rect.topleft != old_pos:
            self.dirty = 1
        self.calculate_bullet_range(self.rect.x, self.rect.y)
        if self.rect.x < 0 or self.rect.x > c.SCREEN_SIZE[0] or self.rect.y < 0 or \
            self.rect.y > c.SCREEN_SIZE[1]:
            self.kill()
            
    def calculate_bullet_range(self, current_x, current_y):
        x_diff = current_x - self.start_x
        y_diff = current_y - self.start_y
        dist_from_start = math.sqrt(x_diff**2 + y_diff**2)
        if dist_from_start >= self.gun.range:       
            self.kill()
        
class Gun():
    def __init__(self, player):
        self.player = player
        self.base_damage = 6
        self.output_damage = int(self.base_damage * self.player.stats.damage_multiplier)
        self.fire_rate = 300
        self.max_ammo_capacity = 500
        self.ammo_held = 100
        self.clip_size = 30000
        self.clip = self.clip_size
        self.range = 300
        self.is_shooting = False
        self.fire_rate_timer = self.fire_rate
        self.bullet_velocity = 20
        self.automatic = True
        self.reload_timer = 0
        self.reload_time = 0
        self.bullets_per_shot = 1
        self.bullet_size = [5, 20]
        
    def update(self, dt):
        self.check_if_shooting(dt)

    def check_if_shooting(self, dt):
        if self.automatic:
            self.fire_rate_timer += dt
            if self.is_shooting and self.fire_rate_timer >= self.fire_rate and \
                    self.clip > 0:
                self.find_mouse_pos_and_shoot()
                self.fire_rate_timer = 0                  
        else:
            if self.is_shooting and self.clip > 0:
                self.find_mouse_pos_and_shoot()
                self.is_shooting = False

    def find_mouse_pos_and_shoot(self):
            pos = pg.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            bullet = Bullet(self, self.player.rect.center[0], self.player.rect.center[1],
                            mouse_x, mouse_y, self.player.game.room.bullet_container,
                            self.player.game.all_sprites)        
            self.clip -= self.bullets_per_shot



            
            
            
            
            
            
            
            
            
            
            
            