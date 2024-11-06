# background.py
import pygame as pg

class Background:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.bg_img = pg.image.load(r"assets/bg.jpg")  # Load background image
        self.bg_y = self.game_instance.height - self.bg_img.get_height()  # Start at the bottom
        self.pixel_per_char = 20  # Pixels to move up per character
        self.target_y = self.bg_y  # Target position for the background

    def move_up(self, char_count):
        """Set a new target position based on the number of correct characters."""
        move_distance = char_count * self.pixel_per_char
        self.target_y += move_distance

    def update(self):
        """Gradually move the background towards the target position."""
        if self.bg_y < self.target_y:
            self.bg_y += 1.5  # Adjust this for slower or faster scrolling

        # Stop scrolling if the background reaches the top
        if self.bg_y >= 0:
            self.bg_y = 0
            return True  # Stop the game when reaching the top
        return False

    def draw(self):
        """Draw the background at the current position."""
        self.game_instance.window.blit(self.bg_img, (0, self.bg_y))
