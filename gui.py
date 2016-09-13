import pygame as pg
import constants as c

class HealthBar(pg.sprite.DirtySprite):
    def __init__(self, actor, size, pos, color, *groups):
        super().__init__(*groups)
        self.size = size
        self.image = pg.Surface(self.size).convert()
        self.image.fill(color)
        pg.draw.rect(self.image, c.WHITE, (pos, self.size), 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.actor = actor
        self.move = 0
        self.dirty = 2
        self.health_timer_on = False
        self.health_timer = 0
        
    def update(self, health, dead):
        if dead == False:        
            if health > 0:
                old_pos = self.rect.topright
                topleft = self.rect.topleft
                self.image = pg.transform.scale(self.image, (health, self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = topleft
                pg.draw.rect(self.image, c.WHITE, (0, 0, 100, self.size[1]), 2)
                """ This code works, but I need to get make the enemies
                    health bar movement cleaner and with dirty.
                    
                if old_pos != self.rect.topright:
                    self.dirty = 1
                """
                    

        elif dead == True:
            self.kill()
            
    def health_timer_start(self, dt):
        self.health_timer += dt
        if self.health_timer >= 450:
            self.kill()
            self.health_timer_on = False
            self.health_timer = 0
            self.move = 0   

            
class DrawText(pg.sprite.DirtySprite):
    def __init__(self, player, pos, *groups):
        super().__init__(*groups)
        self.font = pg.font.SysFont("Arial", 25)
        self.color = c.WHITE
        self.image = None
        self.rect = None
        self.position = pos
        self.player = player
        
    def update(self, text):
        old_text = self.player.gun.ammo
        if text != old_text:
            self.dirty = 1
        self.image = self.font.render(text, 0, self.color)
        self.rect = self.image.get_rect(topleft=self.position)