import pygame as pg
import math
import constants as c


class Bullet(pg.sprite.DirtySprite):
    def __init__(self, gun, start_x, start_y, dest_x, dest_y, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((3, 3)).convert()
        self.image.fill(c.DARKVIOLET)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.floating_point_x = start_x
        self.floating_point_y = start_y
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)
        velocity = 2.5
        self.moveX = math.cos(angle) * velocity
        self.moveY = math.sin(angle) * velocity
        self.gun = gun
        
    def update(self):
        old_pos = self.rect.topleft
        self.floating_point_x += self.moveX
        self.floating_point_y += self.moveY
        self.rect.x = int(self.floating_point_x)
        self.rect.y = int(self.floating_point_y)
        if self.rect.topleft != old_pos:
            self.dirty = 1
        if self.rect.x < 0 or self.rect.x > c.SCREEN_SIZE[0] or self.rect.y < 0 or \
            self.rect.y > c.SCREEN_SIZE[1]:
            self.kill()
            
    def calculate_bullet_range(self):
        pass
        
            
class Gun():
    def __init__(self, player):
        self.player = player
        self.damage = 6
        self.fire_rate = 400
        self.ammo = 50
        self.ammo_capacity = 50
        self.range = 700
        self.is_shooting = False
        self.fire_rate_timer = 0
        
    def update(self, dt):
        self.fire_rate_timer += dt
        if self.is_shooting and self.fire_rate_timer >= self.fire_rate and \
                self.ammo > 0:
            pos = pg.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            bullet = Bullet(self, self.player.rect.center[0], self.player.rect.center[1],
                            mouse_x, mouse_y, self.player.game.room.bullet_container,
                            self.player.game.all_sprites)
            self.ammo -= 1
            self.fire_rate_timer = 0
            
            
        