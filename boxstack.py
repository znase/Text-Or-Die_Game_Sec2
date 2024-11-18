import pygame as pg
import gif_pygame
import os

round = 1  # ตัวแปรรอบของเกม

class BoxStack:
    def __init__(self, game_instance):
        """สร้างคลาส BoxStack พร้อมการตั้งค่าเริ่มต้นของกล่องและตัวละคร"""
        self.game_instance = game_instance  # อ้างอิงถึงอินสแตนซ์ของเกมหลัก
        self.stack_positions = []  # ตำแหน่งของกล่องในสแตก
        self.letter_images = []  # รูปภาพตัวอักษรที่จะแสดงบนกล่อง
        self.pending_boxes = 0  # จำนวนกล่องที่รอการเพิ่ม
        self.box_timer = pg.time.get_ticks()  # ตัวจับเวลาเพื่อควบคุมการเพิ่มกล่อง
        self.round = 1  # จำนวนรอบ

        # โหลดรูปภาพกล่องและปรับขนาดเป็น 1/4 ของขนาดเดิม
        self.original_box_img = pg.image.load(r"assets/box.png")
        self.box_img = pg.transform.scale(self.original_box_img, 
                                          (self.original_box_img.get_width() // 4, 
                                           self.original_box_img.get_height() // 4))
        self.box_width = self.box_img.get_width()  # ความกว้างของกล่อง
        self.box_height = self.box_img.get_height()  # ความสูงของกล่อง

        # โหลดภาพเคลื่อนไหวตัวละครจากไฟล์ GIF
        self.char_gif = gif_pygame.load(r"assets/pet.gif")
        self.character_y_offset = -self.char_gif.get_height()  # ตำแหน่ง Y ที่ใช้ปรับให้ตรงกับกล่อง

        # โหลดภาพตัวละครแบบคงที่
        self.char_img = pg.image.load(r"assets/char.png")
        self.char_width = self.char_img.get_width()
        self.char_height = self.char_img.get_height()
        self.char_img = pg.transform.scale(self.char_img, (self.char_width//2, self.char_height//2))  # ปรับขนาดตัวละคร

        # กำหนดกล่องเริ่มต้นหนึ่งกล่องในตำแหน่งเริ่มต้น
        initial_y = self.game_instance.height - self.box_height - 200
        self.stack_positions.append(initial_y)

    def add_letters(self, letters):
        """เพิ่มรูปภาพตัวอักษรลงในกล่องจากลิสต์ของข้อความ"""
        for letter in reversed(letters):  # เรียงตัวอักษรจากล่างขึ้นบน
            letter_img_path = os.path.join("assets", "letters", f"{letter}.png")  # กำหนดเส้นทางของรูปตัวอักษร
            letter_img = pg.image.load(letter_img_path)
            
            # ปรับขนาดรูปตัวอักษรให้เหมาะสมกับกล่อง
            scaled_letter_img = pg.transform.scale(letter_img, (self.box_width-40, self.box_height))
            self.letter_images.insert(0, scaled_letter_img)  # แทรกรูปตัวอักษรลงในลิสต์

    def move_down(self, distance=120):
        if self.round == 1:
            pass  # หากเป็นรอบแรก ไม่ต้องเลื่อน
        else:
            for i in range(len(self.stack_positions)):
                self.stack_positions[i] += distance
        self.round += 1  # เพิ่มรอบในตัวแปรภายใน


    def add_boxes(self, count):
        """กำหนดจำนวนกล่องที่ต้องเพิ่มแบบทีละหนึ่ง"""
        self.pending_boxes += count  # เพิ่มจำนวนกล่องที่รอการเพิ่ม

    def update(self):
        """อัปเดตกล่องใน stack โดยเพิ่มกล่องที่รอค้างอยู่"""
        current_time = pg.time.get_ticks()
        if self.pending_boxes > 0 and current_time - self.box_timer >= 1000:  # ตรวจสอบเวลาที่ผ่านไป 1 วินาที
            new_y = self.stack_positions[0] - self.box_height  # กำหนดตำแหน่งกล่องใหม่
            self.stack_positions.insert(0, new_y)  # เพิ่มกล่องใหม่ที่ตำแหน่งบนสุดของ stack
            self.pending_boxes -= 1  # ลดจำนวนกล่องที่รอการเพิ่ม
            self.box_timer = current_time  # รีเซ็ตเวลา

        return self.pending_boxes == 0  # คืนค่า True หากไม่มีกล่องรอการเพิ่ม

    def get_character_top(self):
        """คืนค่า y-coordinate ของขอบบนตัวละครสำหรับการตรวจจับการชน"""
        if self.stack_positions:
            return self.stack_positions[0] + self.character_y_offset - 120  # คำนวณตำแหน่งขอบบน
        return None  # คืนค่า None หากไม่มี stack

    def draw(self):
        """วาดกล่อง ตัวอักษร และตัวละครบนหน้าจอเกม"""
        x_center = (self.game_instance.width - self.box_width) // 2  # คำนวณตำแหน่ง x ตรงกลาง
        for i, y in enumerate(self.stack_positions):
            self.game_instance.window.blit(self.box_img, (x_center, y))  # วาดกล่อง
            if i < len(self.letter_images):  # วาดตัวอักษรหากมี
                letter_x = x_center + (self.box_width - self.letter_images[i].get_width()) // 2
                letter_y = y + (self.box_height - self.letter_images[i].get_height()) // 2
                self.game_instance.window.blit(self.letter_images[i], (letter_x, letter_y))

        if self.stack_positions:  # วาดตัวละครบนกล่องบนสุด
            character_x = x_center
            character_y = self.stack_positions[0] + self.character_y_offset

            if self.game_instance.moveup:  # หากตัวละครเคลื่อนไหว
                self.char_gif.unpause()
                self.char_gif.render(self.game_instance.window, (character_x - 20, character_y + 5))
            else:  # หากตัวละครหยุด
                self.char_gif.pause()
                self.game_instance.window.blit(self.char_img, (character_x - 5, character_y + 20))

    def get_character_rect(self):
        """คืนค่าเรคแทงเกิลของตัวละครที่อยู่บนกล่องบนสุด"""
        if self.stack_positions:
            character_x = (self.game_instance.width - self.box_width) // 2
            character_y = self.stack_positions[0] + self.character_y_offset

            if self.game_instance.moveup:
                return pg.Rect(character_x - 10, character_y, self.char_gif.get_width(), self.char_gif.get_height())
            else:
                return pg.Rect(character_x - 10, character_y, self.char_img.get_width(), self.char_img.get_height())
        return None  # คืนค่า None หากไม่มี stack
