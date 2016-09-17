import pygame as pg
import constants as c


class Collider(pg.sprite.DirtySprite):
    def __init__(self, topleft, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert_alpha()
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.topleft = topleft
        self.visible = 0


