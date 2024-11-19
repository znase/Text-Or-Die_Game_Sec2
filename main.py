import pygame as pg
import sys
from inputbox import inputBox
from problem import problemBox
from background import Background
from boxstack import BoxStack
from win import Win
from moving_water import Water
from spcword import SpecialWordActions
from minimap import Minimap  # นำเข้าคลาส Minimap

# สีต่างๆ
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pg.init()
        self.width = 600
        self.height = 768
        self.window = pg.display.set_mode((self.width, self.height))

        # กำหนดค่าเริ่มต้นของส่วนประกอบต่างๆ
        self.moveup = False
        self.movedown = False
        self.input_box = inputBox(self)
        self.problem_box = problemBox(self)
        self.background = Background(self)
        self.box_stack = BoxStack(self)
        self.win = Win(self)
        self.water = Water(self)
        self.special_word_actions = SpecialWordActions(self)
        self.minimap = Minimap(self, self.box_stack)  # สร้าง Minimap

        self.active = self.input_box.active
        self.input_box_visible = True
        self.game_over = False
        self.cursor_visible = False
        self.cursor_timer = pg.time.get_ticks()
        self.problem_letters = self.problem_box.random_problem()

        self.water_active = True
        self.animations_complete = True

        # แสดงหน้า Start Screen ก่อนเริ่มเกม
        self.start_screen()
        self.game_loop()

    def start_screen(self):
        """แสดงหน้า Start Screen ด้วยภาพพื้นหลังเต็มหน้าจอ"""
        # โหลดภาพพื้นหลังสำหรับหน้า Start Screen
        start_bg = pg.image.load("assets/bag.png").convert()
        start_bg = pg.transform.scale(start_bg, (self.width, self.height))

        while True:
            # วาดภาพพื้นหลังแบบเต็มหน้าจอ
            self.window.blit(start_bg, (0, 0))
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                # เมื่อผู้เล่นคลิกเมาส์ที่ใดก็ได้ จะเข้าสู่เกม
                if event.type == pg.MOUSEBUTTONDOWN:
                    return  # ออกจากฟังก์ชัน start_screen() และเข้าสู่ game_loop()

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

                            # การกระทำเมื่อกรอกข้อความใน input box
                            self.input_box_visible = False
                            self.animations_complete = False

                            if self.water_active:
                                self.water.add_water()

                            if correct_letters is not None:
                                characters_moved = len(correct_letters)
                                self.box_stack.add_boxes(characters_moved)
                                self.background.move_up(characters_moved)
                                self.moveup = True
                                self.win.move_up(characters_moved)
                                self.box_stack.add_letters(correct_letters)
                                  # อัปเดตบรรทัด: ส่งค่าตัวแปร movedown
                            else:
                                self.movedown = True  # คำตอบไม่ถูกต้อง ให้ย้ายเครื่องหมายลง
                                self.moveup = False
                                print("Incorrect Answer: Background will not move.")
                                #self.minimap.update(self.moveup, self.movedown, characters_moved)  # อัปเดตบรรทัด: ส่งค่าตัวแปร movedown
                            self.minimap.update(characters_moved, self.moveup, self.movedown)  # อัปเดต Minimap
                            self.box_stack.move_down()
                            self.special_word_actions.trigger_action(user_input.lower())

                        elif event.key == pg.K_BACKSPACE:
                            self.input_box.text = self.input_box.text[:-1]
                        else:
                            self.input_box.text += event.unicode

            # สลับการแสดง/ซ่อนของตัวชี้ตำแหน่ง
            if self.active and not self.game_over:
                if pg.time.get_ticks() - self.cursor_timer > 500:
                    self.cursor_visible = not self.cursor_visible
                    self.cursor_timer = pg.time.get_ticks()

            # อัปเดตส่วนประกอบต่างๆ ของเกม ถ้ายังไม่จบเกม
            if not self.game_over:
                background_done = self.background.update()
                boxstack_done = self.box_stack.update()
                water_done = self.water.update()
                
                self.animations_complete = background_done and boxstack_done and water_done

                if self.animations_complete:
                    self.input_box_visible = True
                    self.moveup = False

                # ตรวจสอบเงื่อนไขการชนะหรือแพ้
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

            # วาดส่วนประกอบต่างๆ ของเกม
            self.background.draw()
            self.box_stack.draw()
            if self.water_active:
                self.water.draw()
            self.win.draw()
            self.minimap.draw()  # วาด Minimap
            self.problem_box.display_problem(self.problem_letters, self.input_box_visible)
            
            # วาดการกระทำของคำพิเศษ
            if not self.game_over:
                character_top_y = self.box_stack.get_character_top()
                if character_top_y is not None:
                    self.special_word_actions.draw(character_top_y)

            if self.input_box_visible:
                self.input_box.draw_input_box()
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()

            # อัปเดตหน้าจอ
            pg.display.update()
            clock.tick(60)

    def display_message(self, text):
        """แสดงข้อความที่กลางหน้าจอ"""
        self.window.fill(WHITE)
        font = pg.font.Font(None, 74)
        message = font.render(text, True, BLACK)
        text_rect = message.get_rect(center=(self.width // 2, self.height // 2))
        self.window.blit(message, text_rect)
        pg.display.update()
        pg.time.delay(2000)

# เริ่มเกม
if __name__ == "__main__":
    game = Game()
