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
        self.health_bar = HealthBar(self, (self.health, 15), (self.rect.center[0]-50,
                          self.rect.center[1]-30))
        self.dead = False
        self.health_timer_on = False
        self.health_timer = 0    

        
    def update(self, room, dt):

        if not self.dead:       
            self.health_timer_start(dt)
            bullet_hit = pg.sprite.spritecollide(self, room.bullet_container, True)
            for bullet in bullet_hit:
                self.health_timer = 0
                self.health_timer_on = True
                self.game.all_sprites.add(self.health_bar)
                self.health_bar.update(self.health, self.dead)      
                self.health -= bullet.gun.damage
                bullet.kill()
            if self.health <= 0:
                self.kill()
                self.dead = True
                self.health_bar.kill()

    def health_timer_start(self, dt):
        if self.health_timer_on == True:
            self.health_timer += dt
            if self.health_timer >= 1000:
                self.health_bar.remove(self.game.all_sprites)
                self.health_timer_on = False
                self.health_timer = 0

            
