import pygame as pg
import constants as c


class Collider(pg.sprite.DirtySprite):
    def __init__(self, topleft, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert()
        self.image.fill(c.RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.dirty = 0
        self.visible = 0
        
