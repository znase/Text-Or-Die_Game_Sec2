# main.py
import pygame as pg
import sys
from inputbox import inputBox
from problem import problemBox
from background import Background
from boxstack import BoxStack
from win import Win
from moving_water import Water
from spcword import SpecialWordActions  # Import SpecialWordActions class

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
        self.water = Water(self)
        self.special_word_actions = SpecialWordActions(self)  # Initialize SpecialWordActions

        self.active = self.input_box.active
        self.input_box_visible = True
        self.moveup = False
        self.game_over = False
        self.cursor_visible = False
        self.cursor_timer = pg.time.get_ticks()
        self.problem_letters = self.problem_box.random_problem()

        self.water_active = True
        self.animations_complete = True
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
                    if self.active and self.input_box_visible:
                        if event.key == pg.K_RETURN:
                            user_input = self.input_box.text
                            correct_letters = self.problem_box.check_text(self.problem_letters, user_input)
                            self.input_box.text = ''
                            self.problem_letters = self.problem_box.random_problem()

                            # Actions when the input box is submitted
                            self.input_box_visible = False
                            self.animations_complete = False

                            if self.water_active:
                                self.water.add_water()

                            if correct_letters is not None:
                                self.box_stack.add_boxes(len(correct_letters))
                                self.background.move_up(len(correct_letters))
                                self.moveup = True
                                self.win.move_up(len(correct_letters))
                                self.box_stack.add_letters(correct_letters)
                            else:
                                print("Incorrect Answer: Background will not move.")

                            self.box_stack.move_down()

                            # ตรวจสอบคำพิเศษและเรียก action
                            self.special_word_actions.trigger_action(user_input.lower())  # เรียกใช้ action

                        elif event.key == pg.K_BACKSPACE:
                            self.input_box.text = self.input_box.text[:-1]
                        else:
                            self.input_box.text += event.unicode

            # Toggle cursor visibility
            if self.active and not self.game_over:
                if pg.time.get_ticks() - self.cursor_timer > 500:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = pg.time.get_ticks()

            # Update game elements if not game over
            if not self.game_over:
                background_done = self.background.update()
                boxstack_done = self.box_stack.update()
                water_done = self.water.update()
                
                self.animations_complete = background_done and boxstack_done and water_done

                if self.animations_complete:
                    self.input_box_visible = True  # Show input box when animations are done
                    self.moveup = False

                # Game over or win conditions
                if self.win.update(self.box_stack.get_character_rect()):
                    pg.time.delay(1000)
                    self.display_message("YOU WIN")
                    pg.time.delay(2000)
                    self.game_over = True

                if self.water.get_top() <= self.box_stack.get_character_top():
                    pg.time.delay(1000)
                    self.display_message("GAME OVER")
                    pg.time.delay(2000)
                    self.game_over = True

            # Draw game elements
            self.background.draw()
            self.box_stack.draw()
            if self.water_active:
                self.water.draw()
            self.win.draw()
            self.problem_box.display_problem(self.problem_letters, self.input_box_visible)

            # Draw special word actions
            if not self.game_over:
                character_top_y = self.box_stack.get_character_top()
                if character_top_y is not None:
                    self.special_word_actions.draw(character_top_y)  # Send character_top_y

            if self.input_box_visible:
                self.input_box.draw_input_box()
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()

            # Update display
            pg.display.update()
            clock.tick(60)

    def display_message(self, text):
        """Display a message in the center of the screen."""
        self.window.fill(WHITE)
        font = pg.font.Font(None, 74)
        message = font.render(text, True, BLACK)
        text_rect = message.get_rect(center=(self.width // 2, self.height // 2))
        self.window.blit(message, text_rect)
        pg.display.update()
        pg.time.delay(2000)

        
# Start the game
if __name__ == "__main__":
    game = Game()
