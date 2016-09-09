import os
import pygame as pg
import constants as c

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.display.set_caption(c.CAPTION)
WINDOW = pg.display.set_mode(c.SCREEN_SIZE)
WINDOW_RECT = WINDOW.get_rect()