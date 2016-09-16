import pygame as pg


class Pickup(pg.sprite.DirtySprite):
    def __init(self, color, size, pos, room, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.room = room