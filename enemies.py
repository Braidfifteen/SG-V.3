import pygame as pg
import prepare as p

            

        
class Enemies(pg.sprite.DirtySprite):
    """Basic enemy class."""
    def __init__(self, player, pos, size, color, *groups):
        super().__init__(pos, size, color, *groups)
        self.player = player
        self.attributes = None
        
    def update(self):
        pass
        
        
    
        