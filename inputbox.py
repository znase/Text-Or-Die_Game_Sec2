# inputbox.py
import pygame as pg

WHITE = (255, 255, 255)  # สีพื้นหลังของกล่องข้อความ (สีขาว)

class inputBox:
    def __init__(self, game_instance):
        """
        สร้างคลาส inputBox สำหรับจัดการการรับข้อความจากผู้ใช้
        """
        self.game_instance = game_instance  # อ้างอิงถึงอินสแตนซ์ของเกมหลัก
        self.window = self.game_instance.window  # หน้าต่างเกมสำหรับวาดกล่องข้อความ
        self.font = pg.font.Font(None, 36)  # กำหนดฟอนต์และขนาดตัวอักษร

        # กำหนดขนาดและตำแหน่งของกล่องข้อความ
        self.input_box_width = 300
        self.input_box_height = 40
        self.input_box = pg.Rect(
            (self.game_instance.width - self.input_box_width) // 2 - 100,  # ตำแหน่ง X (กึ่งกลาง)
            (self.game_instance.height // 3 * 2 + 50),  # ตำแหน่ง Y (ส่วนล่างของหน้าจอ)
            self.input_box_width,  # ความกว้าง
            self.input_box_height  # ความสูง
        )

        # กำหนดสีของกล่องข้อความในสถานะต่าง ๆ
        self.color_inactive = pg.Color(30, 144, 255)  # สีน้ำเงินเมื่อไม่ได้โฟกัส
        self.color_active = pg.Color(0, 191, 255)  # สีฟ้าเมื่อโฟกัส
        self.color = self.color_inactive  # เริ่มต้นด้วยสถานะไม่ได้โฟกัส

        self.text = ''  # ข้อความที่ผู้ใช้พิมพ์
        self.active = False  # สถานะของกล่องข้อความ (True เมื่อโฟกัส)

    def draw_input_box(self):
        """
        วาดกล่องข้อความบนหน้าต่างเกม พร้อมแสดงข้อความที่พิมพ์
        """
        if self.game_instance.input_box_visible:  # ตรวจสอบว่ากล่องข้อความถูกตั้งให้มองเห็นหรือไม่
            # เรนเดอร์ข้อความที่พิมพ์ลงในกล่อง
            txt_surface = self.font.render(self.text, True, self.color)

            # ปรับความกว้างของกล่องให้พอดีกับข้อความ
            width = max(500, txt_surface.get_width() + 10)
            self.input_box.w = width

            # วาดพื้นหลังของกล่องข้อความ
            self.window.fill(WHITE, self.input_box)

            # วาดข้อความในตำแหน่งที่เหมาะสม
            self.window.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

            # วาดกรอบกล่องข้อความ
            pg.draw.rect(self.window, self.color, self.input_box, 2)

    def draw_cursor(self):
        """
        วาดเคอร์เซอร์ที่ตำแหน่งท้ายข้อความในกล่องข้อความ
        """
        # คำนวณตำแหน่ง X ของเคอร์เซอร์โดยอิงตามความยาวข้อความ
        cursor_x = self.input_box.x + 5 + self.font.size(self.text)[0]

        # ความสูงของเคอร์เซอร์ (ปรับให้เล็กกว่ากล่องข้อความเล็กน้อย)
        cursor_height = self.input_box.height - 10

        # วาดเคอร์เซอร์เป็นสี่เหลี่ยมผืนผ้าสีเดียวกับกล่องข้อความ
        pg.draw.rect(self.window, self.color, (cursor_x, self.input_box.y + 5, 2, cursor_height))
