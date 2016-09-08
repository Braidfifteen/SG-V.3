import pygame as pg
import prepare as p


class GameApp():
    """Main class that runs the game."""
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.game_running = True
        self.clock = pg.time.Clock()
        
    def new_game(self):
        """Initializes a new game."""
        self.player = None
        self.room = None
        
        self.all_sprites = pg.sprite.LayeredDirty()
        self.background = pg.Surface(self.screen.getsize()).convert()
        self.background.fill(p.DARKSLATEGREY)
        self.all_sprites.clear(p.WINDOW, self.background)
        
        self.main_loop()
        
    def event_loop(self):
        """
        Processes all events.
        Sends events to player so they can also process events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.new_game()
            self.player.get_event(event)
            
    def display_fps(self):
        """Show FPS in the program window."""
        template = "{} - FPS: {:.2f}"
        caption = template.format(p.CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)
        
    def update(self):
        """Update all sprites."""
        self.all_sprites.update()
        
    def render(self):
        """Draws all sprites to the screen."""
        dirty_rects = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_rects)
        
    def main_loop(self):
        while self.game_running:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(p.FPS)
            self.display_fps()