import pygame as pg
import constants as c

class HealthBar(pg.sprite.DirtySprite):
    def __init__(self, actor, size, pos, color, *groups):
        super().__init__(*groups)
        self.size = size
        self.image = pg.Surface(self.size).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.actor = actor
        self.dirty = 2
        self.move = 0
        
    def update(self, health, dead):
        if dead == False:        
            if health > 0:
                topleft = self.rect.topleft
                self.image = pg.transform.scale(self.image, (health, self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = topleft

        elif dead == True:
            self.kill()
            
