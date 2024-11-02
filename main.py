import pygame as pg
import sys
from inputbox import inputBox  # Import inputBox from inputbox.py
from problem import problemBox, check_text  # Import problemBox and check_text from problem.py

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pg.init()
        self.width = 600
        self.height = 768
        self.window = pg.display.set_mode((self.width, self.height))
        self.bg_img = pg.image.load(r"assets/bg.jpg")

        # Initialize input box and problem box
        self.input_box = inputBox(self)
        self.problem_box = problemBox(self)  # Initialize problemBox with Game instance

        self.active = self.input_box.active
        self.text = ''
        self.input_box_visible = True
        self.cursor_visible = False
        self.cursor_timer = pg.time.get_ticks()

        self.problem_letters = self.problem_box.random_problem()  # Generate initial problem

        self.game_loop()

    def game_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_box.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.input_box.color_active if self.active else self.input_box.color_inactive

                if event.type == pg.KEYDOWN:
                    if self.active:
                        if event.key == pg.K_RETURN:
                            print("User Input:", self.input_box.text)
                            check_text(self.problem_letters, self.input_box.text)  # Check if input is correct
                            self.input_box.text = ''
                            self.problem_letters = self.problem_box.random_problem()  # Generate new problem
                        elif event.key == pg.K_BACKSPACE:
                            self.input_box.text = self.input_box.text[:-1]
                        else:
                            self.input_box.text += event.unicode
                        
            # Change cursor visibility
            if self.active:
                if pg.time.get_ticks() - self.cursor_timer > 500:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = pg.time.get_ticks()

            # Render background and components
            self.window.blit(self.bg_img, (0, -2050))

            # Draw problem text and input box
            self.problem_box.display_problem(self.problem_letters)  # Display the problem
            if self.input_box_visible:
                self.input_box.draw_input_box()
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()

            pg.display.update()

# Start the game
if __name__ == "__main__":
    game = Game()
