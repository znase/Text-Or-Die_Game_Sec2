import pygame as pg
import sys
from inputbox import inputBox
from problem import problemBox
from background import Background
from boxstack import BoxStack
from win import Win
from moving_water import Water
from spcword import SpecialWordActions
from minimap import Minimap  # นำเข้าคลาส Minimap สำหรับแสดงแผนที่ย่อ

# สีต่างๆ สำหรับใช้ในการวาด
WHITE = (255, 255, 255)  # สีขาว
BLACK = (0, 0, 0)  # สีดำ

class Game:
    def __init__(self):
        pg.init()  # เริ่มต้น pygame
        self.width = 600  # กำหนดความกว้างของหน้าจอเกม
        self.height = 768  # กำหนดความสูงของหน้าจอเกม
        self.window = pg.display.set_mode((self.width, self.height))  # สร้างหน้าต่างเกม

        # กำหนดค่าเริ่มต้นสำหรับส่วนต่างๆ ของเกม
        self.moveup = False  # ตัวแปรสำหรับการเลื่อนขึ้นของฉาก
        self.movedown = False  # ตัวแปรสำหรับการเลื่อนลงของฉาก
        self.input_box = inputBox(self)  # สร้างกล่องสำหรับกรอกข้อความ
        self.problem_box = problemBox(self)  # สร้างกล่องสำหรับแสดงปัญหาที่ต้องแก้
        self.background = Background(self)  # สร้างพื้นหลังเกม
        self.box_stack = BoxStack(self)  # สร้างกล่องที่ต้องวางซ้อน
        self.win = Win(self)  # สร้างหน้าจอการชนะเกม
        self.water = Water(self)  # สร้างน้ำที่เคลื่อนที่
        self.special_word_actions = SpecialWordActions(self)  # สร้างการกระทำจากคำพิเศษ
        self.minimap = Minimap(self, self.box_stack)  # สร้างแผนที่ย่อ (Minimap)

        # กำหนดค่าพื้นฐานเพิ่มเติม
        self.active = self.input_box.active  # กำหนดสถานะของกล่องข้อความ
        self.input_box_visible = True  # ให้กล่องข้อความมองเห็น
        self.game_over = False  # กำหนดว่าเกมยังไม่จบ
        self.cursor_visible = False  # กำหนดให้ตัวชี้ไม่มองเห็น
        self.cursor_timer = pg.time.get_ticks()  # ตั้งเวลาในการสลับการแสดงตัวชี้
        self.problem_letters = self.problem_box.random_problem()  # กำหนดคำปัญหาจากการสุ่ม

        self.water_active = True  # เปิดการเคลื่อนที่ของน้ำ
        self.animations_complete = True  # กำหนดว่าแอนิเมชั่นเสร็จสมบูรณ์

        # แสดงหน้า Start Screen ก่อนเริ่มเกม
        self.start_screen()
        self.game_loop()  # เริ่มเกม

    def start_screen(self):
        """แสดงหน้า Start Screen ด้วยภาพพื้นหลังเต็มหน้าจอ"""
        start_bg = pg.image.load("assets/bag.png").convert()  # โหลดภาพพื้นหลัง
        start_bg = pg.transform.scale(start_bg, (self.width, self.height))  # ปรับขนาดภาพให้เต็มหน้าจอ

        while True:
            # วาดภาพพื้นหลังแบบเต็มหน้าจอ
            self.window.blit(start_bg, (0, 0))
            pg.display.update()  # อัปเดตหน้าจอ

            for event in pg.event.get():
                if event.type == pg.QUIT:  # ถ้าผู้เล่นกดปิดหน้าต่าง
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:  # ถ้าผู้เล่นคลิกเมาส์
                    return  # ออกจากฟังก์ชัน start_screen() และเข้าสู่ game_loop()

    def game_loop(self):
        """ฟังก์ชันหลักของเกมที่ทำงานวนรอบ"""
        clock = pg.time.Clock()  # กำหนดเวลาในการควบคุมเฟรม

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # ถ้าผู้เล่นกดปิดหน้าต่าง
                    pg.quit()
                    sys.exit()

                # เมื่อผู้เล่นคลิกที่กล่องข้อความ
                if event.type == pg.MOUSEBUTTONDOWN and not self.game_over:
                    if self.input_box.input_box.collidepoint(event.pos):  # ถ้าคลิกที่กล่องข้อความ
                        self.active = not self.active  # สลับสถานะการใช้งานของกล่องข้อความ
                    else:
                        self.active = False  # ถ้าคลิกที่อื่นให้ปิดการใช้งานกล่องข้อความ
                    self.color = self.input_box.color_active if self.active else self.input_box.color_inactive

                # เมื่อผู้เล่นกดปุ่มคีย์
                if event.type == pg.KEYDOWN and not self.game_over:
                    if self.active and self.input_box_visible:
                        if event.key == pg.K_RETURN:  # เมื่อกด Enter
                            user_input = self.input_box.text  # รับค่าข้อความจากกล่องข้อความ
                            correct_letters = self.problem_box.check_text(self.problem_letters, user_input)  # ตรวจสอบคำตอบ
                            self.input_box.text = ''  # เคลียร์ข้อความจากกล่อง
                            self.problem_letters = self.problem_box.random_problem()  # สุ่มคำใหม่

                            # การกระทำเมื่อกรอกข้อความใน input box
                            self.input_box_visible = False  # ซ่อนกล่องข้อความ
                            self.animations_complete = False  # กำหนดว่าแอนิเมชั่นยังไม่เสร็จ

                            if self.water_active:
                                self.water.add_water()  # เพิ่มน้ำในเกม

                            if correct_letters is not None:
                                characters_moved = len(correct_letters)  # จำนวนตัวอักษรที่ถูกต้อง
                                self.box_stack.add_boxes(characters_moved)  # เพิ่มกล่องใหม่ในสแต็ก
                                self.background.move_up(characters_moved)  # เลื่อนพื้นหลังขึ้น
                                self.moveup = True  # ตั้งค่าสถานะการเลื่อนขึ้น
                                self.win.move_up(characters_moved)  # เลื่อนตำแหน่งหน้าจอการชนะ
                                self.box_stack.add_letters(correct_letters)  # เพิ่มตัวอักษรที่ถูกต้อง
                            else:
                                self.movedown = True  # ถ้าคำตอบผิด ให้เลื่อนเครื่องหมายลง
                                self.moveup = False
                                print("Incorrect Answer: Background will not move.")
                            self.minimap.update(characters_moved, self.moveup, self.movedown)  # อัปเดตแผนที่ย่อ
                            self.box_stack.move_down()  # ย้ายกล่องลง
                            self.special_word_actions.trigger_action(user_input.lower())  # กระตุ้นการกระทำของคำพิเศษ

                        elif event.key == pg.K_BACKSPACE:  # ถ้ากดปุ่ม backspace
                            self.input_box.text = self.input_box.text[:-1]  # ลบตัวอักษรล่าสุด
                        else:
                            self.input_box.text += event.unicode  # เพิ่มตัวอักษรที่พิมพ์

            # สลับการแสดง/ซ่อนตัวชี้ตำแหน่ง
            if self.active and not self.game_over:
                if pg.time.get_ticks() - self.cursor_timer > 500:  # ถ้าเวลาผ่านไป 500 มิลลิวินาที
                    self.cursor_visible = not self.cursor_visible  # สลับสถานะการแสดงตัวชี้
                    self.cursor_timer = pg.time.get_ticks()  # รีเซ็ตเวลา

            # อัปเดตส่วนต่างๆ ของเกม ถ้ายังไม่จบเกม
            if not self.game_over:
                background_done = self.background.update()
                boxstack_done = self.box_stack.update()
                water_done = self.water.update()
                
                self.animations_complete = background_done and boxstack_done and water_done  # ตรวจสอบว่าแอนิเมชั่นเสร็จสมบูรณ์

                if self.animations_complete:
                    self.input_box_visible = True  # แสดงกล่องข้อความ
                    self.moveup = False

                # เงื่อนไขการชนะหรือแพ้
                if self.win.update(self.box_stack.get_character_rect()):  # ถ้าชนะ
                    pg.time.delay(1000)  # หยุดเวลา 1 วินาที
                    self.display_message("YOU WIN")  # แสดงข้อความ "YOU WIN"
                    pg.time.delay(2000)  # หยุดเวลา 2 วินาที
                    self.game_over = True  # เกมจบ

                if self.water.get_top() <= self.box_stack.get_character_top():  # ถ้าน้ำเต็ม
                    pg.time.delay(1000)
                    self.display_message("GAME OVER")  # แสดงข้อความ "GAME OVER"
                    pg.time.delay(2000)
                    self.game_over = True  # เกมจบ

            # วาดส่วนต่างๆ ของเกม
            self.background.draw()  # วาดพื้นหลัง
            self.box_stack.draw()  # วาดกล่องซ้อน
            if self.water_active:
                self.water.draw()  # วาดน้ำ
            self.win.draw()  # วาดหน้าจอการชนะ
            self.minimap.draw()  # วาดแผนที่ย่อ
            self.problem_box.display_problem(self.problem_letters, self.input_box_visible)  # แสดงปัญหาที่ต้องแก้
            
            # วาดการกระทำของคำพิเศษ
            if not self.game_over:
                character_top_y = self.box_stack.get_character_top()
                if character_top_y is not None:
                    self.special_word_actions.draw(character_top_y)  # วาดการกระทำของคำพิเศษ

            if self.input_box_visible:
                self.input_box.draw_input_box()  # วาดกล่องข้อความ
                if self.cursor_visible and self.active:
                    self.input_box.draw_cursor()  # วาดตัวชี้ตำแหน่ง

            # อัปเดตหน้าจอ
            pg.display.update()
            clock.tick(60)  # จำกัดเฟรมเรตที่ 60 เฟรมต่อวินาที

    def display_message(self, text):
        """แสดงข้อความที่กลางหน้าจอ"""
        self.window.fill(WHITE)  # เติมสีขาวทั้งหน้าจอ
        font = pg.font.Font(None, 74)  # กำหนดขนาดฟอนต์
        message = font.render(text, True, BLACK)  # สร้างข้อความ
        text_rect = message.get_rect(center=(self.width // 2, self.height // 2))  # ตั้งตำแหน่งข้อความให้กลางหน้าจอ
        self.window.blit(message, text_rect)  # วาดข้อความ
        pg.display.update()  # อัปเดตหน้าจอ
        pg.time.delay(2000)  # หยุด 2 วินาทีเพื่อให้ผู้เล่นเห็นข้อความ

# เริ่มเกม
if __name__ == "__main__":
    game = Game()  # สร้างเกมและเริ่มเกม
