import pandas as pd
import random
import pygame as pg
from rapidfuzz import process

# Load dictionary data
df = pd.read_excel(r'data/dictionary.xlsx', sheet_name='dictionary')
letters = "abcdefghijklmnopqrstuvwxyz"

class problemBox:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.font = pg.font.Font(None, 36)
        self.window = game_instance.window
        
        # Load and scale the background image for the problem text
        self.bg_image = pg.image.load(r"assets\letters\textBox.png")
        self.bg_image = pg.transform.scale(self.bg_image, (550, 80))  # Adjust size as needed

    def random_problem(self):
        """Generate a random letter problem."""
        return random.sample(letters, 2)

    def display_problem(self, letters):
        """Render the problem text with a background image."""
        # Center the background image on the screen
        bg_x = (self.game_instance.width - self.bg_image.get_width()) // 2
        bg_y = (self.game_instance.height // 2 - 340)  # Adjust position as needed
        self.window.blit(self.bg_image, (bg_x, bg_y))

        # Render and display the problem text
        text_surface = self.font.render(f"Input a word with letters '{letters[0].upper()}' and '{letters[1].upper()}'", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.game_instance.width // 2, self.game_instance.height // 2 - 300))
        self.window.blit(text_surface, text_rect)

def check_text(problem, text):
    """Check if the user input matches the problem criteria."""
    text = text.lower()
    match = process.extractOne(text, df.key)
    
    if match and match[1] == 100.00 and all(letter in text for letter in problem):
        print("Correct")
        score = len(text)  # Increment score based on the length of the text
    else:
        print("Incorrect")
        score = 0
