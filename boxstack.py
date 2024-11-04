# boxstack.py
import pygame as pg

class BoxStack:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.original_box_img = pg.image.load(r"assets/box.png")  # โหลดภาพกล่องขนาดเดิม

        # ปรับขนาดกล่องให้เล็กลง (เช่น ปรับเป็น 50% ของขนาดเดิม)
        self.box_img = pg.transform.scale(self.original_box_img, 
                                          (self.original_box_img.get_width() // 4, 
                                           self.original_box_img.get_height() // 4))
        self.box_width = self.box_img.get_width()
        self.box_height = self.box_img.get_height()
        self.stack_positions = []  # ตำแหน่งของกล่องแต่ละใบในสแตก

    def add_boxes(self, count):
        """
        เพิ่มกล่องใหม่ลงในสแตกตามจำนวนตัวอักษรที่ถูกต้อง โดยเลื่อนกล่องทั้งหมดลง 50px
        แล้วเพิ่มกล่องชุดใหม่จากด้านบน
        """
        # เลื่อนตำแหน่งของกล่องทั้งหมดลง 50px
        self.stack_positions = [y + 50 for y in self.stack_positions]

        for _ in range(count):
            if not self.stack_positions:
                # วางกล่องชุดแรกที่ด้านล่างของหน้าจอ
                new_y = self.game_instance.height - self.box_height
            else:
                # วางกล่องชุดถัดไปต่อจากด้านบนของกล่องด้านบนสุดในสแตก
                new_y = self.stack_positions[0] - self.box_height
            
            # เพิ่มตำแหน่งกล่องใหม่ในสแตก
            self.stack_positions.insert(0, new_y)  # เพิ่มที่ตำแหน่งบนสุดของสแตก

    def draw(self):
        """
        วาดกล่องแต่ละใบในสแตกบนหน้าจอเกม โดยจัดให้กล่องอยู่กลางหน้าจอในแนวนอน
        """
        x_center = (self.game_instance.width - self.box_width) // 2  # จัดกล่องให้อยู่กลางหน้าจอในแนวนอน
        for y in self.stack_positions:
            self.game_instance.window.blit(self.box_img, (x_center, y))
