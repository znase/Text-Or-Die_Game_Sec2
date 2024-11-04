# background.py
import pygame as pg

class Background:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.bg_img = pg.image.load(r"./assets/bg.jpg")  # โหลดภาพพื้นหลัง
        self.bg_y = self.game_instance.height - self.bg_img.get_height()  # เริ่มต้นที่ล่างสุด
        self.pixel_per_char = 20  # จำนวนพิกเซลที่เลื่อนขึ้นต่อ 1 ตัวอักษร

    def move_up(self, char_count):
        # คำนวณพิกเซลที่จะเลื่อนขึ้น
        move_distance = char_count * self.pixel_per_char
        self.bg_y += move_distance
        
        # หยุดการเลื่อนถ้าถึงขอบบนสุด
        if self.bg_y >= 0:
            self.bg_y = 0
            return True  # ส่งค่ากลับเพื่อหยุดเกม
        return False

    def draw(self):
        # วาดภาพพื้นหลังที่ตำแหน่งปัจจุบัน
        self.game_instance.window.blit(self.bg_img, (0, self.bg_y))
