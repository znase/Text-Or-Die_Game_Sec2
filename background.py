# background.py
import pygame as pg

class Background:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.bg_img = pg.image.load(r"assets/bg.jpg")  # โหลดภาพพื้นหลัง
        self.bg_y = self.game_instance.height - self.bg_img.get_height()  # เริ่มต้นที่ล่างสุด
        self.move_step = 100  # จำนวนพิกเซลที่จะเลื่อนขึ้นในแต่ละครั้ง

    def move_up(self):
        # เลื่อนพื้นหลังขึ้น 50 px
        self.bg_y += self.move_step
        # หยุดการเลื่อนถ้าถึงขอบบนสุด
        if self.bg_y >= 0:
            self.bg_y = 0
            return True  # ส่งค่ากลับเพื่อหยุดเกม
        return False

    def draw(self):
        # วาดภาพพื้นหลังที่ตำแหน่งปัจจุบัน
        self.game_instance.window.blit(self.bg_img, (0, self.bg_y))
