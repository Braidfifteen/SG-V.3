import pygame as pg
import math
import constants as c
import random


class Bullet(pg.sprite.DirtySprite):
    def __init__(self, gun, start_x, start_y, dest_x, dest_y, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(gun.bullet_size).convert()
        self.image.fill(c.DARKVIOLET)
        self.rect = self.image.get_rect()
        self.gun = gun
        self.start_x = start_x
        self.start_y = start_y
        self.rect.x = start_x
        self.rect.y = start_y
        self.floating_point_x = start_x
        self.floating_point_y = start_y
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        self.velocity = self.gun.bullet_velocity
        self.moveX = math.cos(angle) * self.velocity
        self.moveY = math.sin(angle) * self.velocity
        self.distance_from_start = None
        
    def update(self):
        old_pos = self.rect.topleft
        #self.moveX *= 0.98
        #self.moveY *= 0.98
        self.floating_point_x += self.moveX
        self.floating_point_y += self.moveY
        self.rect.x = int(self.floating_point_x)
        self.rect.y = int(self.floating_point_y)
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
        self.damage = 6
        self.fire_rate = 300
        self.ammo = 500000
        self.ammo_capacity = 50
        self.range = 200
        self.is_shooting = False
        self.fire_rate_timer = self.fire_rate
        self.bullet_velocity = 5
        self.automatic = True
        self.reload_timer = 0
        self.reload_time = 0
        self.bullet_size = (3, 3)
        
    def update(self, dt):
        self.check_if_shooting(dt)

    def check_if_shooting(self, dt):
        if self.automatic:
            self.fire_rate_timer += dt
            if self.is_shooting and self.fire_rate_timer >= self.fire_rate and \
                    self.ammo > 0:
                self.find_mouse_pos_and_shoot()
                self.fire_rate_timer = 0                  
        else:
            if self.is_shooting:
                self.find_mouse_pos_and_shoot()
                self.is_shooting = False

    def find_mouse_pos_and_shoot(self):
            pos = pg.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            bullet = Bullet(self, self.player.rect.center[0], self.player.rect.center[1],
                            mouse_x, mouse_y, self.player.game.room.bullet_container,
                            self.player.game.all_sprites)        
            self.ammo -= 1



            
            
            
            
            
            
            
            
            
            
            
            