import pygame as pg 

class CharMarker:
    # คลาสสำหรับจัดการตำแหน่งตัวบอกตำแหน่ง (Marker) บน minimap
    def __init__(self, game_instance, minimap, box_stack):
        # ฟังก์ชันเริ่มต้นของคลาส ใช้สำหรับกำหนดค่าที่จำเป็น
        self.game_instance = game_instance  # อินสแตนซ์ของเกมที่ใช้งานอยู่
        self.minimap = minimap  # วัตถุแผนที่ย่อ (minimap)
        self.box_stack = box_stack  # กองกล่องที่ใช้ในเกม

        self.marker_img = pg.image.load("assets/char.png")  # โหลดภาพตัวบอกตำแหน่ง
        self.marker_image = pg.transform.scale(self.marker_img, (30, 30))  # ปรับขนาดภาพให้เป็น 30x30 พิกเซล

        # เก็บค่าความกว้างและความสูงของภาพ
        self.marker_width = self.marker_image.get_width()
        self.marker_height = self.marker_image.get_height()

        # คำนวณตำแหน่งเริ่มต้นของตัวบอกตำแหน่งบน minimap
        self.marker_x = self.minimap.map_x + (self.minimap.map_img.get_width() // 2) - (self.marker_width // 2)
        self.marker_y = self.minimap.map_y + self.minimap.map_img.get_height() - self.marker_height - 30
        self.scale_factor = 1 / 2.7  # ตัวแปรสำหรับสัดส่วนการย่อ-ขยาย

        self.round = 1  # กำหนดค่าเริ่มต้นของรอบ

    def update(self, moveup, movedown, char_count=0, distance=120):
        """
        อัปเดตตำแหน่งตัวบอกตำแหน่ง (Marker)
        moveup: การย้ายตำแหน่งขึ้น
        movedown: การย้ายตำแหน่งลง
        char_count: จำนวนตัวละครที่ต้องเลื่อน
        distance: ระยะทางที่ตัวบอกตำแหน่งจะเคลื่อนที่
        """
        if moveup:  # ตรวจสอบว่ามีการย้ายขึ้นหรือไม่
            if self.round == 1:  # หากอยู่ในรอบแรก
                self.marker_y -= char_count * self.box_stack.box_height * self.scale_factor
            else:  # หากไม่ใช่รอบแรก
                self.marker_y -= char_count * self.box_stack.box_height * self.scale_factor
                self.marker_y += distance * self.scale_factor / 1.5
        elif movedown:  # ตรวจสอบว่ามีการย้ายลงหรือไม่
            if self.round == 1:
                pass  # รอบแรกไม่มีการย้ายลง
            else:
                self.marker_y += distance * self.scale_factor / 1.5
        self.round += 1  # เพิ่มค่ารอบการทำงาน

    def draw(self):
        """
        วาดตัวบอกตำแหน่ง (Marker) บน minimap
        """
        if not self.game_instance.input_box_visible:  # ถ้า input box ไม่แสดง
            self.game_instance.window.blit(self.marker_image, (self.marker_x, self.marker_y))  # วาดตัวบอกตำแหน่ง
