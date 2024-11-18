# moving_water.py
import pygame as pg

class Water:
    def __init__(self, game_instance):
        """
        สร้างคลาส Water สำหรับการจัดการภาพน้ำเคลื่อนไหว
        """
        self.game_instance = game_instance  # อินสแตนซ์ของเกมเพื่อเข้าถึงหน้าต่างและค่าที่เกี่ยวข้อง
        
        # โหลดภาพน้ำและปรับขนาดให้เท่ากับความกว้างของหน้าจอ
        self.water_img = pg.image.load("assets/water.png")
        self.water_img = pg.transform.scale(self.water_img, 
                                            (self.game_instance.width, self.water_img.get_height()))

        # กำหนดตำแหน่งเริ่มต้นให้แสดงเฉพาะส่วนคลื่นที่ด้านล่างของหน้าจอ
        self.y_position = self.game_instance.height - 400  # ตำแหน่ง Y เริ่มต้น (ปรับตามความสูงของคลื่น)
        self.target_y_position = self.y_position  # กำหนดตำแหน่งเป้าหมายให้เท่ากับตำแหน่งเริ่มต้น
        self.rise_amount = 10  # ระยะที่น้ำจะเพิ่มขึ้นต่อการตอบคำถาม
        self.slide_speed = 0.5  # ความเร็วในการเลื่อนภาพน้ำขึ้น

    def add_water(self):
        """
        เพิ่มระดับน้ำโดยเลื่อนตำแหน่งเป้าหมายขึ้น
        """
        self.target_y_position -= self.rise_amount  # ลดค่าตำแหน่งเป้าหมายลง (น้ำเพิ่มสูงขึ้น)

    def update(self):
        """
        เลื่อนภาพน้ำขึ้นไปทีละน้อยจนถึงตำแหน่งเป้าหมาย
        """
        if self.y_position > self.target_y_position:  # ตรวจสอบว่าน้ำยังไม่ถึงตำแหน่งเป้าหมาย
            self.y_position -= self.slide_speed  # เลื่อนตำแหน่ง Y ขึ้นด้วยความเร็วที่กำหนด
        
        # หากน้ำถึงตำแหน่งเป้าหมายแล้ว
        if self.y_position <= self.target_y_position:
            return True  # การเคลื่อนไหวเสร็จสิ้น
        return False  # ยังมีการเคลื่อนไหวต่อ

    def get_top(self):
        """
        คืนค่าตำแหน่ง Y ด้านบนของน้ำ สำหรับการตรวจจับการชน
        """
        return self.y_position  # ตำแหน่ง Y ปัจจุบันของน้ำ

    def draw(self):
        """
        วาดภาพน้ำบนหน้าจอโดยใช้ตำแหน่ง Y ปัจจุบัน
        """
        # แสดงภาพน้ำที่ตำแหน่งปัจจุบันบนหน้าต่างของเกม
        self.game_instance.window.blit(self.water_img, (0, self.y_position))
