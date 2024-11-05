# main.py
import pygame as pg
import sys
from inputbox import inputBox
from problem import problemBox, check_text
from background import Background
from boxstack import BoxStack

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
        self.background = Background(self)
        self.box_stack = BoxStack(self)

        self.active = self.input_box.active
        self.text = ''
        self.input_box_visible = True
        self.cursor_visible = False
        self.cursor_timer = pg.time.get_ticks()
        self.problem_letters = self.problem_box.random_problem()

        self.game_loop()

    def game_loop(self):
        clock = pg.time.Clock()
        
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
        
                            # ตรวจสอบคำตอบของผู้ใช้
                            correct_letters = check_text(self.problem_letters, user_input)
                            self.input_box.text = ''
                            self.problem_letters = self.problem_box.random_problem()
                        
                            if correct_letters is not None:
                                self.box_stack.add_boxes(len(correct_letters))
                                self.background.move_up(len(correct_letters))
    
                                # เพิ่มตัวอักษรของคำตอบที่ถูกต้องใหม่ลงในกล่อง
                                self.box_stack.add_letters(correct_letters)
                                
                                # เลื่อนกล่องลง
                                self.box_stack.move_down(80)

                            else:
                                print("Incorrect Answer: Background will not move.")
                                self.box_stack.move_down(80)


                        elif event.key == pg.K_BACKSPACE:
                            self.input_box.text = self.input_box.text[:-1]
                        else:
                            self.input_box.text += event.unicode

            # Change cursor visibility
            if self.active:
                if pg.time.get_ticks() - self.cursor_timer > 500:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = pg.time.get_ticks()

            # Update and render
            if self.background.update():  # Gradually scroll the background
                print("Game Over: Background reached the top!")
                pg.quit()
                sys.exit()

            self.background.draw()
            self.box_stack.draw()
            self.problem_box.display_problem(self.problem_letters)
            if self.input_box_visible:
                self.input_box.draw_input_box()
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()

            pg.display.update()
            clock.tick(60)  # Limit FPS to make scrolling smooth

# Start the game
if __name__ == "__main__":
    game = Game()