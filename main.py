# main.py
import pygame as pg
import sys
from inputbox import inputBox
from problem import problemBox, check_text
from background import Background  # Import Background class

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pg.init()
        self.width = 600
        self.height = 768
        self.window = pg.display.set_mode((self.width, self.height))

        # Initialize components
        self.input_box = inputBox(self)
        self.problem_box = problemBox(self)
        self.background = Background(self)  # Initialize Background instance

        self.active = self.input_box.active
        self.text = ''
        self.input_box_visible = True
        self.cursor_visible = False
        self.cursor_timer = pg.time.get_ticks()
        self.problem_letters = self.problem_box.random_problem()

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
                            user_input = self.input_box.text
                            print("User Input:", user_input)
                            
                            # ตรวจสอบว่าคำตอบถูกต้องหรือไม่
                            is_correct = check_text(self.problem_letters, user_input)
                            self.input_box.text = ''
                            self.problem_letters = self.problem_box.random_problem()
                            
                            # ถ้าคำตอบถูกต้องให้เลื่อนพื้นหลัง
                            if is_correct:
                                if self.background.move_up(len(user_input)):
                                    print("Game Over: Background reached the top!")
                                    pg.quit()
                                    sys.exit()
                            else:
                                print("Incorrect Answer: Background will not move.")

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
            self.background.draw()  # วาดภาพพื้นหลัง
            self.problem_box.display_problem(self.problem_letters)  # Display problem
            if self.input_box_visible:
                self.input_box.draw_input_box()
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()

            pg.display.update()

# Start the game
if __name__ == "__main__":
    game = Game()
