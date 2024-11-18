import pygame as pg
from char import CharMarker

class Minimap:
    def __init__(self, game_instance, box_stack):
        """
        สร้างคลาส Minimap สำหรับแสดงภาพแผนที่ขนาดเล็ก 
        และตัวบอกตำแหน่งของตัวละครบนหน้าต่างเกม
        """
        self.game_instance = game_instance  # อ้างอิงถึงอินสแตนซ์ของเกมหลัก
        
        # โหลดภาพแผนที่จริง และปรับขนาดให้เป็นแผนที่ขนาดเล็ก
        self.realmap_img = pg.image.load(r"assets/minimap.jpg")
        self.map_img = pg.transform.scale(self.realmap_img, (100, 467))  # ขนาดใหม่ของภาพ minimap

        # กำหนดตำแหน่งของ minimap ที่ด้านขวาบนของหน้าจอ
        self.map_x = self.game_instance.width - 110  # ค่ากำหนด X (ขอบขวา)
        self.map_y = 10  # ค่ากำหนด Y (ขอบบน)

        # จำนวนพิกเซลต่อตัวอักษรสำหรับเลื่อนตำแหน่ง marker
        self.pixel_per_char = 6.6

        # ตัวบอกตำแหน่งตัวละครใน minimap
        self.char_marker = CharMarker(game_instance, self, box_stack)

    def update(self, characters_moved, moveup, movedown):
        """
        อัปเดตตำแหน่ง marker ของตัวละครใน minimap
        """
        # เรียกใช้งานฟังก์ชัน update ใน CharMarker
        self.char_marker.update(moveup, movedown, characters_moved)

    def draw(self):
        """
        วาด minimap และตัวบอกตำแหน่งของตัวละครบนหน้าจอ
        """
        if not self.game_instance.input_box_visible:  # วาดเมื่อกล่องข้อความไม่ได้แสดงผล
            # วาด minimap ที่ตำแหน่งกำหนด
            self.game_instance.window.blit(self.map_img, (self.map_x, self.map_y))
            # วาดตัวบอกตำแหน่งของตัวละคร
            self.char_marker.draw()
