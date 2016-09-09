import sys
import game
import pygame as pg

def main():
    """Create game and start it."""
    game.GameApp().new_game()
    pg.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()