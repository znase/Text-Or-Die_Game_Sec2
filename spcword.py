# spcword.py
import pygame as pg

class SpecialWordActions:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.actions = {
            "fire": self.show_fire_image
            # สามารถเพิ่มคำพิเศษใหม่ได้ที่นี่
        }

        # โหลดภาพที่ต้องการใช้
        self.images = {
            "fire": pg.image.load("assets/fire.png").convert_alpha()
        }

        self.current_image = None
        self.image_timer = 0

    def trigger_action(self, word):
        """เรียก action ตามคำที่ผู้ใช้พิมพ์"""
        if word in self.actions:
            self.actions[word]()  # เรียกฟังก์ชัน action ตามคำ

    def show_fire_image(self, duration=2000):
        """แสดงภาพ fire.png บนหน้าจอ"""
        self.current_image = self.images["fire"]
        self.image_timer = pg.time.get_ticks() + duration


    def draw(self):
        """วาดภาพที่กำลังแสดงอยู่บนหน้าจอ"""
        if self.current_image:
            # กำหนดตำแหน่งแสดงภาพไว้ตรงกลาง
            x = self.game_instance.width // 2 - self.current_image.get_width() // 2
            y = self.game_instance.height // 2 - self.current_image.get_height() // 2
            self.game_instance.window.blit(self.current_image, (x, y))

            # ตรวจสอบเวลา ถ้าครบกำหนดให้หยุดแสดงภาพ
            if pg.time.get_ticks() > self.image_timer:
                self.current_image = None
