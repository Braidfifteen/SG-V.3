import pygame as pg
import prepare as p


class Sprite(pg.sprite.DirtySprite):
    """Basic sprite class for all actors."""
    def __init__(self, pos, size, color *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = [0, 0]
        

class Player(Sprite):
    """Class that represents user controlled sprite."""
    def __init__(self, game, pos, size, color, *groups):
        super().__init__(pos, size, color, *groups)
        self.game = game
        self.room = None
        self.attributes = None
        self.logic = None
        
    def get_event(self, event):
        """Gets events from game and passes them to Player."""
        pass
        
    def update(self):
        """Update image and position of sprite."""
        pass
        
        
class Enemies(Sprite):
    """Basic enemy class."""
    def __init__(self, player, pos, size, color, *groups):
        super().__init__(pos, size, color, *groups)
        self.player = player
        self.attributes = None
        
    def update(self):
        pass
        
        
    
        