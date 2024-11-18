import pygame as pg

round = 1

class CharMarker:
    def __init__(self, game_instance, minimap, box_stack):
        self.game_instance = game_instance
        self.minimap = minimap
        self.box_stack = box_stack

        self.marker_img = pg.image.load("assets/char.png")
        self.marker_image = pg.transform.scale(self.marker_img, (30, 30))

        self.marker_width = self.marker_image.get_width()
        self.marker_height = self.marker_image.get_height()

        self.marker_x = self.minimap.map_x + (self.minimap.map_img.get_width() // 2) - (self.marker_width // 2)
        self.marker_y = self.minimap.map_y + self.minimap.map_img.get_height() - self.marker_height - 30
        self.scale_factor = 1 / 2.7

        self.round = 1

    def update(self, moveup, movedown, char_count=0, distance=120):
        """Update the marker's position."""
        if moveup:
            if self.round == 1:
                self.marker_y -= char_count * self.box_stack.box_height * self.scale_factor
            else :
                self.marker_y -= char_count * self.box_stack.box_height * self.scale_factor 
                self.marker_y += distance * self.scale_factor / 1.5
        elif movedown:
            if self.round == 1:
                pass  # No movement for round 1
            else:
                self.marker_y += distance * self.scale_factor /1.5
        self.round += 1  # Increment round

    def draw(self):
        """Draw the marker on the minimap."""
        if not self.game_instance.input_box_visible:
            self.game_instance.window.blit(self.marker_image, (self.marker_x, self.marker_y))
            
