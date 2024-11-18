# moving_water.py
import pygame as pg

class Water:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        # Load water image and scale it to match screen width
        self.water_img = pg.image.load("assets/water.png")
        self.water_img = pg.transform.scale(self.water_img, (self.game_instance.width, self.water_img.get_height()))

        # Set initial position to show only the wave section at the bottom
        self.y_position = self.game_instance.height - 400  # Adjust this value based on the wave height
        self.target_y_position = self.y_position
        self.rise_amount = 5  # Amount to rise per answer submission
        self.slide_speed = 0.5  # Speed of sliding up the image

    def add_water(self):
        """Increase the target position to slide up the image and reveal more water."""
        self.target_y_position -= self.rise_amount

    def update(self):
        """Slide the water image upwards smoothly towards the target position."""
        if self.y_position > self.target_y_position:
            self.y_position -= self.slide_speed  # Adjust this value for a smoother or faster rise
        
        if self.y_position <= self.target_y_position:
            return True  # Animation complete
        return False
            
    # In moving_water.py
    def get_top(self):
        """Return the current top y-position of the water for collision detection."""
        return self.y_position


    def draw(self):
        """Draw the water image with a sliding effect."""
        # Blit the water image at the current y_position
        self.game_instance.window.blit(self.water_img, (0, self.y_position))
