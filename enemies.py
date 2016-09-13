import pygame as pg
import prepare as p
import constants as c
from gui import HealthBar

            

        
class Enemies(pg.sprite.DirtySprite):
    """Basic enemy class."""
    def __init__(self, game, player, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert()
        self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.player = player
        self.game = game
        self.health = 100
        self.damage = 10
        self.dirty = 1
        self.health_bar = HealthBar(self, (self.health, 15), (self.rect.center[0]-10,
                          self.rect.center[1]-10), self.game.all_sprites)
        self.dead = False
        
    def update(self, room):
        self.health_bar.update(self.health, self.dead)       
        if self.dead == False:

            bullet_hit = pg.sprite.spritecollide(self, room.bullet_container, True)
            for bullet in bullet_hit:
                self.health -= bullet.gun.damage
                bullet.kill()
            if self.health <= 0:
                self.kill()
                self.dead = True
        
        
        
    
        