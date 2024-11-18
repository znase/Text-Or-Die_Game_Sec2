import pygame as pg

class Background:
    def __init__(self, game_instance):
        # กำหนดค่าตัวแปรเริ่มต้นสำหรับคลาส Background
        self.game_instance = game_instance  # เก็บอินสแตนซ์ของเกม เพื่อใช้ข้อมูลและฟังก์ชันที่เกี่ยวข้อง
        self.bg_img = pg.image.load(r"assets/bg.jpg")  # โหลดรูปภาพพื้นหลัง
        self.bg_y = self.game_instance.height - self.bg_img.get_height()  # กำหนดตำแหน่ง Y ของพื้นหลังเริ่มต้นให้อยู่ล่างสุดของหน้าจอ
        self.pixel_per_char = 40  # จำนวนพิกเซลที่พื้นหลังจะเลื่อนต่อ 1 ตัวอักษร
        self.target_y = self.bg_y  # กำหนดตำแหน่งเป้าหมายเริ่มต้นของ Y

    def move_up(self, char_count):
        # ฟังก์ชันสำหรับเลื่อนพื้นหลังขึ้นตามจำนวนตัวอักษรที่กำหนด
        move_distance = char_count * self.pixel_per_char  # คำนวณระยะทางที่ต้องเลื่อน
        self.target_y += move_distance  # ปรับตำแหน่งเป้าหมาย Y

    def update(self):
        # ฟังก์ชันอัปเดตตำแหน่งของพื้นหลัง
        if self.bg_y < self.target_y:  # หากพื้นหลังยังไม่ถึงเป้าหมาย
            self.bg_y += 1.5  # เลื่อนพื้นหลังขึ้นทีละ 1.5 พิกเซล

        if self.bg_y >= self.target_y:  # ตรวจสอบว่าพื้นหลังถึงเป้าหมายแล้วหรือยัง
            return True  # หากถึงแล้ว คืนค่า True
        return False  # หากยังไม่ถึง คืนค่า False

    def draw(self):
        # ฟังก์ชันสำหรับวาดพื้นหลังบนหน้าจอ
        self.game_instance.window.blit(self.bg_img, (0, self.bg_y))  # วาดรูปภาพพื้นหลังในตำแหน่ง (0, bg_y)
