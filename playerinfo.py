import pygame as pg
import constants as c






class Player(pg.sprite.DirtySprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size).convert_alpha()
        self.image.fill((c.BLACK))
        self.rect = self.image.get_rect(center=pos)
        self.true_pos = list(self.rect.center)
        self.room = None
        self.stats = PlayerStats()


    def get_event(self, event, keys):
        pass
       
        
                    
                
            
    def update(self, keys, dt):
        self.vector = [0, 0]
        for key in c.CONTROLS:
            if keys[key]:
                direction = c.CONTROLS[key]
                self.vector[0] += c.DIRECT_DICT[direction][0]
                self.vector[1] += c.DIRECT_DICT[direction][1]     
        
        
        
        old_pos = self.rect.center
        factor = (c.ANGLE_UNIT_SPEED if all(self.vector) else 1)
        frame_speed = self.stats.speed*factor*dt
        self.true_pos[0] += self.vector[0]*frame_speed
        self.true_pos[1] += self.vector[1]*frame_speed
        self.rect.center = self.true_pos
        if self.rect.center != old_pos:
            self.dirty = 1

class PlayerStats():
    def __init__(self):
        self.speed = 250
        
class PlayerLogic():
    def __init(self):
        pass