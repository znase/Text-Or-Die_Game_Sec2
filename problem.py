import pandas as pd
import random
import pygame as pg
from rapidfuzz import process

# โหลดข้อมูล dictionary
df = pd.read_excel(r'data/dictionary.xlsx', sheet_name='dictionary')
letters = "abcdefghijklmnopqrstuvwxyz"

# สร้าง mapping ระหว่างตัวอักษร a ถึง z และ column ที่สอดคล้องใน DataFrame
column_map = {chr(i): chr(i) for i in range(ord('a'), ord('z') + 1)}

class problemBox:
    def __init__(self, game_instance):
        """
        สร้างคลาส problemBox สำหรับแสดงและตรวจสอบปัญหาการป้อนคำศัพท์
        """
        self.game_instance = game_instance  # อินสแตนซ์ของเกมหลัก
        self.font = pg.font.Font(None, 36)  # กำหนดฟอนต์และขนาดตัวอักษร
        self.window = game_instance.window  # หน้าต่างเกมสำหรับการวาดภาพ

        # โหลดและปรับขนาดภาพพื้นหลังของปัญหา
        self.bg_image = pg.image.load("assets/letters/textBox.png")
        self.bg_image = pg.transform.scale(self.bg_image, (550, 80))  # ปรับขนาดภาพตามต้องการ

    def random_problem(self):
        """
        สุ่มตัวอักษร 2 ตัวจากตัวอักษรภาษาอังกฤษ a-z
        """
        return random.sample(letters, 2)

    def display_problem(self, letters, input_box_visible):
        """
        แสดงข้อความปัญหาบนหน้าจอพร้อมภาพพื้นหลัง เมื่อ input box ถูกแสดง
        """
        if input_box_visible:
            # วาดภาพพื้นหลังที่ตำแหน่งตรงกลางของหน้าจอ
            bg_x = (self.game_instance.width - self.bg_image.get_width()) // 2
            bg_y = (self.game_instance.height // 2 - 340)  # ปรับตำแหน่ง Y ตามต้องการ
            self.window.blit(self.bg_image, (bg_x, bg_y))

            # เรนเดอร์ข้อความของปัญหา และแสดงผล
            text_surface = self.font.render(
                f"Input a word with letters '{letters[0].upper()}' and '{letters[1].upper()}'", 
                True, (0, 0, 0)
            )
            text_rect = text_surface.get_rect(center=(self.game_instance.width // 2, self.game_instance.height // 2 - 300))
            self.window.blit(text_surface, text_rect)

    def check_text(self, problem, text):
        """
        ตรวจสอบว่าคำที่ผู้ใช้ป้อนตรงตามเงื่อนไขของปัญหาหรือไม่
        """
        text = text.lower()  # แปลงข้อความให้เป็นตัวพิมพ์เล็ก

        # ตรวจสอบว่าข้อความเป็นตัวอักษรทั้งหมดและไม่ใช่ค่าว่าง
        if all(char in letters for char in text) and text != "":
            # ตรวจสอบตัวอักษรแรกของข้อความ และค้นหาใน dictionary column ที่สอดคล้อง
            first_char = text[0]
            column = column_map.get(first_char, 'a')  # หากไม่มีการแมป จะใช้ค่า default เป็น 'a'
            match = process.extractOne(text, df[column])

            # ตรวจสอบว่าคำตรงใน dictionary และประกอบด้วยตัวอักษรในปัญหาทั้งหมด
            if match and match[1] == 100.00 and all(letter in text for letter in problem):
                print("Correct")  # แสดงข้อความเมื่อคำถูกต้อง
                score = len(text)  # คำนวณคะแนนตามความยาวของคำ
                return list(text)  # คืนค่าคำในรูปแบบลิสต์
        else:
            print("Incorrect")  # แสดงข้อความเมื่อคำไม่ถูกต้อง
            score = 0
            return None
