import pygame as pg
from char import CharMarker

class Minimap:
    def __init__(self, game_instance, box_stack):
        self.game_instance = game_instance
        self.realmap_img = pg.image.load(r"assets/minimap.jpg")
        self.map_img = pg.transform.scale(self.realmap_img, (100, 467))
        self.map_x = self.game_instance.width - 110
        self.map_y = 10
        self.pixel_per_char = 6.6

        self.char_marker = CharMarker(game_instance, self, box_stack)

    def update(self, characters_moved, moveup, movedown):
        """Update the character marker position."""
        self.char_marker.update(moveup, movedown, characters_moved)

    def draw(self):
        """Draw the minimap and character marker."""
        if not self.game_instance.input_box_visible:
            self.game_instance.window.blit(self.map_img, (self.map_x, self.map_y))
            self.char_marker.draw()
            
