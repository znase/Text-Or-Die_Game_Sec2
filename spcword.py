# spcword.py
import pygame as pg

class SpecialWordActions:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.actions = {
            "fire": self.show_fire_image,
            "rain": self.show_rain_image
            # สามารถเพิ่มคำพิเศษใหม่ได้ที่นี่
        }

        # โหลดภาพที่ต้องการใช้
        self.images = {
            "fire": pg.image.load("assets/fire.png").convert_alpha(),
            "rain": pg.image.load("assets/rain.png").convert_alpha()
        }

        self.current_image = None
        self.current_image_name = None  # เก็บชื่อของภาพปัจจุบัน
        self.image_timer = 0

    def trigger_action(self, word):
        """เรียก action ตามคำที่ผู้ใช้พิมพ์"""
        if word in self.actions:
            self.actions[word]()  # เรียกฟังก์ชัน action ตามคำ

    def show_fire_image(self, duration=2000):
        """แสดงภาพ fire.png ที่ถูกปรับขนาดบนหน้าจอ"""
        original_image = self.images["fire"]
        # ปรับขนาดภาพให้เล็กลง 50%
        self.current_image = pg.transform.scale(original_image, (original_image.get_width() // 4, original_image.get_height() // 4))
        self.current_image_name = "fire"  # กำหนดชื่อภาพปัจจุบัน
        self.image_timer = pg.time.get_ticks() + duration
        
    def show_rain_image(self, duration=2000):
        """แสดงภาพ rain.png ที่ถูกปรับขนาดบนหน้าจอ"""
        original_image = self.images["rain"]
        # ปรับขนาดภาพให้เล็กลง 50%
        self.current_image = pg.transform.scale(original_image, (original_image.get_width() // 2, original_image.get_height() // 2))
        self.current_image_name = "rain"  # กำหนดชื่อภาพปัจจุบัน
        self.image_timer = pg.time.get_ticks() + duration

    def draw(self, character_y_position):
        """วาดภาพที่กำลังแสดงอยู่บนหน้าจอ"""
        if self.current_image:
            # คำนวณตำแหน่ง X ตรงกลางหน้าจอ
            x = self.game_instance.width // 2 - self.current_image.get_width() // 2
            
            # กำหนดตำแหน่ง Y ให้อยู่ด้านบนตัวละคร
            y = character_y_position - self.current_image.get_height() + 140  # เลื่อนขึ้นเหนือหัวตัวละคร 10 px

            # วาดภาพบนหน้าจอ
            self.game_instance.window.blit(self.current_image, (x, y))

            # ตรวจสอบเวลา ถ้าครบกำหนดให้หยุดแสดงภาพ
            if pg.time.get_ticks() > self.image_timer:
                self.current_image = None
                self.current_image_name = None  # รีเซ็ตชื่อภาพ
