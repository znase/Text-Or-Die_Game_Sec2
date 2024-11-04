import pygame as pg

class BoxStack:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.original_box_img = pg.image.load(r"assets/box.png")  # โหลดภาพกล่องขนาดเดิม
        self.box_img = pg.transform.scale(self.original_box_img, 
                                          (self.original_box_img.get_width() // 4, 
                                           self.original_box_img.get_height() // 4))
        self.box_width = self.box_img.get_width()
        self.box_height = self.box_img.get_height()
        self.stack_positions = []  # ตำแหน่งของกล่องแต่ละใบในสแตก

        # โหลดภาพตัวละครและปรับขนาด
        self.original_character_img = pg.image.load(r"assets/character.png")
        self.character_img = pg.transform.scale(self.original_character_img, 
                                                (self.original_character_img.get_width() // 2, 
                                                 self.original_character_img.get_height() // 2))  
        self.character_y_offset = -self.character_img.get_height()  # ตำแหน่งที่ตัวละครยืนอยู่บนกล่อง

    def move_down(self, distance=50):
        for i in range(len(self.stack_positions)):
            self.stack_positions[i] += distance  # เลื่อนแต่ละกล่องลงตามระยะทางที่กำหนด

    def add_boxes(self, count):
        self.stack_positions = [y + 50 for y in self.stack_positions]
        for _ in range(count):
            if not self.stack_positions:
                new_y = self.game_instance.height - self.box_height - 150
            else:
                new_y = self.stack_positions[0] - self.box_height
            self.stack_positions.insert(0, new_y)

    def draw(self):
        x_center = (self.game_instance.width - self.box_width) // 2  # จัดกล่องให้อยู่กลางหน้าจอในแนวนอน
        for i, y in enumerate(self.stack_positions):
            self.game_instance.window.blit(self.box_img, (x_center, y))
        
        # วาดตัวละครที่อยู่บนกล่องด้านบนสุด
        if self.stack_positions:
            character_x = x_center
            character_y = self.stack_positions[0] + self.character_y_offset
            self.game_instance.window.blit(self.character_img, (character_x - 30, character_y))
