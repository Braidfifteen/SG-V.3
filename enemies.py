import pygame as pg
import prepare as p
import constants as c
from gui import HealthBar

            
     
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
        self.health = 100
        self.damage = 10
        self.dirty = 2
        
        self.health_bar = None
        
    def update(self, room, dt):

        if self.health > 0:
            for i in room.health_bar_container:
                i.move_health_bar(dt)
            bullet_hit = pg.sprite.spritecollide(self, room.bullet_container, True)
            for bullet in bullet_hit:
                self.health -= bullet.gun.damage
                if self.health > 0:
                    self.health_bar = HealthBar(self, (self.health, 10), (self.rect.centerx,
                      self.rect.center[1]-30), c.RED) 
                    self.health_bar.rect.centerx = self.rect.centerx
                    self.health_timer_on = True
                    self.health_bar.add_to_group(room.health_bar_container)
                    self.game.all_sprites.add(self.health_bar)
                    self.health_bar.update(self.health)
                    bullet.kill()
        else:
            self.kill()
            room.health_bar_container.update(self.health)
        
