import pygame as pg
import prepare as p
import constants as c
from rooms import Room
from playerinfo import Player
from generate_floors import GenerateFloor
import random


class GameApp():
    """Main class that runs the game."""
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.game_running = True
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()
        self.fps = 60
        
    def new_game(self):
        """Initializes a new game."""
        self.floor = GenerateFloor()
        self.player = Player(self, self.screen_rect.center, (16, 16))
        self.make_rooms()
        self.starting_room = random.choice(self.floor.rooms_on_floor)
        self.room = self.rooms[self.starting_room]
        
        self.all_sprites = pg.sprite.LayeredDirty()
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(c.DARKGREEN)
        self.all_sprites.clear(p.WINDOW, self.background)
        self.all_sprites.add(self.room.wall_container, self.room.door_container,
                             self.room.collider_container, self.player)
        
        self.main_loop()
        
    def start_new_game(self, key):
        if key == pg.K_r:
            self.new_game()
            
    def make_rooms(self):
        room_size = c.SCREEN_SIZE
        wall_size = c.TILE_SIZE
        self.rooms = {}
        for room_number in self.floor.rooms_on_floor:
            exits = self.floor.floor_dict[room_number]
            self.rooms[room_number] = Room(room_number, (0, 0), exits, room_size, wall_size)
            
    def change_room(self, door):
        room = self.rooms[door.exit_to]
        pw, ph = self.player.rect.size
        arrival_spots = {
            "left": (room.rect.right - (door.rect.w + pw), self.player.rect.top),
            "right": (room.rect.left + door.rect.w, self.player.rect.top),
            "up": (self.player.rect.left, room.rect.bottom - (door.rect.h + ph)),
            "down": (self.player.rect.left, room.rect.top + door.rect.h)}
        self.player.rect.topleft = arrival_spots[door.direction]
        self.room = room
        self.all_sprites.empty()
        self.all_sprites.add(self.room.wall_container, self.room.door_container,
                             self.room.collider_container, self.player)
        
    def event_loop(self):
        """
        Processes all events.
        Sends events to player so they can also process events.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.game_running = False
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.start_new_game(event.key)
            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            self.player.get_event(event)
             
    def display_fps(self):
        """Show FPS in the program window."""
        template = "{} - FPS: {:.2f}"
        caption = template.format(c.CAPTION, self.clock.get_fps())
        pg.display.set_caption(caption)
        
    def update(self, dt):
        """Update all sprites."""
        self.player.update(self.room.wall_container)
        for door in self.room.door_container:
            if self.player.rect.colliderect(door.rect):
                self.change_room(door)
                break
        
    def render(self):
        """Draws all sprites to the screen."""
        dirty_rects = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_rects)
        
    def main_loop(self):
        self.clock.tick(self.fps)/1000.0
        dt = 0.0
        while self.game_running:
            self.event_loop()
            self.update(dt)
            self.render()
            dt = self.clock.tick(self.fps)/1000.0
            self.display_fps()