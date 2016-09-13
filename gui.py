import pygame as pg
import constants as c

class HealthBar(pg.sprite.DirtySprite):
    def __init__(self, actor, size, pos, *groups):
        super().__init__(*groups)
        self.size = size
        self.image = pg.Surface(self.size).convert()
        self.image.fill(c.BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.actor = actor
        
    def update(self, health, dead):
        self.dirty = 1
        """

        elif health >= 0:
            self.kill()
        """
        if dead == False:        
            if health > 0:
                self.image = pg.transform.scale(self.image, (health, 10))
        elif dead == True:
            self.kill()