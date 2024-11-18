import pygame as pg
import gif_pygame
import os

round = 1

class BoxStack:
    def __init__(self, game_instance):
        """Initialize BoxStack with fixed scaling for the box and character images."""
        self.game_instance = game_instance
        self.stack_positions = []
        self.letter_images = []
        self.pending_boxes = 0
        self.box_timer = pg.time.get_ticks()

        # Load and scale the box image to 1/4 of its original size
        self.original_box_img = pg.image.load(r"assets/box.png")
        self.box_img = pg.transform.scale(self.original_box_img, 
                                          (self.original_box_img.get_width() // 4, 
                                           self.original_box_img.get_height() // 4))
        self.box_width = self.box_img.get_width()
        self.box_height = self.box_img.get_height()
        self.stack_positions = []

        # Load character animation using gif_pygame
        self.char_gif = gif_pygame.load(r"assets/pet.gif")
        self.character_y_offset = -self.char_gif.get_height()

        # Load static character image
        self.char_img = pg.image.load(r"assets/char.png")
        self.char_width = self.char_img.get_width()
        self.char_height = self.char_img.get_height()
        self.char_img = pg.transform.scale(self.char_img, (self.char_width//2, self.char_height//2))

        # Initial stack with one box
        initial_y = self.game_instance.height - self.box_height - 200
        self.stack_positions.append(initial_y)


    def add_letters(self, letters):
        """Add new letter images from a list of text without removing old letters."""
        for letter in reversed(letters):
            letter_img_path = os.path.join("assets", "letters", f"{letter}.png")
            letter_img = pg.image.load(letter_img_path)
            
            # Resize the letter image to fit the box
            scaled_letter_img = pg.transform.scale(letter_img, (self.box_width-40, self.box_height))
            self.letter_images.insert(0, scaled_letter_img)

    def move_down(self, distance=120):
        #print(globalround)
        global round
        if round == 1 :
            pass
        else:
            for i in range(len(self.stack_positions)):
                self.stack_positions[i] += distance
        
        round += 1

    def add_boxes(self, count):
        """Set the number of boxes to be added gradually, one at a time."""
        self.pending_boxes += count

    def update(self):
        """Update and gradually add pending boxes. Return True when all boxes are added."""
        current_time = pg.time.get_ticks()
        if self.pending_boxes > 0 and current_time - self.box_timer >= 1000:
            new_y = self.stack_positions[0] - self.box_height
            self.stack_positions.insert(0, new_y)  # Insert a new box at the top
            self.pending_boxes -= 1  # Decrease the pending box count
            self.box_timer = current_time  # Reset the timer

        # Return True when no more boxes are waiting to be added
        return self.pending_boxes == 0

    def get_character_top(self):
        """Return the y-coordinate of the character's top edge for collision detection."""
        if self.stack_positions:
            return self.stack_positions[0] + self.character_y_offset - 120
        return None

    def draw(self):
        x_center = (self.game_instance.width - self.box_width) // 2
        for i, y in enumerate(self.stack_positions):
            # Draw box
            self.game_instance.window.blit(self.box_img, (x_center, y))
            # Draw letter on the box
            if i < len(self.letter_images):
                letter_x = x_center + (self.box_width - self.letter_images[i].get_width()) // 2
                letter_y = y + (self.box_height - self.letter_images[i].get_height()) // 2
                self.game_instance.window.blit(self.letter_images[i], (letter_x, letter_y))

        # Draw the character on the top box
        if self.stack_positions:
            character_x = x_center
            character_y = self.stack_positions[0] + self.character_y_offset

            if self.game_instance.moveup:
                self.char_gif.unpause()
                self.char_gif.render(self.game_instance.window, (character_x -20, character_y + 5))
            else:
                self.char_gif.pause()
                self.game_instance.window.blit(self.char_img, (character_x-5, character_y+20))

    def get_character_rect(self):
        """Return the rectangle of the character positioned on top of the box stack."""
        if self.stack_positions:
            character_x = (self.game_instance.width - self.box_width) // 2
            character_y = self.stack_positions[0] + self.character_y_offset

            if self.game_instance.moveup:
                return pg.Rect(character_x - 10, character_y, self.char_gif.get_width(), self.char_gif.get_height())
            else:
                return pg.Rect(character_x - 10, character_y, self.char_img.get_width(), self.char_img.get_height())
        return None