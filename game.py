import pygame as pg
import prepare as p
import constants as c
from rooms import Room
from player import Player
from enemies import Enemies
from generate_floors import GenerateFloor
import random
from gui import DrawText


class GameApp():
    """Main class that runs the game."""
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.game_running = True
        self.clock = pg.time.Clock()
        self.keys = pg.key.get_pressed()
        self.fps = 60
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(c.DARKGREEN)
        
    def new_game(self):
        """Initializes a new game."""
        self.floor = GenerateFloor()
        self.all_sprites = pg.sprite.LayeredDirty()     
        self.all_sprites.clear(p.WINDOW, self.background)     
        self.player = Player(self, self.screen_rect.center, (16, 16))             
        self.make_rooms()
        self.starting_room = random.choice(self.floor.rooms_on_floor)
        self.room = self.rooms[self.starting_room]
        self.all_sprites.add(self.room.make_all_sprites_container(),
                             self.player.all_sprites_container)
        self.main_loop()
        
    def start_new_game(self, key):
        if key == pg.K_RETURN:
            self.new_game()
            
    def make_rooms(self):
        room_size = c.SCREEN_SIZE
        wall_size = c.TILE_SIZE
        self.rooms = {}
        for room_number in self.floor.rooms_on_floor:
            exits = self.floor.floor_dict[room_number]
            self.rooms[room_number] = Room(room_number, (0, 0), exits, room_size, wall_size, self,
            self.player)
            
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
        self.all_sprites.add(self.room.all_sprites_container,
                             self.player.all_sprites_container)
        
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
        
    def check_if_doors_locked(self):
        if len(self.room.enemy_container) <= 0:
            for door in self.room.door_container:
                if door.door_locked_collider.alive():
                    door.unlock_door()
                elif self.player.rect.colliderect(door.rect):
                    self.change_room(door)
                    break

    def update(self, walls, enemies, dt):
        """Update all sprites."""
        self.player.update(self.keys, walls, enemies, dt)
        self.room.update(dt)
        self.check_if_doors_locked()
        
    def render(self):
        """Draws all sprites to the screen."""
        dirty_rects = self.all_sprites.draw(self.screen)
        pg.display.update(dirty_rects)
        
    def main_loop(self):
        while self.game_running:
            self.clock.tick(self.fps)
            dt = self.clock.get_time()
            self.event_loop()
            self.update(self.room.wall_container, self.room.enemy_container, dt)
            self.render()
            self.display_fps()