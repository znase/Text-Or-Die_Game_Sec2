import pygame as pg
import sys
from inputbox import inputBox
from problem import problemBox, check_text
from background import Background
from boxstack import BoxStack
from win import Win
from moving_water import Water  # Import the Water class

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
        self.win = Win(self)
        self.water = Water(self)  # Initialize the Water class

        self.active = self.input_box.active
        self.text = ''
        self.input_box_visible = True
        self.cursor_visible = False
        self.cursor_timer = pg.time.get_ticks()
        self.problem_letters = self.problem_box.random_problem()

        self.water_active = True  # Start the water effect immediately
        self.game_over = False  # Track game-over state
        self.game_loop()

    def game_loop(self):
        clock = pg.time.Clock()
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and not self.game_over:
                    if self.input_box.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.input_box.color_active if self.active else self.input_box.color_inactive

                if event.type == pg.KEYDOWN and not self.game_over:
                    if self.active:
                        if event.key == pg.K_RETURN:
                            user_input = self.input_box.text
                            print("User Input:", user_input)

                            # ตรวจสอบคำตอบของผู้ใช้
                            correct_letters = check_text(self.problem_letters, user_input)
                            self.input_box.text = ''
                            self.problem_letters = self.problem_box.random_problem()

                            # เลื่อนระดับน้ำทุกครั้งที่ผู้ใช้กรอกคำตอบ
                            if self.water_active:
                                self.water.add_water()

                            if correct_letters is not None:
                                # เพิ่มกล่องข้อความถ้าตอบถูก
                                self.box_stack.add_boxes(len(correct_letters))
                                self.background.move_up(len(correct_letters))
                                self.win.move_up(len(correct_letters))
                                self.box_stack.add_letters(correct_letters)
                            else:
                                print("Incorrect Answer: Background will not move.")

                            # เลื่อนกล่องลงทุกครั้ง
                            self.box_stack.move_down()

                        elif event.key == pg.K_BACKSPACE:
                            self.input_box.text = self.input_box.text[:-1]
                        else:
                            self.input_box.text += event.unicode

            # Change cursor visibility
            if self.active and not self.game_over:
                if pg.time.get_ticks() - self.cursor_timer > 500:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = pg.time.get_ticks()

            # Update and render game elements if not game over
            # In Game class's game_loop method
            if not self.game_over:
                # Check for collision between water and character
                character_top = self.box_stack.get_character_top()
                if character_top is not None and self.water.get_top() <= character_top:
                    print("Game Over: Water reached the character!")
                    self.game_over = True

                # Update water if active
                if self.water_active:
                    self.water.update()

                # Check for collision between water and character
                if self.water.get_top() <= self.box_stack.get_character_top():
                    print("Game Over: Water reached the character!")
                    self.game_over = True

                # Check for win condition
                if self.win.update(self.box_stack.get_character_rect()):
                    # Display "YOU WIN" message if collision detected
                    self.window.fill(WHITE)
                    font = pg.font.Font(None, 74)
                    text = font.render("YOU WIN", True, BLACK)
                    text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                    self.window.blit(text, text_rect)
                    pg.display.update()
                    pg.time.delay(2000)
                    self.game_over = True

            # Draw elements
            self.background.draw()
            self.box_stack.draw()
            if self.water_active:
                self.water.draw()
            self.win.draw()
            self.problem_box.display_problem(self.problem_letters)
            if self.input_box_visible:
                self.input_box.draw_input_box()
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()

            # Display "Game Over" message if game is over
            if self.game_over:
                font = pg.font.Font(None, 74)
                text = font.render("GAME OVER", True, BLACK)
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.window.blit(text, text_rect)
                pg.display.update()

            # Update display and control frame rate
            pg.display.update()
            clock.tick(60)

# Start the game
if __name__ == "__main__":
    game = Game()
