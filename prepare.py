import os
import pygame as pg
import constants as c

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(c.CAPTION)
WINDOW = pg.display.set_mode(c.SCREEN_SIZE)
WINDOW_RECT = WINDOW.get_rect()

CROSS_HAIR = pg.image.load("C:/Python Projects/SG-V.3/resources/circle_dot.png").convert()
CROSS_HAIR.set_colorkey(c.BLACK)
CROSS_HAIR_HIT = pg.image.load("C:/Python Projects/SG-v.3/resources/circle_dot_hit.png").convert()
CROSS_HAIR_HIT.set_colorkey(c.BLACK)
WALLS = pg.image.load("C:/Python Projects/SG-V.3/resources/walls.png").convert_alpha()
CHASING_ENEMY = pg.image.load(
    "C:/Python Projects/SG-V.3/resources/floatingskel.png").convert()
CHASING_ENEMY.set_colorkey(c.BLACK)
BULLETS = pg.image.load("C:/Python Projects/SG-V.3/resources/bullets.png").convert_alpha()
PLAYER = pg.image.load("C:/Python Projects/SG-V.3/resources/protoplayer.png").convert_alpha()