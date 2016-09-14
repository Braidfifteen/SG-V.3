import pygame as pg
import constants as c

class HealthBar(pg.sprite.DirtySprite):
    age_counter = 0
    def __init__(self, actor, size, pos, color, *groups):
        super().__init__(*groups)
        self.size = size
        self.image = pg.Surface(self.size).convert()
        self.image.fill(color)
        #pg.draw.rect(self.image, c.WHITE, (pos, self.size), 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.setup_movement_variables()
        self.actor = actor
        self.age = None
        
    def update(self, health):      
            if health > 0:
                old_pos = self.rect.topright
                topleft = self.rect.topleft
                self.image = pg.transform.scale(self.image, (health, self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = topleft
                #pg.draw.rect(self.image, c.WHITE, (0, 0, 100, self.size[1]), 2)
                if old_pos != self.rect.topright:
                    self.dirty = 1
            else:
                self.kill()
            
    def on_screen_timer_start(self, dt):
        self.on_screen_timer += dt
        if self.on_screen_timer >= self.on_screen_time:
            self.kill()
            self.on_screen_timer_on = False
            self.on_screen_timer = 0
            self.move_up_speed = 0   
    
    def move_health_bar(self, dt):
        self.on_screen_timer_start(dt)
        self.dirty = 1
        self.move_up_speed *= self.move_up_acceleration
        self.rect.y -= self.move_up_speed
        
    def setup_movement_variables(self):
        self.on_screen_time = 450
        self.move_up_speed = 5
        self.move_up_acceleration = 0.8
        self.on_screen_timer_on = False
        self.on_screen_timer = 0
           
    def add_to_group(self, group):
        if len(group) < 3:
            group.add(self)
            HealthBar.age_counter += 1
            self.age = HealthBar.age_counter
        elif len(group) >= 3:
            oldest_bar = [min(i.age for i in group)]
            for i in group:
                if i.age == oldest_bar[0]:
                    i.kill()
            group.add(self)
            HealthBar.age_counter += 1
            self.age = HealthBar.age_counter
        
        
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