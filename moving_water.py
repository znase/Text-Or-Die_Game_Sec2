import pygame as pg

class Water:
    def __init__(self, game_instance, initial_height=50, speed=5):
        self.game_instance = game_instance
        self.window = game_instance.window
        self.width = game_instance.width
        self.initial_height = initial_height
        self.current_height = initial_height  # Track the current height of the water
        self.y_position = self.game_instance.height - self.current_height
        self.speed = speed  # Speed at which the water rises
        self.rise_count = 1  # Start at the first increment

        # Load the wave texture (to be used only at the top of the water)
        self.wave_image = pg.image.load("assets/water.png")
        self.wave_image = pg.transform.scale(self.wave_image, (self.width, 50))  # Adjust for a small wave height

        # Set a color for the main water area (without texture)
        self.water_color = (0, 128, 255)  # Blue color for the water

    def add_water(self):
        # Increase the water height incrementally with each correct answer
        increment_height = self.rise_count * self.speed
        self.current_height += increment_height
        self.rise_count += 1

        # Update the y_position to reflect the new water height
        self.y_position = self.game_instance.height - self.current_height

        # Ensure that the water doesn’t go above the screen
        if self.current_height >= self.game_instance.height:
            self.current_height = self.game_instance.height
            self.y_position = 0  # Clamp at the top

    def draw(self):
        # Fill the area with a solid color for the main water
        pg.draw.rect(self.window, self.water_color, (0, self.y_position, self.width, self.current_height))

        # Draw the wave texture at the top of the water to create a surface effect
        self.window.blit(self.wave_image, (0, self.y_position - 50))  # Adjust so the waves appear at the top





