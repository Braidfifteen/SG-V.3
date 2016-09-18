import pygame as pg
import prepare as p
import constants as c
import random
from gui import HealthBar
from math import sqrt

            
     
class Enemies(pg.sprite.DirtySprite):
    """Basic enemy class."""
    def __init__(self, sheet, game, player, pos, size, *groups):
        super().__init__(*groups)
        self.game = game
        self.frame = 54
        self.frames = self.get_frames(sheet, size)
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pg.mask.from_surface(self.image)
        self.player = player
        self.health_bar = None
        self.animate_timer = 0.0
        self.animate_fps = 50.0
        
    def get_frames(self, sheet, size):
        spritesheet = sheet
        indices = [[x, 0] for x in range(59)]
        return self.get_images(spritesheet, indices, size)
        
    def get_images(self, sheet, frame_indices, size):
        frames = []
        for cell in frame_indices:
            frame_rect = ((size[0]*cell[0], size[1]*cell[1]), size)
            frames.append(sheet.subsurface(frame_rect))
        return frames
    
    def next_image(self):
        now = pg.time.get_ticks()
        if now-self.animate_timer > 1000/self.animate_fps:
            self.frame = (self.frame+1)%len(self.frames)
            self.image = self.frames[self.frame]
            self.animate_timer = now
        
    def update(self, room, dt):
        self.next_image()
        self.check_if_alive(room, dt)

    def check_if_alive(self, room, dt):
        if self.health > 0:
            for health_bar in room.health_bar_container:
                health_bar.move_health_bar(dt)
            self.handle_bullet_hit(room)            
        else:
            self.kill()
            room.health_bar_container.update(self.health)

    def handle_bullet_hit(self, room):
        callback = pg.sprite.collide_mask    
        bullet_hit = pg.sprite.spritecollide(self, room.bullet_container, True, callback)
        for bullet in bullet_hit:
            self.player.gui.cross_hair.hit = True 
            self.health -= bullet.gun.output_damage
            bullet.kill()
            self.handle_health_bar(room)

            
    def handle_health_bar(self, room):
        if self.health > 0:
            self.health_bar = HealthBar(self, (self.health, 10), (self.rect.centerx,
                                        self.rect.center[1]-30), c.RED)
            self.health_bar.rect.centerx = self.rect.centerx
            self.health_bar.add_to_group(room.health_bar_container)
            self.game.all_sprites.add(self.health_bar)
            self.health_bar.update(self.health)
            

class ChasingEnemy(Enemies):
    def __init__(self, game, player, pos, size, *groups):
        self.spritesheet = p.CHASING_ENEMY
        super().__init__(self.spritesheet, game, player, pos, size, *groups)
        self.dirty = 2
        self.speed = 4
        self.health = 100
        self.damage = 10

        
        
    def find_player_location_vector(self):
        vx = self.player.rect.x - self.rect.x
        vy = self.player.rect.y - self.rect.y
        dist_from_player = sqrt(vx**2 + vy**2)
        vx /= dist_from_player
        vy /= dist_from_player
        if all([vx, vy]):
            vx /= sqrt(2)
            vy /= sqrt(2)
        return [vx, vy]

    def move_towards_player(self, vector):
        if self.alive():
            old_pos = self.rect.center
            self.rect.x += (vector[0] * self.speed)
            self.rect.y += (vector[1] * self.speed)
            if self.rect.center != old_pos:
                self.dirty = 1
        
    def update(self, room, dt):
        super().update(room, dt)

        #self.move_towards_player(self.find_player_location_vector())
        
        
        
        
        