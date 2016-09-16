import pygame as pg
import prepare as p
import constants as c
from gui import HealthBar
from math import sqrt

            
     
class Enemies(pg.sprite.DirtySprite):
    """Basic enemy class."""
    def __init__(self, game, player, pos, size, *groups):
        super().__init__(*groups)
        self.game = game
        self.image = pg.Surface(size).convert()
        self.image.fill(c.SILVER)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.player = player
        self.health_bar = None

    def update(self, room, dt):
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
        bullet_hit = pg.sprite.spritecollide(self, room.bullet_container, True)
        for bullet in bullet_hit:
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
        super().__init__(game, player, pos, size, *groups)
        self.dirty = 1
        self.speed = 2
        self.health = 100
        self.damage = 10
        
    def find_player_location_vector(self):
        vx = self.player.rect.x - self.rect.x
        vy = self.player.rect.y - self.rect.y
        dist_from_player = sqrt(vx**2 + vy**2)
        vx = vx / dist_from_player
        vy = vy / dist_from_player
        return [vx, vy]

    def move_towards_player(self, vector):
        if self.alive():
            old_pos = self.rect.center
            self.rect.x += int(vector[0] * self.speed)
            self.rect.y += int(vector[1] * self.speed)
            if self.rect.center != old_pos:
                self.dirty = 1
        
    def update(self, room, dt):
        super().update(room, dt)
        self.move_towards_player(self.find_player_location_vector())
        
        
        
        
        