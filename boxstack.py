import pygame as pg
import os


class BoxStack:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.original_box_img = pg.image.load(r"assets/box.png")
        self.box_img = pg.transform.scale(self.original_box_img, 
                                          (self.original_box_img.get_width() // 4, 
                                           self.original_box_img.get_height() // 4))
        self.box_width = self.box_img.get_width()
        self.box_height = self.box_img.get_height()
        self.stack_positions = []

        # โหลดภาพตัวละครและปรับขนาด
        self.original_character_img = pg.image.load(r"assets/char.png")
        self.character_img = pg.transform.scale(self.original_character_img, 
                                                (self.original_character_img.get_width() // 2, 
                                                 self.original_character_img.get_height() // 2))  
        self.character_y_offset = -self.character_img.get_height()

        # ตำแหน่งเริ่มต้นให้มีกล่องหนึ่งกล่อง
        initial_y = self.game_instance.height - self.box_height - 200
        self.stack_positions.append(initial_y)

        # เก็บรายการภาพตัวอักษรในแต่ละตำแหน่งกล่อง
        self.letter_images = []

    def add_letters(self, letters):
        """เพิ่มรูปภาพตัวอักษรใหม่จาก list(text) โดยไม่ลบตัวอักษรเก่า"""
        for letter in reversed(letters):
            letter_img_path = os.path.join("assets", "letters", f"{letter}.png")
            letter_img = pg.image.load(letter_img_path)
            
            # ปรับขนาดภาพตัวอักษรให้พอดีกับกล่อง
            scaled_letter_img = pg.transform.scale(letter_img, (self.box_width, self.box_height))
            self.letter_images.insert(0, scaled_letter_img)  # เพิ่มตัวอักษรใหม่ด้านบนสุด

    def move_down(self, distance=80):
        for i in range(len(self.stack_positions)):
            self.stack_positions[i] += distance

    def add_boxes(self, count):
        # เลื่อนกล่องทั้งหมดลงและเพิ่มกล่องใหม่
        self.stack_positions = [y + 80 for y in self.stack_positions]
        for _ in range(count):
            new_y = self.stack_positions[0] - self.box_height
            self.stack_positions.insert(0, new_y)

    def draw(self):
        x_center = (self.game_instance.width - self.box_width) // 2
        for i, y in enumerate(self.stack_positions):
            # วาดกล่อง
            self.game_instance.window.blit(self.box_img, (x_center, y))
            # วาดตัวอักษรบนกล่อง
            if i < len(self.letter_images):
                letter_x = x_center + (self.box_width - self.letter_images[i].get_width()) // 2
                letter_y = y + (self.box_height - self.letter_images[i].get_height()) // 2
                self.game_instance.window.blit(self.letter_images[i], (letter_x, letter_y))
        
        # วาดตัวละครที่อยู่บนกล่องด้านบนสุด
        if self.stack_positions:
            character_x = x_center
            character_y = self.stack_positions[0] + self.character_y_offset
            self.game_instance.window.blit(self.character_img, (character_x - 10, character_y + 5))
