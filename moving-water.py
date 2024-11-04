# water-moving.py
import pygame as pg

class Water:
    def __init__(self, game_instance, initial_height=50, speed=5):
        self.game_instance = game_instance
        self.window = game_instance.window
        self.width = game_instance.width
        self.height = initial_height
        self.y_position = self.game_instance.height - self.height
        self.speed = speed  # Speed at which the water rises

        # Load the water image
        self.water_image = pg.image.load("/Users/suweerayanoensai/Text-Or-Die_Game_Sec2/assets/water.png")
        self.water_image = pg.transform.scale(self.water_image, (self.width, self.height))

    def move_up(self, amount):
        # Increase the water level by moving it up
        self.y_position -= amount * self.speed
        # Check if the water has reached the top
        if self.y_position < 0:
            self.y_position = 0
            return True  # Indicate game over
        return False  # Continue the game

    def draw(self):
        for y in range(self.y_position, self.game_instance.height, self.height):
            self.window.blit(self.water_image, (0, y))
